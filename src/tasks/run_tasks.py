from crewai import Task
from textwrap import dedent
import subprocess
import os

def run_tests(agent):
    return Task(
        description=dedent("Создай Dockerfile, собери образ и запусти тесты с сохранением результатов в Allure"),
        expected_output="Результаты в output/allure-results",
        agent=agent,
        callback=_execute_docker
    )

def _execute_docker(output):
    os.makedirs("output/allure-results", exist_ok=True)
    dockerfile = """
FROM python:3.11-slim
WORKDIR /app
COPY test_api.py .
RUN pip install pytest requests allure-pytest
CMD ["pytest", "test_api.py", "--alluredir=./allure-results"]
"""
    with open("output/Dockerfile", "w") as f:
        f.write(dockerfile)
    subprocess.run(["docker", "build", "-t", "ai-qa-test", "-f", "output/Dockerfile", "output/"], check=True)
    subprocess.run([
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}/output/allure-results:/app/allure-results",
        "ai-qa-test"
    ], check=False)
    return "Тесты выполнены"