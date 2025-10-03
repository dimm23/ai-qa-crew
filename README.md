# 🤖 AI QA Crew — Мультиагентная система автономного тестирования

> **End-to-end AI-driven QA pipeline**: от ТЗ до Allure-отчёта — без участия человека.  
> Локально. Без облака. На open-source LLM.

## 💡 Концепция
Система состоит из 4 специализированных AI-агентов:
1. **Test Designer** — генерирует тест-кейсы в формате Given-When-Then
2. **Test Coder** — преобразует их в pytest-код
3. **Test Runner** — собирает Docker-образ и запускает тесты
4. **QA Reporter** — генерирует Allure-отчёт

Все агенты работают на **локальной open-source модели** через Ollama.

## 🛠️ Технологии
- **LLM**: `deepseek-coder:6.7b` (Ollama)
- **Фреймворк**: CrewAI + LangChain
- **Тесты**: pytest + requests
- **Контейнеризация**: Docker
- **Отчётность**: Allure

## ▶️ Запуск

1. Установи [Ollama](https://ollama.com/)
2. Загрузи модель:
   ```bash
   ollama pull deepseek-coder:6.7b