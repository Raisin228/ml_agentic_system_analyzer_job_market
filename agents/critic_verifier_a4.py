"""Критик и верификатор. Атрошенко Б. С."""

from agents.base import BaseAgent
from models.critic_verifier_resp import CriticVerifierResponse


class CriticVerifier(BaseAgent):

    def __init__(self):
        super().__init__(CriticVerifierResponse, name="CriticVerifier")

    def build_prompt(self, input_data: str | dict) -> str:
        """
        Промпт задание.

        :param input_data: данные от Агента1.
        :return строка с заданием.
        """
        return (
            f"Review the following career report for consistency and quality.\n\n"
            f"=== SKILL MAP (Response Agent 1) ===\n"
            f"{input_data.get("market_analyst")}\n\n"
            f"=== SALARY TABLE (Agent 2) ===\n"
            f"{input_data.get("salary_estimator")}\n\n"
            f"=== CAREER PLAN (Agent 3) ===\n"
            f"{input_data.get("career_advisor")}\n\n"
            f"Analyze the report and provide your verdict."
        )

    def system_prompt(self) -> str:
        """Системный промпт c ролью и заданием для агента."""
        return """You are a strict quality auditor for IT career reports.

        Your task: review the full report produced by 3 previous agents (skill_map, 
        salary_table, career plan) and verify its consistency and quality.

        Checks to perform:
        - Do salary ranges match the skill demand levels? (critical skills should 
          correlate with higher salaries)
        - Are there contradictions? For example: a skill marked as "declining" 
          should NOT be prioritized in learning_path — if it is, add a warning.
        - Do the portfolio_project technologies actually appear in the skill_map?
        - Are the resources in learning_path realistic and relevant?
        - Does gap_analysis align with skill_map priorities?

        Rules:
        - quality_score: integer 0-100 with justification
        - warnings: list every inconsistency found. Each warning has a field name, 
          severity ("critical" or "minor"), and a message explaining the issue.
          The list CAN be empty if no issues are found.
        - is_consistent: true only if there are no critical warnings

        Respond ONLY with valid JSON without markdown wrappers or explanations.

        Example JSON response:
        {
          "quality_score": 72,
          "quality_score_reason": "Salary ranges are realistic but learning_path includes a declining skill as priority topic.",
          "warnings": [
            {
              "field": "skill_map.frameworks.jQuery",
              "severity": "critical",
              "message": "jQuery is marked as declining in skill_map but appears as a Foundation topic"
            },
            {
              "field": "salary_table.junior.remote_usd",
              "severity": "minor",
              "message": "Junior remote USD salary seems too high for entry-level position"
            }
          ],
          "is_consistent": false
        }"""
