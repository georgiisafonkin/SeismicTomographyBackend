from geo.models.schemas.event import EventsByCoordinates
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


    async def fetch_area_events(self, event_request: EventRequest) -> List[EventsByCoordinates]:
        async with self._lazy_session() as session:
            event_repo = EventRepo(session=session)
            events = await event_repo.fetch_events_by_network(event_request=event_request)
            area_events = []
            for event in events:
                if event_request.min_latitude <= event.latitude <= event_request.max_latitude and \
                    event_request.min_longitude <= event.longitude <= event_request.max_longitude:
                    area_events.append(EventsByCoordinates(id=event.id,
                                                                   event_time=event.event_time,
                                                                   magnitude=event.magnitude,
                                                                   latitude=event.latitude,
                                                                   longitude=event.longitude,
                                                                   depth=event.depth,
                                                                   network_code=event.network_code,
                                                                   accepted=event.accepted))
        return area_events
        