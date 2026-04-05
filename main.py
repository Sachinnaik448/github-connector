from fastapi import FastAPI
from routers import repos, issues

app = FastAPI(
    title="GitHub Cloud Connector",
    description=(
        "A REST API connector for GitHub. Authenticate with a Personal Access Token "
        "and interact with repositories and issues."
    ),
    version="1.0.0",
    contact={"name": "GitHub Connector"},
)

# Register route modules
app.include_router(repos.router)
app.include_router(issues.router)


@app.get("/", tags=["Health"])
def root():
    """Health check — confirms the service is running."""
    return {
        "service": "GitHub Cloud Connector",
        "status": "running",
        "docs": "/docs",
    }
