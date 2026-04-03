"""Аналитик рынка. Атрошенко Б. С."""

from agents.base import BaseAgent
from models.market_analyst_resp import MarketAnalizerResponse


class MarketAnalyst(BaseAgent):
    def __init__(self) -> None:
        """Инициализатор."""
        super().__init__(MarketAnalizerResponse, name="MarketAnalyst")

    def build_prompt(self, input_data: str) -> str:
        """
        Пользовательский промпт.

        :param input_data: строка с названием it специальности.
        """
        return f"Analyze the IT specialization: {input_data}"

    def system_prompt(self) -> str:
        """Системный промпт c ролью и заданием для агента."""
        return """
            You are an experienced IT labor market analyst.

            Your task: receive an IT specialization name and return a structured
            skill map (skill_map) with demand and trend assessment for each skill.

            Rules:
            - Identify hard skills (languages, frameworks, infrastructure) and soft skills
            - For each skill specify:
            - demand: "critical" | "important" | "nice-to-have"
            - trend: "growing" | "stable" | "declining"
            - At least 3 skills per category
            - market_trend_reason — brief explanation of the trends (1-2 sentences)

            Reply with ONLY valid JSON, no markdown wrappers, no explanations.
            Response format:
            {
            "role": "role name",
            "skill_map": {
                "languages": [{"name": "...", "importance": "...", "trend": "..."}, ...],
                "frameworks": [{"name": "...", "importance": "...", "trend": "..."}, ...],
                "infrastructure": [{"name": "...", "importance": "...", "trend": "..."}, ...],
                "soft_skills": [{"name": "...", "importance": "...", "trend": "..."}, ...]
            },
            "market_trend_reason": "..."
            }
        """
