from crewai import Task
from textwrap import dedent

def design_tests(agent, spec: str):
    return Task(
        description=dedent(f"""
            Проанализируй ТЗ и создай 3–5 тест-кейсов в формате Given-When-Then.
            Учти валидные и невалидные сценарии.
            ТЗ: {spec}
        """),
        expected_output="Markdown-файл с тест-кейсами",
        output_file="output/test_cases_nlp.md",
        agent=agent
    )