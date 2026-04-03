"""Точка входа. Атрошенко Б. С."""

import argparse

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
    agent1_resp: dict = MarketAnalyst().run("Python Backend Dev")

    agent2_resp = SalaryEstimator().run(agent1_resp.get('data'))
