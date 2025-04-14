from .base import BaseView
from geo.models import schemas
from typing import List

class EventsResponse(BaseView):
    content: list[schemas.Event]

class EventByCoordinatesResponse(BaseView):
    content: List[schemas.EventsByParams]