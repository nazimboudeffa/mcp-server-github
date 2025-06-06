from mcp.server.fastmcp import FastMCP
import requests
import pandas as pd

# Create an MCP
mcp = FastMCP("GitHub")

# Define the API endpoint
base_url = "https://api.github.com/"

@mcp.tool()
async def get_issue_from_repo(owner, repo, issue_number):
    """
    Get issue details from a GitHub repository.
    Parameters:
    - owner: The owner of the repository.
    - repo: The name of the repository.
    - issue_number: The number of the issue to retrieve.
    Returns:
    - A dictionary containing issue details.
    """
    url = f"{base_url}repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(url)
    if response.status_code != 200:
        raise requests.HTTPError(f"Error: {response.status_code} - {response.text}")

    data = response.json()
    return {
        "issue_number": data.get("number"),
        "title": data.get("title"),
        "body": data.get("body"),
        "state": data.get("state"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "user": data.get("user", {}).get("login")
    }

@mcp.tool()
async def get_comments_from_issue(owner, repo, issue_number):
    """
    Get comments from a specific issue in a GitHub repository.
    Parameters:
    - owner: The owner of the repository.
    - repo: The name of the repository.
    - issue_number: The number of the issue to retrieve comments from.
    Returns:
    - A list of dictionaries containing comment details.
    """
    url = f"{base_url}repos/{owner}/{repo}/issues/{issue_number}/comments"
    response = requests.get(url)
    if response.status_code != 200:
        raise requests.HTTPError(f"Error: {response.status_code} - {response.text}")

    data = response.json()
    return [
        {
            "comment_id": comment.get("id"),
            "body": comment.get("body"),
            "user": comment.get("user", {}).get("login"),
            "created_at": comment.get("created_at"),
            "updated_at": comment.get("updated_at")
        } for comment in data
    ]   