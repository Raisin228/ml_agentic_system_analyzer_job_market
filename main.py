"""Точка входа. Атрошенко Б. С."""

import argparse

from agents.career_advisor_a3 import CareerAdvisor
from agents.critic_verifier_a4 import CriticVerifier
from agents.market_analyst_a1 import MarketAnalyst
from agents.salary_estimator_a2 import SalaryEstimator


def parse_args() -> argparse.Namespace:
    """Парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Job Market Analyzer")
    parser.add_argument(
        "--role",
        type=str,
        required=True,
        help='Название должности, например: "Backend Python Developer"',
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    agent1_resp: dict = MarketAnalyst().run("iOS Developer (Swift)")
    agent2_resp: dict = SalaryEstimator().run(agent1_resp.get("data"))
    req_data = {**agent1_resp.get("data"), **agent2_resp.get("data")}
    agent3_resp: dict = CareerAdvisor().run(req_data)

    common_res_last_agents = {
        "market_analyst": agent1_resp, "salary_estimator": agent2_resp, "career_advisor": agent3_resp
    }
    agent4_resp: dict = CriticVerifier().run(common_res_last_agents)
