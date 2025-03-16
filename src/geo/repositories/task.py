from src.geo.models.tables.task import Task
from geo.repositories.base import BaseRepository


class TaskRepo(BaseRepository[Task]):
    table = Task
