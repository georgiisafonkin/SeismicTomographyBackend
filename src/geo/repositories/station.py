from geo.models import tables
from geo.repositories.base import BaseRepository
from geo.models.schemas.station import StationsRequest, Station
from typing import List
from src.geo.config import logger
import aiohttp

class StationRepo(BaseRepository[tables.Station]):
    table = tables.Station

    

    async def fetch_station_by_network(self, station_request: StationsRequest) -> List[Station]:
        url = self.SERVER_URL + self.STATION
        params = {
            'network_code': station_request.network_code
        }
        logger.info(self.AUTH)
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as session:
            async with session.get(url, params=params, auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as response:
                result = await response.json()
                logger.info(result)
                return result

