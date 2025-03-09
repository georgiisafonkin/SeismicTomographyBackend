from src.geo.repositories.base import BaseRepository
from src.geo.models.schemas.station import StationsRequest, StationSchema
from src.geo.models.tables.station import Station
from typing import List
from src.geo.config import logger
import aiohttp

class StationRepo(BaseRepository[Station]):
    table = Station

    async def fetch_station_by_network(self, station_request: StationsRequest) -> List[StationSchema]:
        url = self.SERVER_URL + self.STATION
        params = {
            'network_code': station_request.network_code
        }
        logger.info(self.AUTH)
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as session:
            async with session.get(url, params=params, auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as response:
                result = await response.json()
                logger.info(result)
                return [StationSchema(**st) for st in result]

