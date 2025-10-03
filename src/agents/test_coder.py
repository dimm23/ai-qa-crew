# src/agents/test_coder.py
from crewai import Agent
from langchain_community.llms import Ollama
from tools.codebase_inspector import CodebaseInspectorTool

llm = Ollama(model="deepseek-coder:6.7b", temperature=0.1)

test_coder = Agent(
    role="Senior QA Automation Engineer",
    goal=(
        "Генерировать автотесты строго в соответствии с архитектурой проекта ai-qa-crew. "
        "Используй существующие PageObject (pages/), модели (models/) и фикстуры (conftest.py). "
        "Не дублируй код — расширяй существующие классы или используй их."
    ),
    backstory=(
        "Ты знаешь структуру репозитория github.com/dimm23/ai-qa-crew. "
        "Ты пишешь код в стиле проекта: для UI — через PageObject, для API — через Pydantic-модели. "
        "Ты избегаешь прямых вызовов driver или requests, если есть обёртки."
    ),
    tools=[CodebaseInspectorTool()],
    verbose=True,
    allow_delegation=False,
    llm=llm
)