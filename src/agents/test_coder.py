from crewai import Agent
from langchain_community.llms import Ollama

llm = Ollama(model="deepseek-coder:6.7b", temperature=0.1)

test_coder = Agent(
    role="Senior QA Automation Engineer",
    goal="Преобразовать NLP-тест-кейсы в рабочий pytest-код на Python с использованием requests",
    backstory="Автоматизатор с опытом в Python, Java, Kotlin. Пишет чистый, поддерживаемый код.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)