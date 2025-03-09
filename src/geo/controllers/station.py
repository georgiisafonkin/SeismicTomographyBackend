from fastapi import APIRouter, Depends
from fastapi import status as http_status
from geo.services import ServiceFactory
from geo.services.di import get_services
from geo.models.schemas.station import StationsRequest
from geo.views.station import StationsResponse
from geo.services import station


station_router = APIRouter(prefix="/stations", tags=["Station"])

@station_router.get(path="", status_code=http_status.HTTP_202_ACCEPTED)
async def get_stations_by_coordinates(
        stations_request: StationsRequest,
        services: ServiceFactory = Depends(get_services)
) -> StationsResponse:
    """

    Получение станций указанной сети из определённой области 
    
    """
    return StationsResponse(content= await services.station.fetch_area_stations(station_request=stations_request))
    