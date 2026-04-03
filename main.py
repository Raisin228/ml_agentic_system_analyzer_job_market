"""Точка входа. Атрошенко Б. С."""

import argparse

from agents.market_analyst_a1 import MarketAnalyst


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
    agent = MarketAnalyst()
    print(agent.run("Python Backend Dev"))
