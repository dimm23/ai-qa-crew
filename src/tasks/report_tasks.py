from crewai import Task
from textwrap import dedent
import subprocess

def report_results(agent):
    return Task(
        description=dedent("Сгенерируй Allure-отчёт и подготовь манифест для TestOps"),
        expected_output="HTML-отчёт и JSON-манифест",
        agent=agent,
        callback=_generate_allure_report
    )

def _generate_allure_report(output):
    try:
        subprocess.run(["allure", "generate", "output/allure-results", "-o", "output/allure-report", "--clean"], check=True)
        with open("output/testops_manifest.json", "w") as f:
            f.write('{"status": "ready_for_testops_upload"}')
        return "Отчёт сгенерирован"
    except Exception as e:
        return f"Ошибка: {e}"