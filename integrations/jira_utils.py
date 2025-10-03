import requests
import os
from pathlib import Path

JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

def find_related_story(issue_key: str) -> str:
    # Пример: ищем задачу типа Story в связях
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}?fields=issuelinks"
    resp = requests.get(url, auth=(JIRA_EMAIL, JIRA_TOKEN))
    data = resp.json()
    
    for link in data["fields"]["issuelinks"]:
        if "outwardIssue" in link:
            linked = link["outwardIssue"]
            if linked["fields"]["issuetype"]["name"] == "Story":
                return linked["key"]
    return issue_key  # если нет — работаем с самой задачей

def download_latest_attachment(issue_key: str) -> str | None:
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}?fields=attachment"
    resp = requests.get(url, auth=(JIRA_EMAIL, JIRA_TOKEN))
    attachments = resp.json()["fields"]["attachment"]
    
    if not attachments:
        return None
        
    latest = max(attachments, key=lambda x: x["created"])
    download_url = latest["content"]
    filename = latest["filename"]
    
    out_path = f"temp_attachments/{issue_key}_{filename}"
    Path(out_path).parent.mkdir(exist_ok=True)
    
    with requests.get(download_url, auth=(JIRA_EMAIL, JIRA_TOKEN), stream=True) as r:
        with open(out_path, "wb") as f:
            for chunk in r.iter_content():
                f.write(chunk)
    return out_path

def post_jira_comment(issue_key: str, comment: str):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    requests.post(
        url,
        json={"body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment}]}]}},
        auth=(JIRA_EMAIL, JIRA_TOKEN),
        headers={"Content-Type": "application/json"}
    )