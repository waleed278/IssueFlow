from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas

from app.services.project_service import ( 
    get_project_for_owner

)

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload



def list_project_tasks(
    db: Session,
    project_id: int,
    user_id: int,
    status_filter: str | None,
    priority: str | None,
    search: str | None,
    limit: int,
    offset: int,
    sort_by: str,
    sort_order: str,
):
    get_project_for_owner(
        db=db,
        project_id=project_id,
        user_id=user_id
    )

    filters = [
        models.Task.project_id == project_id
    ]

    if status_filter is not None:
        filters.append(
            models.Task.status
            == status_filter
        )

    if priority is not None:
        filters.append(
            models.Task.priority
            == priority
        )

    if search is not None:
        filters.append(
            models.Task.title.ilike(
                f"%{search}%"
            )
        )

    sort_columns = {
        "id": models.Task.id,
        "title": models.Task.title,
    }

    sort_column = sort_columns[
        sort_by
    ]

    if sort_order == "desc":
        ordering = sort_column.desc()
    else:
        ordering = sort_column.asc()

    statement = (
        select(models.Task)
        .where(*filters)
        .order_by(
            ordering,
            models.Task.id.asc()
        )
        .offset(offset)
        .limit(limit)
    )

    items = db.scalars(
        statement
    ).all()

    count_statement = (
        select(func.count())
        .select_from(models.Task)
        .where(*filters)
    )

    total = (
        db.scalar(count_statement)
        or 0
    )

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


    
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