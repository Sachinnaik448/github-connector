from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from services import github_service

router = APIRouter(prefix="/issues", tags=["Issues"])


class CreateIssueRequest(BaseModel):
    owner: str = Field(..., description="GitHub username or org that owns the repo")
    repo: str = Field(..., description="Repository name")
    title: str = Field(..., min_length=1, description="Issue title (required)")
    body: str = Field(default="", description="Issue description (optional)")


@router.get("/list", summary="List issues from a repository")
def list_issues(
    owner: str = Query(..., description="GitHub username or org"),
    repo: str = Query(..., description="Repository name"),
    state: str = Query(default="open", description="Issue state: open, closed, all"),
):
    if state not in ("open", "closed", "all"):
        raise HTTPException(status_code=400, detail="state must be 'open', 'closed', or 'all'.")
    try:
        issues = github_service.list_issues(owner, repo, state)
        return {"owner": owner, "repo": repo, "state": state, "count": len(issues), "issues": issues}
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            raise HTTPException(status_code=404, detail=f"Repository '{owner}/{repo}' not found.")
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/create", summary="Create a new issue in a repository", status_code=201)
def create_issue(payload: CreateIssueRequest):
    try:
        issue = github_service.create_issue(
            owner=payload.owner,
            repo=payload.repo,
            title=payload.title,
            body=payload.body,
        )
        return {"message": "Issue created successfully.", "issue": issue}
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            raise HTTPException(status_code=404, detail=f"Repository '{payload.owner}/{payload.repo}' not found.")
        if "403" in error_msg:
            raise HTTPException(status_code=403, detail="Permission denied. Check your token's 'repo' scope.")
        raise HTTPException(status_code=500, detail=error_msg)
