"""Оценщик зарплаты. Атрошенко Б. С."""

from agents.base import BaseAgent
from models.salary_estimator_resp import SalaryExpectations


class SalaryEstimator(BaseAgent):

    def __init__(self):
        """Инициализатор."""
        super().__init__(SalaryExpectations, name="SalaryEstimator")

    def build_prompt(self, input_data: dict) -> str:
        """
        Промпт задание.

        :param input_data: данные от Агента1.
        :return строка с заданием.
        """
        return (
            f"Role: {input_data.get('job_title')} \n"
            f"Skill map (skill_map): {input_data.get('skill_map')} \n"
            f"Estimate salary ranges based on these skills."
        )

    def system_prompt(self) -> str:
        """Системный промпт c ролью и заданием для агента."""
        return """You are an expert in IT industry salaries for both the Russian and international markets.

        Your task: based on the skill map (skill_map), estimate salary ranges
        for the given IT specialization.

        Rules:
        - Build a salary table for 4 grades: junior, middle, senior, lead
        - For each grade provide ranges for 3 regions:
          - moscow: salary in Moscow (RUB)
          - russian_province: salary in Russian regions (RUB)
          - remote_jobs: salary for international remote work (USD)
        - Each range contains: min_income, median_income, max_income
        - market_trend: market vector
          - trend: overall market trend ("growing" | "stable" | "declining")
          - reason: brief explanation of the trend (2 sentences).
        - top_employers: list of 3-5 real companies actively hiring
          specialists of this profile

        Salaries must be realistic and reflect the current 2026 market.
        Reply with ONLY valid JSON, no markdown wrappers, no explanations.

        Response format:
        {
          "role": "role name",
          "salary_table": {
            "junior": {
              "russian_province": {"min_income": 0, "median_income": 0, "max_income": 0},
              "moscow": {"min_income": 0, "median_income": 0, "max_income": 0},
              "remote_jobs": {"min_income": 0, "median_income": 0, "max_income": 0}
            },
            "middle": { ... },
            "senior": { ... },
            "lead": { ... }
          },
          "market_trend": {
            "trend": "growing",
            "reason": "Description this trend in 2 sentence."
          },
          "top_employers": ["Company1", "Company2", "Company3", "Company4"]
        }"""
