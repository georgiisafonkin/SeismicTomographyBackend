from geo.models import tables
from geo.repositories.base import BaseRepository
from geo.models.schemas.event import Event, EventRequest
from sqlalchemy import select, insert

from typing import List
import aiohttp
from datetime import datetime

from src.geo.config import logger

class EventRepo(BaseRepository[tables.Event]):
    table = tables.Event

    async def fetch_events_by_params(self, event_request: EventRequest) -> List[Event]:
        url = self.SERVER_URL + self.EVENT
        params = {
            'network': event_request.network_code,
            'start_time': event_request.start_time.isoformat(),
            'end_time': event_request.end_time.isoformat(),
            'min_lat': event_request.min_latitude,
            'max_lat': event_request.max_latitude,
            'min_lon': event_request.min_longitude,
            'max_lon': event_request.max_longitude,
            'min_depth': event_request.min_depth,
            'max_depth': event_request.max_depth,
            'accepted': str(True)
        }
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as session:
            async with session.get(url, params=params, auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as response:
                # logger.info(f"RESPONSE: {await response.json()}")
                result = await response.json()
                return [Event(**st) for st in result]