from geo.models import tables
from geo.repositories.base import BaseRepository

class PickRepo(BaseRepository[tables.Pick]):
    table = tables.Pick