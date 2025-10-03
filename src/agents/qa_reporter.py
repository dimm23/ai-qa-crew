from crewai import Agent
from langchain_community.llms import Ollama

llm = Ollama(model="deepseek-coder:6.7b", temperature=0.2)

qa_reporter = Agent(
    role="QA Quality Advocate",
    goal="Проанализировать результаты прогона, сгенерировать Allure-отчёт и подготовить данные для публикации в Allure TestOps",
    backstory="Отвечает за прозрачность качества. Готовит отчёты для product owner'ов.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)