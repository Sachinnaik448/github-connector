from fastapi import APIRouter, HTTPException, Query
from services import github_service

router = APIRouter(prefix="/repos", tags=["Repositories"])


@router.get("/{username}", summary="Fetch repositories for a GitHub user")
def get_repositories(
    username: str,
    sort: str = Query(default="updated", description="Sort by: updated, created, pushed, full_name"),
):
    """Returns a list of public repositories for the given GitHub username."""
    if sort not in ("updated", "created", "pushed", "full_name"):
        raise HTTPException(status_code=400, detail="sort must be: updated, created, pushed, or full_name")
    try:
        repos = github_service.get_repositories(username, sort)
        return {"username": username, "count": len(repos), "repositories": repos}
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            raise HTTPException(status_code=404, detail=f"GitHub user '{username}' not found.")
        raise HTTPException(status_code=500, detail=error_msg)
