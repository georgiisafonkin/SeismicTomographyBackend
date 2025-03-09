from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.geo.models.schemas.station import StationsRequest, Station
from src.geo.repositories.station import StationRepo
from src.geo.config import logger

class StationApplicationService:
    def __init__(
            self,
            lazy_session: async_sessionmaker[AsyncSession],
    ):
        self._lazy_session = lazy_session

    async def fetch_area_stations(self, station_request: StationsRequest):
        async with self._lazy_session() as session:
            station_repo = StationRepo(session)
            stations = await station_repo.fetch_station_by_network(station_request=station_request)
            logger.info(f"Stations object: {stations}")
            area_stations = list()
            for station in stations:
                if station_request.min_latitude <= station.latitude <= station_request.max_latitude and \
                    station_request.min_longitude <= station.longitude <= station_request.max_longitude:
                    area_stations.append(station)
        
        return area_stations

 
