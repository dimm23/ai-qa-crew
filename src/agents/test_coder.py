from crewai import Agent
from langchain_community.llms import Ollama
from src.tools.codebase_inspector import CodebaseInspectorTool

llm = Ollama(model="deepseek-coder:6.7b", temperature=0.1)

test_coder = Agent(
    role="Senior QA Automation Engineer",
    goal="Генерировать автотесты в соответствии с существующей архитектурой проекта",
    backstory="Знает структуру репозитория ai-qa-crew и следует принятым паттернам.",
    tools=[CodebaseInspectorTool()],
    llm=llm,
    verbose=True
)