from .base import BaseView
from geo.models import schemas


class TaskResponse(BaseView):
    content: schemas.Task


class TasksResponse(BaseView):
    content: list[schemas.TaskShort]


class TaskCountResponse(BaseView):
    content: int

class TaskMetadataResponse(BaseView):
    content: schemas.TaskMetadata

class TaskShortResponse(BaseView):
    content: schemas.TaskShort