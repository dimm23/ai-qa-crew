from fastapi import FastAPI, Request
import requests
import os
from pathlib import Path
from extract_text import extract_text_from_file  
from run_qa_crew import run_qa_pipeline          # main.py как функция
import sys

sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI()

JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

@app.post("/webhook/jira")
async def jira_webhook(request: Request):
    payload = await request.json()
    
    # Проверка события
    issue = payload.get("issue")
    changelog = payload.get("changelog")
    
    if not issue or not changelog:
        return {"status": "ignored"}

    # Проверяем: статус → "Ready for Test" и есть лейбл "AI-QA"
    to_status = None
    for item in changelog.get("items", []):
        if item["field"] == "status":
            to_status = item["toString"]
    
    labels = issue["fields"].get("labels", [])
    
    if to_status == "Ready for Test" and "AI-QA" in labels:
        issue_key = issue["key"]
        print(f"🚀 Запуск AI QA для задачи {issue_key}")
        
        # Шаг 2.1: Найти вложение в связанной задаче (Story)
        story_key = find_related_story(issue_key)
        attachment_path = download_latest_attachment(story_key)
        
        if not attachment_path:
            post_jira_comment(issue_key, "❌ Не найдено вложение с ТЗ.")
            return {"status": "no attachment"}

        # Шаг 2.2: Извлечь текст
        spec_text = extract_text_from_file(attachment_path)
        spec_file = f"temp_specs/{issue_key}_spec.txt"
        Path(spec_file).parent.mkdir(exist_ok=True)
        with open(spec_file, "w") as f:
            f.write(spec_text)

        # Шаг 2.3: Запустить твой AI QA Crew
        report_url = run_qa_pipeline(spec_file, issue_key)

        # Шаг 2.4: Отправить результат в Jira
        post_jira_comment(issue_key, f"✅ AI QA завершён!\nAllure-отчёт: {report_url}")

    return {"status": "processed"}