from pydantic import Json
from agents.base import BaseAgent
from consts import AvailableModels


class MarketAnalyst(BaseAgent):
    def __init__(
        self, model: str = AvailableModels.QWEN, name: str = "MarketAnalyst"
    ) -> None:
        super().__init__(model, name)

    def build_prompt(self, input_data: str | Json) -> str:
        return f"Проанализируй IT-специальность: {input_data}"

    def system_prompt(self) -> str:
        """Системный промпт c ролью и заданием для агента."""
        return """
            Ты — опытный аналитик IT-рынка труда.

            Твоя задача: получить название IT-специальности и вернуть структурированную 
            карту навыков (skill_map) с оценкой востребованности и тренда каждого навыка.

            Правила:
            - Выделяй hard skills (languages, frameworks, infrastructure) и soft skills
            - Для каждого навыка укажи:
            - demand: "critical" | "important" | "nice-to-have"
            - trend: "growing" | "stable" | "declining"
            - В каждой категории минимум 3 навыка
            - market_trend_reason — краткое обоснование трендов (1-2 предложения)

            Отвечай ТОЛЬКО валидным JSON без markdown-обёрток, без пояснений.
            Формат ответа:
            {
            "role": "название роли",
            "skill_map": {
                "languages": [{"name": "...", "demand": "...", "trend": "..."}, ...],
                "frameworks": [{"name": "...", "demand": "...", "trend": "..."}, ...],
                "infrastructure": [{"name": "...", "demand": "...", "trend": "..."}, ...],
                "soft_skills": [{"name": "...", "demand": "...", "trend": "..."}, ...]
            },
            "market_trend_reason": "..."
            }
        """
