from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from app.services import project_service
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user
from typing import Annotated,Literal
from app.services.task_service import list_project_tasks
router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)






@router.post(
    "",
    response_model=schemas.ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        get_current_user
    )
):

    return project_service.create_project(
        db=db,
        project_data=project,
        owner=current_user
    )



   
@router.get(
    "/{project_id}",
    response_model=schemas.ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.get(
        models.Project,
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project



@router.patch("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id:int,
    project_update:schemas.ProjectUpdate,
    db:Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
                   ):
    project = db.get(models.Project,project_id)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not Found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to modify this project")

    update_data = project_update.model_dump(exclude_unset=True)

    for field,value in update_data.items():
        setattr(project,field,value)

    db.commit()
    db.refresh(project)
    return project



@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        get_current_user
    )
):
    project = db.get(
        models.Project,
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this project"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }


@router.post(
    "/projects/{project_id}/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    project_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user:models.User = Depends(get_current_user)
):
    project = db.get(
        models.Project,
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project.owner_id != current_user.id:
        raise HTTPException(
        status_code=403,
        detail="You cannot create tasks in this project"
    )
    

    if task.assignee_id is not None:
        assignee = db.get(
            models.User,
            task.assignee_id
        )

        if assignee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignee not found"
            )

    db_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status="todo",
        project_id=project_id,
        assignee_id=task.assignee_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@router.get(
    "/projects/{project_id}/tasks",
    response_model=schemas.TaskPageResponse
)
def get_project_tasks(
    project_id: int,

    status_filter: Annotated[
        Literal[
            "todo",
           "in_progress",
            "done"
        ] | None,
        Query(alias="status")
    ] = None,

    priority: Annotated[
        Literal[
            "low",
            "medium",
            "high"
        ] | None,
        Query()
    ] = None,

    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=100
        )
    ] = None,

    sort_by: Annotated[
        Literal[
            "id",
            "title"
        ],
        Query()
    ] = "id",

    sort_order: Annotated[
        Literal[
            "asc",
            "desc"
        ],
        Query()
    ] = "asc",

    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100
        )
    ] = 20,

    offset: Annotated[
        int,
        Query(ge=0)
    ] = 0,

    db: Session = Depends(get_db),

    current_user: models.User = Depends(
        get_current_user
    ),
):
    return list_project_tasks(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        status_filter=status_filter,
        priority=priority,
        search=search,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )