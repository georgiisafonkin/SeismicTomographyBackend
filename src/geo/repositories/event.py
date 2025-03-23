from geo.models import tables
from src.geo.models.tables.event import event_pick_table
from geo.repositories.base import BaseRepository
from geo.models.schemas.event import Event, EventRequest
from sqlalchemy import select, insert

from typing import List
import aiohttp

class EventRepo(BaseRepository[tables.Event]):
    table = tables.Event

    async def fetch_events_by_network(self, event_request: EventRequest) -> List[Event]:
        url = self.SERVER_URL + self.EVENT
        params = {
            'network': event_request.network_code
        }
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as session:
            async with session.get(url, params=params, auth=aiohttp.BasicAuth(self.DB_LOGIN, self.DB_PASSWORD)) as response:
                result = await response.json()
                return [Event(**st) for st in result]

    async def get_picks_ids(self, event_id: int):
        return (await self._session.execute(select(event_pick_table).filter_by(event_id))).scalars().all()

    async def add_event_pick_association(self, event_id: int, pick_id: int, commit: bool = True):
        stmt = insert(event_pick_table).values(event_id=event_id, pick_id=pick_id)
        await self._session.execute(stmt)
        if commit:
            await self._session.commit()