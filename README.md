<a href="https://github.com/Raisin228/ml_agentic_system_analyzer_job_market">
  <img src="https://github.com/Raisin228/ml_agentic_system_analyzer_job_market/blob/main/photos/agent.png" width="80" align="left" style="margin-right: 12px;" />
</a>  



#  Job Market Analyzer — Multi-Agent System

<br clear="left"/>

> Многоагентная система анализа IT-рынка труда на базе локальных LLM (Ollama | qwen2.5:7B).  
> Вводишь название должности — получаешь полный карьерный отчёт: карту навыков, зарплатные вилки, план развития и оценку качества.

---

### Описание

---

Проект представляет собой **пайплайн из 4-х специализированных AI-агентов**, которые последовательно обрабатывают запрос и передают результат друг другу. Каждый агент работает с локальной LLM через Ollama, а ответы валидируются по строгим Pydantic-схемам с помощью Instructor.

***Что умеет система:***  
✅ Анализировать рынок IT-вакансий по заданной специальности.  
✅ Строить карту навыков с оценкой значимости и тренда для каждого скилла.  
✅ Рассчитывать зарплатные вилки по 4 грейдам и 3 регионам (регионы РФ / Москва / удалёнка в USD).  
✅ Генерировать персональный 3-месячный план карьерного развития с ресурсами.  
✅ Автоматически верифицировать и оценивать качество итогового отчёта.  
✅ Сохранять полный результат в `report.json` и генерировать красивый `report.md`.

ℹ️ **Версия v1.0 — модели работают локально, интернет не нужен.**

---

### Оглавление

---

- [Описание](#описание) — задумка и перечень функционала
- [Архитектура агентов](#архитектура-агентов) — описание каждого агента и его роли
- [Стек технологий](#стек-технологий) — инструменты, используемые в проекте
- [Запуск проекта](#запуск-проекта) — инструкция по развёртыванию
- [Структура проекта](#структура-проекта) — дерево файлов и их назначение
- [Пример вывода](#пример-вывода) — что получится после запуска
- [Разработчик @Raisin228](https://github.com/Raisin228)

---

### Архитектура агентов

---

Система работает как **последовательный пайплайн**: каждый агент получает на вход результат предыдущего.

```
[Пользователь: "iOS Developer (Swift)"]
        │
        ▼
┌─────────────────────┐
│  Agent 1            │  MarketAnalyst
│  Аналитик рынка     │──► skill_map (языки, фреймворки, инфра, soft-skills)
│                     │    + оценка значимости и тренда для каждого навыка
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Agent 2            │  SalaryEstimator
│  Оценщик зарплат    │──► salary_table (Junior / Middle / Senior / Lead)
│                     │    × регион (провинция РФ / Москва / удалёнка $)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Agent 3            │  CareerAdvisor
│  Карьерный советник │──► learning_path (3 фазы × 30 дней)
│                     │    + gap_analysis + идея portfolio-проекта
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Agent 4            │  CriticVerifier
│  Критик-верификатор │──► quality_index (0–100) + warnings + is_consistent
│                     │    Проверяет противоречия между отчётами агентов 1-3
└─────────────────────┘
        │
        ▼
  report.json  +  report.md
```

#### 🔎 Agent 1 — MarketAnalyst (Аналитик рынка)

Принимает название IT-специальности и строит **карту навыков**:
- Языки программирования, фреймворки, инфраструктура, soft-skills
- Для каждого навыка: `importance` (critical / important / nice-to-have) и `trend` (growing / stable / declining)
- Кратко объясняет текущие тенденции рынка

#### 💰 Agent 2 — SalaryEstimator (Оценщик зарплат)

На основе skill_map рассчитывает **зарплатные ожидания**:
- Таблица: 4 грейда × 3 региона (min / median / max)
- Москва и регионы РФ — в рублях, международная удалёнка — в USD
- Указывает топ-3/5 работодателей, активно нанимающих специалистов данного профиля

#### 🗺️ Agent 3 — CareerAdvisor (Карьерный советник)

Получает данные от агентов 1 и 2, формирует **персональный план развития**:
- `learning_path`: 3 фазы — Foundation → Practice → Portfolio, каждая с темами и реальными ресурсами (курсы, книги, документация)
- `gap_analysis`: быстрые победы (2–4 недели) и долгосрочные цели (3+ месяца)
- `portfolio_project`: конкретная идея проекта с перечнем технологий

#### 🔍 Agent 4 — CriticVerifier (Критик и верификатор)

Анализирует отчёты агентов 1–3 и **проверяет их на противоречия**:
- Зарплаты соответствуют уровню спроса на навыки?
- Нет ли скиллов с трендом "declining" в плане обучения?
- Технологии portfolio-проекта есть в skill_map?
- Выставляет `quality_index` (0–100) и формирует список `warnings`

---

### Стек технологий

---

| Инструмент | Версия | Назначение |
|---|---|---|
| [Python](https://www.python.org/) | 3.13 | Язык программирования |
| [Ollama](https://ollama.com/) | latest | Локальный сервер для запуска LLM |
| [Qwen 2.5 7B](https://ollama.com/library/qwen2.5) | 7B | Основная языковая модель |
| [DeepSeek R1](https://ollama.com/library/deepseek-r1) | 8B | Альтернативная модель (consts.py) |
| [OpenAI SDK](https://github.com/openai/openai-python) | 2.30.0 | HTTP-клиент для запросов к Ollama |
| [Instructor](https://python.useinstructor.com/) | 1.15.1 | Валидация ответов LLM по Pydantic-схемам |
| [Pydantic](https://docs.pydantic.dev/) | 2.12.5 | Описание схем ответов агентов |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | 1.2.2 | Загрузка переменных окружения |

---

### Запуск проекта

---

#### 1. Установите Ollama и скачайте модель

```bash
# Установка Ollama (macOS)
brew install ollama

# Запустите сервер
ollama serve

# В отдельном терминале — скачайте модель
ollama pull qwen2.5:7b
```

#### 2. Клонируйте репозиторий

```bash
git clone https://github.com/Raisin228/ml_agentic_system_analyzer_job_market.git
cd ml_agentic_system_analyzer_job_market
```

#### 3. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 4. Установите зависимости

```bash
pip install requirements.txt
```

#### 5. Создайте файл `.env` (по аналогии с .env.example)

```bash
# .env
AI_API_KEY=ollama   # по умолчанию уже прописано в коде
```

#### 6. Запустите анализ

```bash
python main.py --role "iOS Developer (Swift)"
```

Замените `"iOS Developer (Swift)"` на любую IT-специальность, например:

```bash
python main.py --role "Backend Python Developer"
python main.py --role "ML Engineer"
python main.py --role "DevOps Engineer"
```

#### 7. Получите результат

После выполнения в директории проекта появятся:
- `report.json` — полный структурированный результат всех агентов
- `report.md` — красивый Markdown-отчёт с таблицами и карьерным планом
- `run.log` — лог выполнения с попытками и сырыми ответами

---

### Структура проекта

---

```
ml_agentic_system_analyzer_job_market/
│
├── agents/
│   ├── base.py                  # BaseAgent: retry-логика, вызов LLM, логирование
│   ├── market_analyst_a1.py     # Agent 1: Аналитик рынка
│   ├── salary_estimator_a2.py   # Agent 2: Оценщик зарплат
│   ├── career_advisor_a3.py     # Agent 3: Карьерный советник
│   └── critic_verifier_a4.py   # Agent 4: Критик-верификатор
│
├── models/
│   ├── market_analyst_resp.py   # Pydantic-схема ответа Agent 1
│   ├── salary_estimator_resp.py # Pydantic-схема ответа Agent 2
│   ├── career_advisor_resp.py   # Pydantic-схема ответа Agent 3
│   └── critic_verifier_resp.py  # Pydantic-схема ответа Agent 4
│
├── consts.py                    # Названия доступных локальных моделей
├── main.py                      # Точка входа, оркестрация агентов
├── report_generator.py          # Генерация report.json и report.md
│
├── report.json                  # Генерируется после запуска
├── report.md                    # Генерируется после запуска
└── run.log                      # Лог выполнения (генерируется после запуска)
```

---

### Пример вывода

---

После запуска `python main.py --role "iOS Developer (Swift)"` в `report.md` вы получите:

**Карта навыков** с цветовой разметкой значимости и трендов:

| Skill | Importance | Trend |
|-------|-----------|-------|
| Swift | 🔴 critical | 📈 growing |
| UIKit | 🔴 critical | ➡️ stable |
| SwiftUI | 🟡 important | 📈 growing |

**Зарплатная таблица** по грейдам и регионам:

| Level | Region (RU) | Moscow | Remote (USD) |
|-------|-------------|--------|--------------|
| **Junior** | 250 000 – 350 000 – 450 000 ₽ | 350 000 – 500 000 – 650 000 ₽ | $12 000 – $18 000 – $25 000 |
| **Senior** | 700 000 – 950 000 – 1 250 000 ₽ | 1 000 000 – 1 300 000 – 1 600 000 ₽ | $35 000 – $45 000 – $55 000 |

**Карьерный план** по 3 фазам (Foundation → Practice → Portfolio) с реальными ресурсами.

**Оценка качества** от Агента-критика: `████████░░ 85/100` с детальным списком предупреждений.

---

*Автор: [@Raisin228](https://github.com/Raisin228)*
