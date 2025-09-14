import requests
import base64
import os

GITHUB_REPO = "poncema4/CyberSmart"
FILE_PATH = "password_report.txt"

def push_to_github(file_path, commit_message="Updated password report from CyberSmart!", branch="main"):
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}

    # Read the file contents
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    content_bytes = content.encode("utf-8")
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")

    # Get SHA of the existing file
    url_get = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    r = requests.get(url_get, headers=headers)
    if r.status_code == 200:
        sha = r.json()["sha"]
        # File does not exist yet
    elif r.status_code == 404:
        sha = None
    else:
        raise Exception(f"Failed to get file info from Github: {r.json()}")

    # Prepare payload
    payload = {
        "message": commit_message,
        "content": content_b64,
        "branch": branch
    }
    if sha:
        payload["sha"] = sha

    # Push the file
    r = requests.put(url_get, headers=headers, json=payload)
    if r.status_code in [200, 201]:
        print("File pushed to GitHub successfully!")
    else:
        print("Failed to push:", r.json())