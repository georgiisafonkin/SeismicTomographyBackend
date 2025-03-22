from geo.models import tables
from geo.repositories.base import BaseRepository
from geo.models.schemas.event import Event, EventRequest
from typing import List
import aiohttp

from src.geo.config import logger
class EventRepo(BaseRepository[tables.Event]):
    table = tables.Event

    async def fetch_events_by_network(self, event_request: EventRequest) -> List[Event]:
        url = self.SERVER_URL + self.EVENT
        params = {
            'network_code': event_request.network_code
        }
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as session:
            async with session.get(url, params=params, auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as response:
                result = await response.json()
                logger.info(f"events: {response}")
                return [Event(**st) for st in result]