from __future__ import annotations

from sqlalchemy import ForeignKey, String, CheckConstraint , UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    is_active:Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    projects: Mapped[list[Project]] = relationship(
        back_populates="owner"
    )

    assigned_tasks: Mapped[list[Task]] = relationship(
        back_populates="assignee"
    )

    memberships: Mapped[list[ProjectMembership]] =  relationship(
        back_populates="user"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    owner: Mapped[User] = relationship(
        back_populates="projects"
    )

    tasks: Mapped[list[Task]] = relationship(
        back_populates="project"
    )
    memberships: Mapped[list[ProjectMembership]] =  relationship(
            back_populates="project"
        )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="todo"
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    project: Mapped[Project] = relationship(
        back_populates="tasks"
    )

    assignee: Mapped[User | None] = relationship(
        back_populates="assigned_tasks"
    )

class ProjectMembership(Base):
    __tablename__ =  "project_memberships"

    __table_args__=(
        UniqueConstraint(
            "project_id","user_id",
            name = "uq_project_membership_project_user",
        ),
        CheckConstraint(
            "role IN('owner','member')",
            name= "ck_project_membership_role",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    project_id:Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )
    user_id:Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index= True
    )
    role: Mapped[str] = mapped_column(String(20),nullable=False)

    project: Mapped[Project] = relationship(
        back_populates="memberships"
    )
    user: Mapped[User] = relationship(
        back_populates="memberships"
    )

