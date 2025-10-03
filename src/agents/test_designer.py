from crewai import Agent
from langchain_community.llms import Ollama

llm = Ollama(model="deepseek-coder:6.7b", temperature=0.3)

test_designer = Agent(
    role="Senior QA Analyst",
    goal="Создать структурированные тест-кейсы в формате Given-When-Then на основе ТЗ, применяя методы тест-дизайна",
    backstory="Опытный QA-аналитик с 10+ годами в нефтехимии и финтехе. Умеет выявлять скрытые требования.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)