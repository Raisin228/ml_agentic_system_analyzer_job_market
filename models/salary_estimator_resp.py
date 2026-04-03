"""Модель ответа, в рамках размышления для Агента №2 - Оценщик ЗП. Атрошенко Б. С."""
from pydantic import BaseModel, Field
from typing import Literal


class SalaryRange(BaseModel):
    """3 уровня зарплатных вилок."""

    min_income: int = Field(default=1, description="Минимальная сумма дохода в локации")
    median_income: int = Field(default=10, description="Средний доход в рамках должности")
    max_income: int = Field(default=100, description="Потолок рынка в данной должности")


class RegionBreakdown(BaseModel):
    """Разбивка дохода по регионам."""

    russian_province: SalaryRange = Field(description="Зп на позицию в рамках регионов")
    moscow: SalaryRange = Field(description="Зп на позицию в МСК")
    remote_jobs: SalaryRange = Field(description="Зп за рубежом / валютная удалёнка")


class GradationByLevels(BaseModel):
    """Разбивка по уровню сотрудника."""

    junior: RegionBreakdown = Field(description="Дохо для Jun'а")
    middle: RegionBreakdown = Field(description="Дохо для Midl'а")
    senior: RegionBreakdown = Field(description="Дохо для Senior'а")
    lead: RegionBreakdown = Field(description="Дохо для Lead'а")

class MarketVector(BaseModel):
    """Направление рынка и почему именно такое."""

    trend: Literal["growing", "stable", "declining"]
    reason: str = Field(
        min_length=1,
        description="Обоснование тренда, 1-2 предложения"
    )

class SalaryExpectations(BaseModel):
    """Итоговая выборка от оценщика зарплат."""

    salary_table: GradationByLevels
    market_trend: MarketVector
    top_employers: list[str] = Field(
        description="Компании, где требуются специалисты этого профиля",
        min_length=3, max_length=5
    )
