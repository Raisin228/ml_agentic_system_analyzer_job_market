"""Модель ответа, в рамках которой размышляет Агент №3 - Карьерный советник. Атрошенко Б. С."""

from typing import Literal

from pydantic import BaseModel, Field


class Resource(BaseModel):
    """Источник информации."""

    name: str = Field(description="Название курса/книги/документации/сайта")
    type: Literal["course", "book", "documentation", "tutorial", "site"]


class Topic(BaseModel):
    """Темы и задачи, которые нужно подтянуть | решить в рамках стадии."""

    theme: str = Field(description="Название темы")
    resources: list[Resource] = Field(description="Список ресурсов где можно поискать информацию", min_length=2)


class Phase(BaseModel):
    """Разбивка по фазам."""

    stage: Literal["Foundation", "Practice", "Portfolio"]
    topics: list[Topic] = Field(description="Общий список тем для изучения", min_length=2, max_length=5)
    milestone: str = Field(description="Ожидаемый результат фазы")


class GapItem(BaseModel):
    """Каждый навык по отдельности и его описание."""

    skill: str
    description: str


class GapAnalysis(BaseModel):
    """Разбиение по сложности освоения каждого навыка."""

    quick_wins: list[GapItem] = Field(
        min_length=2,
        max_length=5,
        description="Навыки, которые можно закрыть за 2-4 недели"
    )
    long_term: list[GapItem] = Field(
        min_length=2,
        max_length=5,
        description="Навыки на 3+ месяца развития"
    )


class PortfolioProject(BaseModel):
    """Проекты, которые можно реализовать в качестве опыта для портфолио."""

    title: str = Field(description="Название проекта")
    description: str = Field(description="Краткое описание проекта", max_length=512)
    skills_demonstrated: list[str] = Field(
        description="Навыки, которые будут изучены в проекте", min_length=3, max_length=6
    )


class CareerAdvisorResponse(BaseModel):
    """Финальное заключение карьерного советника."""

    learning_path: list[Phase] = Field(description="Путь развития навыков из gap_analysis", min_length=3, max_length=3)
    gap_analysis: GapAnalysis = Field(description="Список того что нужно подучить и как быстро это можно сделать.")
    portfolio_project: PortfolioProject = Field(description="Проект для портфолио")
