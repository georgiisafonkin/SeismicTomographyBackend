from fastapi import APIRouter, Depends, Query
from fastapi import status as http_status
from geo.services import ServiceFactory
from geo.services.di import get_services
from geo.views.event import EventByCoordinatesResponse
from geo.models.schemas.event import EventRequest
from typing import List
from datetime import datetime

event_router = APIRouter(prefix="/events", tags=["Event"])

@event_router.get(path="/", status_code=http_status.HTTP_202_ACCEPTED)
async def get_events_by_params(
        start_time: datetime = Query(..., alias="start_time"), # Запрашиваем параметры через Query
        end_time: datetime = Query(..., alias="end_time"),
        min_latitude: float = Query(..., alias="min_latitude"),
        max_latitude: float = Query(..., alias="max_latitude"),
        min_longitude: float = Query(..., alias="min_longitude"),
        max_longitude: float = Query(..., alias="max_longitude"),
        min_depth: float = Query(..., alias="min_depth"),
        max_depth: float = Query(..., alias="max_depth"),
        network_code: str = Query(..., alias="network_code"),
        services: ServiceFactory = Depends(get_services)
) -> EventByCoordinatesResponse:
    """
    Получение событий указанной сети с указанными параметрами

    """
    event_request = EventRequest(
        start_time=start_time,
        end_time=end_time,
        min_latitude=min_latitude,
        max_latitude=max_latitude,
        min_longitude=min_longitude,
        max_longitude=max_longitude,
        min_depth=min_depth,
        max_depth=max_depth,
        network_code=network_code
    )

    return EventByCoordinatesResponse(content= await services.event.fetch_events(event_request=event_request))