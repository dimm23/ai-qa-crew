from crewai import Task
from textwrap import dedent

def code_tests(agent):
    return Task(
        description=dedent("""
            Преобразуй тест-кейсы из output/test_cases_nlp.md в pytest-функции.
            Используй requests. URL: http://host.docker.internal:8000
            Только код, без комментариев.
        """),
        expected_output="Валидный Python-файл с тестами",
        output_file="output/test_api.py",
        agent=agent
    )