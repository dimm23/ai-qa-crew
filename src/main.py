import os
from crewai import Crew
from src.agents.test_designer import test_designer
from src.agents.test_coder import test_coder
from src.agents.test_runner import test_runner
from src.agents.qa_reporter import qa_reporter
from src.tasks.design_tasks import design_tests
from src.tasks.code_tasks import code_tests
from src.tasks.run_tasks import run_tests
from src.tasks.report_tasks import report_results

def main():
    with open("../api_spec.txt", "r", encoding="utf-8") as f:
        spec = f.read()

    crew = Crew(
        agents=[test_designer, test_coder, test_runner, qa_reporter],
        tasks=[
            design_tests(test_designer, spec),
            code_tests(test_coder),
            run_tests(test_runner),
            report_results(qa_reporter)
        ],
        verbose=2
    )

    result = crew.kickoff()
    print("\n✅ AI QA Pipeline завершён!")
    print("📁 Результаты:")
    print("   - Тест-кейсы: output/test_cases_nlp.md")
    print("   - Автотесты:  output/test_api.py")
    print("   - Отчёт:      output/allure-report/index.html")

if __name__ == "__main__":
    main()