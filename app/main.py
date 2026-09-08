from fastapi import FastAPI

from app.routers import (
    auth,
    projects,
    tasks,
    users,
)


app = FastAPI(
    title="IssueFlow API"
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {
        "message": "IssueFlow API is running"
    }