from fastapi import APIRouter, Depends
from fastapi import status as http_status
from geo.services import ServiceFactory
from geo.services.di import get_services
from geo.models.schemas import StationsRequest


station_router = APIRouter(prefix="/station", tags=["Station"])

@station_router.get(status_code=http_status.HTTP_202_ACCEPTED)
async def data_proc(
        stations_request: StationsRequest,
        services: ServiceFactory = Depends(get_services)
):
    """

    Получение станций указанной сети из определённой области 
    
    """

    pass
    # await services.station.get_data(stations_request=stations_request)
    