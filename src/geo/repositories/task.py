from geo.models.schemas.task import TaskID, TaskMetadata
from src.geo.models.tables.task import Task, task_station_table, task_event_table
from geo.repositories.base import BaseRepository
from sqlalchemy import select, insert


class TaskRepo(BaseRepository[Task]):
    table = Task       

    async def get_stations_ids(self, task_id: TaskID):
        return (await self._session.execute(select(task_station_table).filter_by(task_id))).scalars().all()
    
    async def get_events_ids(self, task_id: TaskID):
        return (await self._session.execute(select(task_event_table).filter_by(task_id))).scalars().all()
    
    async def add_task_station_association(self, task_id: TaskID, station_code: str, commit: bool = True):
        stmt = insert(task_station_table).values(task_id=task_id, station_code=station_code)
        await self._session.execute(stmt)
        if commit:
            await self._session.commit()

    async def add_task_event_association(self, task_id: TaskID, event_id: int, commit: bool = True):
        stmt = insert(task_event_table).values(task_id=task_id, event_id=event_id)
        await self._session.execute(stmt)
        if commit:
            await self._session.commit()