from fastapi import APIRouter, Depends, Query
from fastapi import status as http_status
from geo.services import ServiceFactory
from geo.services.di import get_services
from geo.views.event import EventByCoordinatesResponse
from geo.models.schemas.event import EventRequest
from typing import List

event_router = APIRouter(prefix="/events", tags=["Event"])

@event_router.get(path="/", status_code=http_status.HTTP_202_ACCEPTED)
async def get_events_by_coordinates(
        min_latitude: float = Query(..., alias="min_latitude"),  # Запрашиваем параметры через Query
        max_latitude: float = Query(..., alias="max_latitude"),
        min_longitude: float = Query(..., alias="min_longitude"),
        max_longitude: float = Query(..., alias="max_longitude"),
        network_code: str = Query(..., alias="network_code"),
        services: ServiceFactory = Depends(get_services)
) -> EventByCoordinatesResponse:
    """
    Получение событий указанной сети из определённой области
    """
    event_request = EventRequest(
        min_latitude=min_latitude,
        max_latitude=max_latitude,
        min_longitude=min_longitude,
        max_longitude=max_longitude,
        network_code=network_code
    )

    return EventByCoordinatesResponse(content= await services.event.fetch_area_events(event_request=event_request))