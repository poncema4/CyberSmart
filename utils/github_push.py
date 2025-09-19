import requests
import base64
import os

GITHUB_REPO = "poncema4/CyberSmart"

def push_to_github(file_path: str, commit_message: str | None = None, branch: str = "main") -> None:
    """
    Push password repo and feedback comments to Github repo
    """
    if commit_message is None:
        if file_path.endswith("password_report.txt"):
            commit_message = "Updated password report for CyberSmart!"
        elif file_path.endswith("feedback.txt"):
            commit_message = "Updated user feedback for CyberSmart!"
        else:
            commit_message = "Updated file for CyberSmart!"

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("No Github token was found in the environment")
        return

    headers = {"Authorization": f"token {token}"}

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    content_bytes = content.encode("utf-8")
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sha = r.json()["sha"]
    elif r.status_code == 404:
        sha = None
    else:
        raise Exception(f"Failed to get file info from Github: {r.json()}")

    payload = {
        "message": commit_message,
        "content": content_b64,
        "branch": branch
    }

    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=headers, json=payload)
    if r.status_code in [200, 201]:
        print("File pushed to GitHub successfully!")
    else:
        print("Failed to push:", r.json())