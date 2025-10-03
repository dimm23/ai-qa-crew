# tools/codebase_inspector.py
from langchain.tools import BaseTool
from pathlib import Path
import os

class CodebaseInspectorTool(BaseTool):
    name = "CodebaseInspector"
    description = (
        "Анализирует структуру проекта ai-qa-crew и возвращает содержимое релевантных файлов: "
        "PageObject (pages/), API-модели (models/), фикстуры (conftest.py). "
        "Запрос должен быть на русском: например, 'покажи PageObject для логина' или 'есть ли модель User?'"
    )

    def _run(self, query: str) -> str:
        repo_root = Path("src")  # предполагаем, что запуск из корня проекта

        # Определяем тип запроса
        query_lower = query.lower()
        results = []

        if "pageobject" in query_lower or "страниц" in query_lower or "ui" in query_lower:
            pages_dir = repo_root / "pages"
            if pages_dir.exists():
                for py_file in pages_dir.glob("*.py"):
                    content = py_file.read_text(encoding="utf-8")
                    results.append(f"### {py_file.name}\n```python\n{content}\n```")
            else:
                results.append("Папка pages/ не найдена.")

        if "модель" in query_lower or "dto" in query_lower or "api" in query_lower:
            models_dir = repo_root / "models"
            if models_dir.exists():
                for py_file in models_dir.glob("*.py"):
                    content = py_file.read_text(encoding="utf-8")
                    results.append(f"### {py_file.name}\n```python\n{content}\n```")
            else:
                results.append("Папка models/ не найдена.")

        if "фикстур" in query_lower or "conftest" in query_lower:
            conftest = repo_root / "conftest.py"
            if conftest.exists():
                content = conftest.read_text(encoding="utf-8")
                results.append(f"### conftest.py\n```python\n{content}\n```")
            else:
                results.append("Файл conftest.py не найден.")

        if not results:
            return "Не удалось найти релевантные файлы по запросу."

        return "\n\n".join(results)

    async def _arun(self, query: str):
        raise NotImplementedError("Async not supported")