import datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from geo.exceptions import NotFound
from geo.models.schemas import TaskID, Task, TaskState, TaskMetadata
from geo.repositories import TaskRepo, SeisDataRepo, EventRepo, PickRepo, StationRepo
from geo.views.task import TaskMetadataResponse

from geo.config import logger


class TaskApplicationService:

    def __init__(
            self,
            lazy_session: async_sessionmaker[AsyncSession],
    ):
        self._lazy_session = lazy_session

    async def list(self, page: int, per_page: int) -> list[Task]:
        per_page_limit = 40

        per_page = min(per_page, per_page_limit, 2147483646)
        offset = min((page - 1) * per_page, 2147483646)

        async with self._lazy_session() as session:
            task_repo = TaskRepo(session)
            tasks = await task_repo.get_all(offset=offset, limit=per_page, order_by='created_at')
        result = [Task.model_validate(task) for task in tasks]
        result.reverse()
        return result

    async def get_task(self, task_id: TaskID) -> Task:
        async with self._lazy_session() as session:
            task_repo = TaskRepo(session)
            task = await task_repo.get(id=task_id)
        if not task:
            raise NotFound(f"Задача с id {task_id!r} не найдена")
        return Task.model_validate(task)
    
    async def get_task_metadata(self, task_id: TaskID) -> TaskMetadataResponse:
        async with self._lazy_session() as session:
            task_repo = TaskRepo(session)
            task = await task_repo.get(id=task_id)
            if not task:
                raise NotFound(f"Задача с id {task_id!r} не найдена") 
            await session.refresh(task)
            task_obj = Task.model_validate(task)

        return TaskMetadata(seisdata=task_obj.seisdata,
                                        stations=task_obj.stations,
                                        events=task_obj.events)


    async def new_task(self) -> Task:
        async with self._lazy_session() as session:
            task_repo = TaskRepo(session)
            task = await task_repo.create(
                state=TaskState.PLAIN,
                created_at=datetime.datetime.now(tz=datetime.UTC)
            )

        return Task.model_validate(task)

    async def delete_task(self, task_id: TaskID) -> None:
        async with self._lazy_session() as session:
            task_repo = TaskRepo(session)
            task = await task_repo.get(id=task_id)
            if not task:
                raise NotFound(f"Задача с id {task_id!r} не найдена")
            # if task.state == TaskState.IN_PROGRESS:
            #     raise NotFound(f"Задача с id {task_id!r} находится в обработке")
            await task_repo.delete(id=task_id)

    async def count(self) -> int:
        async with self._lazy_session() as session:
            task_repo = TaskRepo(session)
            count = await task_repo.count()
        return count
    
    async def update_metadata(self, task_id: TaskID, task_metadata: TaskMetadata) -> None:
        async with self._lazy_session() as session:
            task_repo = TaskRepo(session)
            task = await task_repo.get(id=task_id)

            if not task:
                raise NotFound(f"Задача с id {task_id!r} не найдена")
            if task.state == TaskState.IN_PROGRESS:
                raise NotFound(f"Задача с id {task_id!r} находится в обработке")

            # Обновление сейсданных
            seis_data_repo = SeisDataRepo(session)
            seis_data = await seis_data_repo.get(task_id=task_id)
            if seis_data:
                # Обновляем существующие сейсданные
                seis_data.start_time = task_metadata.seisdata.start_time
                seis_data.end_time = task_metadata.seisdata.end_time
                seis_data.network_code = task_metadata.seisdata.network_code
                seis_data.min_latitude = task_metadata.seisdata.min_latitude
                seis_data.max_latitude = task_metadata.seisdata.max_latitude
                seis_data.min_longitude = task_metadata.seisdata.min_longitude
                seis_data.max_longitude = task_metadata.seisdata.max_longitude
            else:
                # Создаем новые сейсданные, если их нет
                seis_data = await seis_data_repo.create(
                    start_time=task_metadata.seisdata.start_time,
                    end_time=task_metadata.seisdata.end_time,
                    network_code=task_metadata.seisdata.network_code,
                    min_latitude=task_metadata.seisdata.min_latitude,
                    max_latitude=task_metadata.seisdata.max_latitude,
                    min_longitude=task_metadata.seisdata.min_longitude,
                    max_longitude=task_metadata.seisdata.max_longitude,
                    task_id=task_id
                )

            # Обновление данных о станциях
            station_repo = StationRepo(session)
            for station in task_metadata.stations:
                cur_st = await station_repo.get(code=station.code)
                if not cur_st:
                    await station_repo.create(
                        code=station.code,
                        latitude=station.latitude,
                        longitude=station.longitude,
                        depth=station.depth,
                        network_code=station.network_code
                    )
                await task_repo.add_task_station_association(task_id=task_id, station_code=station.code)

            # Обновление данных об ивентах
            event_repo = EventRepo(session)
            pick_repo = PickRepo(session)
            for event in task_metadata.events:
                cur_event = await event_repo.get(id=event.id)

                if not cur_event:
                    cur_event = await event_repo.create(
                        id=event.id,
                        time=event.time,
                        magnitude=event.magnitude,
                        latitude=event.latitude,
                        longitude=event.longitude,
                        depth=event.depth,
                        network_code=event.network_code,
                        accepted=event.accepted
                    )
                    for pick in event.picks:
                        await pick_repo.create(
                            id=pick.id,
                            time=pick.time,
                            phase=pick.phase,
                            station_code=pick.station_code,
                            event_id=cur_event.id
                        )
                else:
                    # Если событие уже существует, обновляем его
                    cur_event.time = event.time
                    cur_event.magnitude = event.magnitude
                    cur_event.latitude = event.latitude
                    cur_event.longitude = event.longitude
                    cur_event.depth = event.depth
                    cur_event.network_code = event.network_code
                    cur_event.accepted = event.accepted

                    # Обновление пиков для существующего события
                    for pick in event.picks:
                        existing_pick = await pick_repo.get(id=pick.id)
                        if not existing_pick:
                            await pick_repo.create(
                                id=pick.id,
                                time=pick.time,
                                phase=pick.phase,
                                station_code=pick.station_code,
                                event_id=cur_event.id
                            )
                        else:
                            # Обновляем существующий пик
                            existing_pick.time = pick.time
                            existing_pick.phase = pick.phase
                            existing_pick.station_code = pick.station_code
                await task_repo.add_task_event_association(task_id=task_id, event_id=event.id)

            # Не забудьте зафиксировать изменения в базе данных
            await session.commit()