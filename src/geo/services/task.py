import datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from geo.exceptions import NotFound
from geo.models.schemas import TaskID, Task, TaskState, TaskMetadata
from geo.repositories import TaskRepo, SeisDataRepo, EventRepo, PickRepo, StationRepo

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
    
    async def get_task_metadata(self, task_id: TaskID) -> TaskMetadata:
        async with self._lazy_session() as session:
            task_repo = TaskRepo(session)
            task = await task_repo.get(id=task_id)
        if not task:
            raise NotFound(f"Задача с id {task_id!r} не найдена") 
        
        logger.info(f"task_data: {task.seisdata}\n{task.stations}\n{task.events}")



        task_metadata = TaskMetadata(seisdata=task.seisdata,
                                     stations=task.stations,
                                     events=task.events)
        
        logger.info(f"task_metadata: {task_metadata}")

        return task_metadata


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
            if task.state == TaskState.IN_PROGRESS:
                raise NotFound(f"Задача с id {task_id!r} находится в обработке")
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

            # Добавление сейсданных
            seis_data_repo = SeisDataRepo(session)
            await seis_data_repo.create(start_time=task_metadata.seisdata.start_time,
                                  end_time=task_metadata.seisdata.end_time,
                                  network_code=task_metadata.network,
                                  min_latitude=task_metadata.seisdata.min_latitude,
                                  max_latitude=task_metadata.seisdata.max_latitude,
                                  min_longitude=task_metadata.seisdata.min_longitude,
                                  max_longitude=task_metadata.seisdata.max_longitude,
                                  task_id=task_id)

            # Добавление данных о станциях
            station_repo = StationRepo(session)
            for station in task_metadata.stations:
                cur_st = station_repo.get(code=station.code)
                if not cur_st:
                    station_repo.create(code=station.code,
                                        latitude=station.latitude,
                                        longitude=station.longitude,
                                        depth=station.depth,
                                        network_code=station.network_code)
                await task_repo.add_task_station_association(task_id=task_id, station_code=station.code)
                
            # Добавление данных об ивентах
            event_repo = EventRepo(session)
            pick_repo = PickRepo(session)
            for event in task_metadata.events:
                cur_event = event_repo.get(event_id=event.id)

                if not cur_event:
                    await event_repo.create(id=event.id,
                                      time=event.time,
                                      magnitude=event.magnitude,
                                      latitude=event.latitude,
                                      longitude=event.longitude,
                                      depth=event.depth,
                                      network_code=event.network_code,
                                      accepted=event.accepted)
                    for pick in event.picks:
                        await pick_repo.create(id=pick.id,
                                         time=pick.time,
                                         phase=pick.phase,
                                         station_code=pick.station_code)
                        
                        await event_repo.add_event_pick_association(event_id=event.id, pick_id=pick.id)
