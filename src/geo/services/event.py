from geo.models.schemas.event import EventsByParams
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from geo.repositories.event import EventRepo
from geo.models.schemas.event import EventRequest
from typing import List
from geo.config import logger

class EventApplicationService():
    def __init__(
            self,
            lazy_session: async_sessionmaker[AsyncSession],
    ):
        self._lazy_session = lazy_session


    async def fetch_events(self, event_request: EventRequest) -> List[EventsByParams]:
        async with self._lazy_session() as session:
            event_repo = EventRepo(session=session)
            events = await event_repo.fetch_events_by_params(event_request=event_request)
            r_events = [] # returnable events
            for event in events:
                r_events.append(EventsByParams(id=event.id,
                                                    time=event.time,
                                                    magnitude=event.magnitude,
                                                    latitude=event.latitude,
                                                    longitude=event.longitude,
                                                    depth=event.depth,
                                                    network_code=event.network_code,
                                                    accepted=event.accepted))
        return r_events
        