# GitHub Cloud Connector

A production-ready REST API that connects to GitHub's API — built with **FastAPI** and **Python**.
Supports fetching repositories, listing issues, and creating issues — all secured via a GitHub Personal Access Token.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Tech Stack & Why](#tech-stack--why)
- [Prerequisites](#prerequisites)
- [Step 1 — Clone the Repository](#step-1--clone-the-repository)
- [Step 2 — Create a Virtual Environment](#step-2--create-a-virtual-environment)
- [Step 3 — Install Dependencies](#step-3--install-dependencies)
- [Step 4 — Generate a GitHub Personal Access Token](#step-4--generate-a-github-personal-access-token)
- [Step 5 — Configure Environment Variables](#step-5--configure-environment-variables)
- [Step 6 — Run the Server](#step-6--run-the-server)
- [Step 7 — Test the API](#step-7--test-the-api)
- [API Endpoints Reference](#api-endpoints-reference)
- [Error Handling](#error-handling)
- [Security Notes](#security-notes)

---

## Project Structure

```
github-connector/
│
├── main.py                  # App entry point — registers routers, configures FastAPI
├── config.py                # Loads and validates environment variables at startup
├── requirements.txt         # All Python dependencies, pinned to exact versions
│
├── routers/                 # HTTP layer — handles requests/responses only
│   ├── __init__.py
│   ├── repos.py             # GET /repos/{username}
│   └── issues.py            # GET /issues/list  |  POST /issues/create
│
├── services/                # Business logic layer — all GitHub API calls live here
│   ├── __init__.py
│   └── github_service.py    # get_repositories(), list_issues(), create_issue()
│
├── .env                     # ⚠️ Your secrets — NEVER commit this (git-ignored)
├── .env.example             # Safe template — shows required vars without real values
├── .gitignore               # Excludes .env, __pycache__, venv, etc.
└── README.md                # This file
```

**Why this structure?**
Routers only handle HTTP (what comes in, what goes out). Services handle all the GitHub API logic. This separation means you can swap GitHub for GitLab later by only touching `services/` — nothing else changes.

---

## Tech Stack & Why

| Tool | Version | Why |
|------|---------|-----|
| **Python** | 3.11+ | Readable, widely supported, one of two suggested options |
| **FastAPI** | 0.115 | Auto Swagger docs, async support, Pydantic validation built-in |
| **httpx** | 0.27 | Async HTTP client — works natively with FastAPI's async model |
| **python-dotenv** | 1.0 | Loads `.env` file so secrets never touch source code |
| **Pydantic** | 2.9 | Validates request bodies — catches bad input before hitting GitHub |
| **uvicorn** | 0.30 | ASGI server — runs FastAPI in production-grade async mode |

---

## Prerequisites

Before starting, make sure you have these installed on your machine:

- **Python 3.11+** — check with `python --version` or `python3 --version`
- **pip** — comes with Python, check with `pip --version`
- **Git** — check with `git --version`
- A **GitHub account**

---

## Step 1 — Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/YOUR_USERNAME/github-connector.git
cd github-connector
```

> **Where you are now:** Inside the `github-connector/` project folder.
> All commands from here on run from this folder unless stated otherwise.

---

## Step 2 — Create a Virtual Environment

A virtual environment isolates this project's dependencies from the rest of your system.
This prevents version conflicts if you have other Python projects.

```bash
# Create the virtual environment (creates a folder called "venv")
python -m venv venv
```

Now **activate** it:

**On macOS / Linux:**
```bash
source venv/bin/activate
```

**On Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

✅ You'll know it's active when your terminal prompt shows `(venv)` at the start.

To deactivate later (when you're done working):
```bash
deactivate
```

---

## Step 3 — Install Dependencies

With your virtual environment active:

```bash
pip install -r requirements.txt
```

This installs FastAPI, uvicorn, httpx, python-dotenv, and Pydantic — all pinned to exact versions for reproducibility.

Verify the install:
```bash
pip list
```

---

## Step 4 — Generate a GitHub Personal Access Token

Your token authenticates all API requests to GitHub. **Never share it or commit it.**

1. Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token"** → choose **"Generate new token (classic)"**
3. Give it a name, e.g. `github-connector-dev`
4. Set expiration (30 days is fine for assignment; no expiration for long-term use)
5. Under **Scopes**, check:
   - ✅ `repo` — full access to repositories and issues (needed for creating issues)
   - ✅ `read:user` — needed to fetch user info
6. Click **"Generate token"**
7. **Copy the token immediately** — GitHub only shows it once

---

## Step 5 — Configure Environment Variables

In the project folder, copy the example env file:

**On macOS / Linux:**
```bash
cp .env.example .env
```

**On Windows (Command Prompt):**
```bash
copy .env.example .env
```

Now open `.env` in any text editor and fill in your token:

```env
GITHUB_TOKEN=ghp_YourActualTokenHere
GITHUB_API_BASE_URL=https://api.github.com
```

> ⚠️ The `.env` file is already listed in `.gitignore` — it will **never** be committed to Git.
> The `.env.example` file is what gets committed — it shows the structure without secrets.

---

## Step 6 — Run the Server

With your virtual environment active and `.env` configured:

```bash
uvicorn main:app --reload
```

**What this means:**
- `main` → refers to `main.py`
- `app` → the FastAPI instance inside it
- `--reload` → auto-restarts when you edit code (use only in development)

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

The API is now live at **http://localhost:8000**

---

## Step 7 — Test the API

### Option A: Swagger UI (easiest — no extra tools needed)

Open your browser and go to:
```
http://localhost:8000/docs
```

You'll see a full interactive API UI. Click any endpoint → **"Try it out"** → fill in params → **"Execute"**.

### Option B: curl (terminal)

```bash
# Health check
curl http://localhost:8000/

# Fetch repos for a GitHub user
curl http://localhost:8000/repos/torvalds

# List open issues from a repo
curl "http://localhost:8000/issues/list?owner=torvalds&repo=linux&state=open"

# Create an issue (replace with YOUR repo)
curl -X POST http://localhost:8000/issues/create \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "your-github-username",
    "repo": "your-repo-name",
    "title": "Test issue from GitHub Connector",
    "body": "This issue was created via the GitHub Cloud Connector API."
  }'
```

### Option C: Postman

1. Download [Postman](https://www.postman.com/downloads/)
2. Import requests manually or use the Swagger UI's `/openapi.json` to auto-import

---

## API Endpoints Reference

### `GET /`
Health check.

**Response:**
```json
{
  "service": "GitHub Cloud Connector",
  "status": "running",
  "docs": "/docs"
}
```

---

### `GET /repos/{username}`
Fetch all public repositories for a GitHub user.

**Path Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `username` | string | GitHub username or org name |

**Example:**
```
GET /repos/octocat
```

**Response:**
```json
{
  "username": "octocat",
  "count": 8,
  "repositories": [
    {
      "id": 1296269,
      "name": "Hello-World",
      "full_name": "octocat/Hello-World",
      "description": "My first repository on GitHub!",
      "url": "https://github.com/octocat/Hello-World",
      "language": null,
      "stars": 2341,
      "forks": 3049,
      "open_issues": 5,
      "private": false,
      "created_at": "2011-01-26T19:01:12Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

**Errors:**
- `404` — User not found on GitHub

---

### `GET /issues/list`
List issues from a repository (pull requests are excluded).

**Query Parameters:**
| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `owner` | string | ✅ | — | Repo owner (username or org) |
| `repo` | string | ✅ | — | Repository name |
| `state` | string | ❌ | `open` | `open`, `closed`, or `all` |

**Example:**
```
GET /issues/list?owner=octocat&repo=Hello-World&state=open
```

**Response:**
```json
{
  "owner": "octocat",
  "repo": "Hello-World",
  "state": "open",
  "count": 2,
  "issues": [
    {
      "id": 1,
      "number": 42,
      "title": "Found a bug",
      "body": "Steps to reproduce...",
      "state": "open",
      "url": "https://github.com/octocat/Hello-World/issues/42",
      "author": "octocat",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-02T00:00:00Z"
    }
  ]
}
```

**Errors:**
- `400` — Invalid `state` value
- `404` — Repository not found

---

### `POST /issues/create`
Create a new issue in a repository.

> ⚠️ Your GitHub token must have `repo` scope enabled.

**Request Body (JSON):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `owner` | string | ✅ | Repo owner |
| `repo` | string | ✅ | Repository name |
| `title` | string | ✅ | Issue title (cannot be empty) |
| `body` | string | ❌ | Issue description |

**Example:**
```json
POST /issues/create
{
  "owner": "your-username",
  "repo": "your-repo",
  "title": "Bug: Login page crashes on mobile",
  "body": "Steps to reproduce:\n1. Open on mobile\n2. Tap login\n3. App crashes"
}
```

**Response (201 Created):**
```json
{
  "message": "Issue created successfully.",
  "issue": {
    "id": 123456789,
    "number": 1,
    "title": "Bug: Login page crashes on mobile",
    "body": "Steps to reproduce...",
    "state": "open",
    "url": "https://github.com/your-username/your-repo/issues/1",
    "author": "your-username",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

**Errors:**
- `403` — Token lacks `repo` scope
- `404` — Repository not found
- `422` — Validation error (e.g. empty title)

---

## Error Handling

All errors return a consistent JSON structure:

```json
{
  "detail": "Human-readable error message here"
}
```

| HTTP Code | Meaning |
|-----------|---------|
| `400` | Bad request — invalid parameter value |
| `403` | Forbidden — token missing required scope |
| `404` | Not found — user or repo doesn't exist on GitHub |
| `422` | Unprocessable — request body failed validation |
| `500` | Unexpected server error |

---

## Security Notes

- ✅ Token is loaded from `.env` — never hardcoded in source
- ✅ `.env` is in `.gitignore` — never committed to Git
- ✅ `.env.example` is committed — shows required structure without secrets
- ✅ `config.py` fails fast at startup if `GITHUB_TOKEN` is missing
- ✅ All GitHub API errors are caught and returned as clean HTTP responses
- ⚠️ For production: use a secrets manager (AWS Secrets Manager, GitHub Actions Secrets, etc.) instead of `.env`
