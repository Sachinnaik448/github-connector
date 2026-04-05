import httpx
from config import GITHUB_TOKEN, GITHUB_API_BASE_URL

# Reusable headers sent with every GitHub API request
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def _build_url(path: str, params: dict = None) -> str:
    """Build a full URL with query parameters."""
    url = f"{GITHUB_API_BASE_URL}{path}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"
    return url


def get_repositories(username: str, sort: str = "updated") -> list[dict]:
    """Fetch all public repositories for a given GitHub username."""
    url = _build_url(f"/users/{username}/repos", {"sort": sort, "per_page": "100"})
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        response.raise_for_status()
        repos = response.json()
        return [
            {
                "id": r["id"],
                "name": r["name"],
                "full_name": r["full_name"],
                "description": r["description"],
                "url": r["html_url"],
                "language": r["language"],
                "stars": r["stargazers_count"],
                "forks": r["forks_count"],
                "open_issues": r["open_issues_count"],
                "private": r["private"],
                "created_at": r["created_at"],
                "updated_at": r["updated_at"],
            }
            for r in repos
        ]


def list_issues(owner: str, repo: str, state: str = "open") -> list[dict]:
    """List issues from a repository. State can be 'open', 'closed', or 'all'."""
    url = _build_url(f"/repos/{owner}/{repo}/issues", {"state": state, "per_page": "100"})
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        response.raise_for_status()
        issues = response.json()
        return [
            {
                "id": i["id"],
                "number": i["number"],
                "title": i["title"],
                "body": i["body"],
                "state": i["state"],
                "url": i["html_url"],
                "author": i["user"]["login"],
                "created_at": i["created_at"],
                "updated_at": i["updated_at"],
            }
            for i in issues
            if "pull_request" not in i
        ]


def create_issue(owner: str, repo: str, title: str, body: str = "") -> dict:
    """Create a new issue in a repository."""
    url = _build_url(f"/repos/{owner}/{repo}/issues")
    payload = {"title": title, "body": body}
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        i = response.json()
        return {
            "id": i["id"],
            "number": i["number"],
            "title": i["title"],
            "body": i["body"],
            "state": i["state"],
            "url": i["html_url"],
            "author": i["user"]["login"],
            "created_at": i["created_at"],
        }
