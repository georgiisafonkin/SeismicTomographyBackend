from geo.models import tables
from geo.repositories.base import BaseRepository


class UsersRepo(BaseRepository[tables.UserTable]):
    table = tables.UserTable