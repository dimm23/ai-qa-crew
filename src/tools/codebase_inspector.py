from langchain.tools import BaseTool
import os
from pathlib import Path

class CodebaseInspectorTool(BaseTool):
    name = "Codebase Inspector"
    description = "Анализирует структуру репозитория и извлекает содержимое файлов по пути."

    def _run(self, query: str) -> str:
        # query может быть: "page objects for login", "API models for user"
        repo_path = Path("repos/ai-qa-crew")
        
        if "page object" in query.lower():
            po_files = list(repo_path.rglob("pages/*.py"))
            return "\n\n---\n".join(f"### {f.relative_to(repo_path)}\n{f.read_text()}" for f in po_files[:3])
        
        if "api model" in query.lower():
            model_files = list(repo_path.rglob("models/*.py"))
            return "\n\n---\n".join(f"### {f.relative_to(repo_path)}\n{f.read_text()}" for f in model_files[:3])
        
        return "Не найдено релевантных файлов."

    async def _arun(self, query: str):
        raise NotImplementedError("Not supported")