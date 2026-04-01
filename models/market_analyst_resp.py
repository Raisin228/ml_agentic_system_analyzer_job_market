"""Модель ответа, в рамках которой размышляет Агент №1 - Аналитик Рынка."""

from pydantic import BaseModel, Field
from typing import Literal


class Skill(BaseModel):
    """Один конкретный навык, его значимость и тренд."""

    name: str
    importance: Literal["critical", "important", "nice-to-have"]
    trend: Literal["growing", "stable", "declining"]


class SkillMap(BaseModel):
    """Карта с перечислением основных навыков специалиста. Hard | Soft ..."""

    languages: list[Skill]
    frameworks: list[Skill]
    infrastructure: list[Skill]
    soft_skills: list[Skill]


class MarketAnalizerResponse(BaseModel):
    """Финальная модель ответа, содержащая название должности."""

    job_title: str
    skill_map: SkillMap
    market_trend_reason: str = Field(min_length=1, description="Причины такого тренда")
