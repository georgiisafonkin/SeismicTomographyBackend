from fastapi import APIRouter, Depends, Query
from fastapi import status as http_status
from geo.services import ServiceFactory
from geo.services.di import get_services
from geo.models.schemas.station import StationsRequest
from geo.views.station import StationsResponse
from geo.services import station


station_router = APIRouter(prefix="/stations", tags=["Station"])

@station_router.get(path="/", status_code=http_status.HTTP_202_ACCEPTED)
async def get_stations_by_coordinates(
        min_latitude: float = Query(..., alias="min_latitude"),  # Запрашиваем параметры через Query
        max_latitude: float = Query(..., alias="max_latitude"),
        min_longitude: float = Query(..., alias="min_longitude"),
        max_longitude: float = Query(..., alias="max_longitude"),
        network_code: str = Query(..., alias="network_code"),
        services: ServiceFactory = Depends(get_services)
) -> StationsResponse:
    """
    Получение станций указанной сети из определённой области
    """
    stations_request = StationsRequest(
        min_latitude=min_latitude,
        max_latitude=max_latitude,
        min_longitude=min_longitude,
        max_longitude=max_longitude,
        network_code=network_code
    )

    return StationsResponse(content= await services.station.fetch_area_stations(station_request=stations_request))
    