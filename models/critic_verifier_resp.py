"""Модель ответа, в рамках которой размышляет Агент №4 - Критик и верификатор. Атрошенко Б. С."""

from typing import Literal
from pydantic import BaseModel, Field


class Score(BaseModel):
    """Общий балл за отчёт."""

    quality_index: int = Field(description="Оценка по всему отчёту", ge=0, le=100)
    reason: str = Field(description="Причина такого индекса", min_length=100, max_length=1024)


class Warns(BaseModel):
    """Предупреждения найденные системой."""

    field: str = Field(description="Поле, в котором найдено несоответстве")
    severity: Literal["critical", "minor", "inaccuracy"]
    message: str = Field(description="Краткое описание неточности", min_length=50, max_length=256)


class CriticVerifierResponse(BaseModel):
    """Итоговый ответ от Критика и верификатора."""

    score: Score = Field(description="Общая оценка с пояснением")
    is_consistent: bool = Field(description="Итоговый вердикт о целости отчёта")
    warnings: list[Warns] = Field(description="Обнаруженные несоответствия в данных", min_length=0, max_length=5)
