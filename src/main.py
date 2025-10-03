import os
import shutil
from pathlib import Path
from crewai import Crew
from src.agents.test_designer import test_designer
from src.agents.test_coder import test_coder
from src.agents.test_runner import test_runner
from src.agents.qa_reporter import qa_reporter
from src.tasks.design_tasks import design_tests
from src.tasks.code_tasks import code_tests
from src.tasks.run_tasks import run_tests
from src.tasks.report_tasks import report_tasks


def run_qa_pipeline(spec_file: str, issue_key: str) -> str:
    """
    Запускает полный AI QA pipeline для заданного ТЗ.
    
    Args:
        spec_file (str): Путь к файлу с описанием требований (текст/ТЗ)
        issue_key (str): Идентификатор задачи (например, QA-123)
    
    Returns:
        str: URL к сгенерированному Allure-отчёту
    """
    # Создаём изолированную папку для задачи
    output_dir = Path(f"output/{issue_key}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Копируем ТЗ в рабочую папку (для прозрачности)
    spec_dest = output_dir / "spec.txt"
    shutil.copy(spec_file, spec_dest)

    # Читаем ТЗ
    with open(spec_dest, "r", encoding="utf-8") as f:
        spec = f.read()

    # Настраиваем пути для задач
    test_cases_path = str(output_dir / "test_cases_nlp.md")
    test_code_path = str(output_dir / "test_api.py")
    dockerfile_path = str(output_dir / "Dockerfile")
    allure_results_path = str(output_dir / "allure-results")
    allure_report_path = str(output_dir / "allure-report")

    # Создаём задачи с динамическими путями
    tasks = [
        design_tests(test_designer, spec, output_file=test_cases_path),
        code_tests(test_coder, input_file=test_cases_path, output_file=test_code_path),
        run_tests(
            test_runner,
            test_file=test_code_path,
            dockerfile_path=dockerfile_path,
            allure_results_path=allure_results_path
        ),
        report_tasks(
            qa_reporter,
            allure_results_path=allure_results_path,
            allure_report_path=allure_report_path
        )
    ]

    # Запуск мультиагентную AI команду
    crew = Crew(
        agents=[test_designer, test_coder, test_runner, qa_reporter],
        tasks=tasks,
        verbose=2
    )

    crew.kickoff()

    # Возвращаем URL отчёта (можно заменить на реальный хост)
    report_url = f"http://localhost:8080/allure/{issue_key}/index.html"
    print(f"\n✅ Pipeline для {issue_key} завершён!")
    print(f"📁 Артефакты: {output_dir.absolute()}")
    print(f"🔗 Отчёт: {report_url}")

    return report_url


# Для запуска вручную (например, для тестирования)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Использование: python main.py <путь_к_ТЗ.txt> <ключ_задачи>")
        sys.exit(1)

    spec_path = sys.argv[1]
    task_key = sys.argv[2]

    if not os.path.isfile(spec_path):
        print(f"Ошибка: файл {spec_path} не найден")
        sys.exit(1)

    run_qa_pipeline(spec_path, task_key)