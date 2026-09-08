from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas

from app.services.project_service import ( 
    get_project_for_owner

)

def create_task(
    db: Session,
    project_id: int,
    task_data: schemas.TaskCreate,
    user_id: int
) -> models.Task:

    get_project_for_owner(
        db=db,
        project_id=project_id,
        user_id=user_id
    )

    if task_data.assignee_id is not None:
        assignee = db.get(
            models.User,
            task_data.assignee_id
        )

        if assignee is None:
            if assignee is None:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignee not found"
            )

    task = models.Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status="todo",
        project_id=project_id,
        assignee_id=task_data.assignee_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task