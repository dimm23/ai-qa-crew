from crewai import Agent
from langchain_community.llms import Ollama

llm = Ollama(model="deepseek-coder:6.7b", temperature=0.2)

test_runner = Agent(
    role="DevOps QA Engineer",
    goal="Создать Dockerfile, собрать образ и запустить автотесты, сохранив результаты в формате Allure",
    backstory="Инженер, отвечающий за CI/CD и стабильность тестовых окружений.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)