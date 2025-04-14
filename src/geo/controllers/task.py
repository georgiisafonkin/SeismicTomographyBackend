from fastapi import APIRouter, Depends
from fastapi import status as http_status

from geo.models.schemas import TaskID, TaskMetadata
from geo.services import ServiceFactory
from geo.services.di import get_services

from geo.views.task import TasksResponse, TaskResponse, TaskCountResponse, TaskMetadataResponse, TaskShortResponse
task_router = APIRouter(prefix="/task", tags=["Task"])


@task_router.get("", response_model=TasksResponse, status_code=http_status.HTTP_200_OK)
async def task_list(
        page: int = 1,
        per_page: int = 10,
        services: ServiceFactory = Depends(get_services)
):
    """
    Получить список задач

    """
    return TasksResponse(content=await services.task.list(page, per_page))


@task_router.get("/count", response_model=TaskCountResponse, status_code=http_status.HTTP_200_OK)
async def task_count(services: ServiceFactory = Depends(get_services)):
    """
    Получить количество задач

    """
    return TaskCountResponse(content=await services.task.count())


@task_router.get("/{task_id}", response_model=TaskShortResponse, status_code=http_status.HTTP_200_OK)
async def task(task_id: TaskID, services: ServiceFactory = Depends(get_services)):
    """
    Получить задачу по id

    """
    return TaskShortResponse(content=await services.task.get_task(task_id))


@task_router.post("", response_model=TaskShortResponse, status_code=http_status.HTTP_200_OK)
async def new_task(services: ServiceFactory = Depends(get_services)):
    """
    Создать новую задачу

    """
    return TaskShortResponse(content=await services.task.new_task())


@task_router.delete("/{task_id}", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: TaskID, services: ServiceFactory = Depends(get_services)):
    """
    Удалить задачу по id

    """
    await services.task.delete_task(task_id)

@task_router.post("/{task_id}/metadata", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_task_metadata(task_id: TaskID, task_metadata: TaskMetadata, services: ServiceFactory = Depends(get_services)):
    """
    Обновить сейсданные, данные о станциях и событиях на определённой задаче

    """
    
    await services.task.update_metadata(task_id=task_id, task_metadata=task_metadata)

@task_router.get("/{task_id}/metadata", response_model=TaskMetadataResponse, status_code=http_status.HTTP_200_OK)
async def get_task_metadata(task_id: TaskID, services: ServiceFactory = Depends(get_services)) -> TaskMetadataResponse:
    return TaskMetadataResponse(content= await services.task.get_task_metadata(task_id=task_id))