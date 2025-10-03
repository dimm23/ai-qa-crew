# src/tasks/code_tasks.py
from crewai import Task
from textwrap import dedent

def code_tests(agent, input_file: str, output_file: str):
    return Task(
        description=dedent(f"""
            1. Проанализируй ТЗ из {input_file}.
            2. Определи: это UI-тест или API-тест?
            3. Используй инструмент CodebaseInspector, чтобы:
               - найти релевантные PageObject (если UI)
               - найти модели и фикстуры (если API)
            4. Сгенерируй тест в соответствии с архитектурой проекта.
            5. Если нужен новый PageObject — предложи его структуру отдельно.
        """),
        expected_output=dedent("""
            Два блока:
            ### Сгенерированный тест
            ```python
            ... 
            ```

            ### Рекомендации по интеграции
            - Если нужно создать новый PageObject: укажи путь и методы
            - Если нужно обновить модель: опиши изменения
        """),
        output_file=output_file,
        agent=agent
    )