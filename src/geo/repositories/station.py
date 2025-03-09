from src.geo.config import DB_LOGIN, DB_PASSWORD
from geo.models import tables
from geo.repositories.base import BaseRepository


class StationRepo(BaseRepository[tables.Station]):
    table = tables.Station
    

    def get_stations():

