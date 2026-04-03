"""Генератор отчётов: JSON -> report.md. Атрошенко Б. С."""

import json
from datetime import datetime
from pathlib import Path


IMPORTANCE_EMOJI = {
    "critical": "🔴",
    "important": "🟡",
    "nice-to-have": "🟢",
}

TREND_EMOJI = {
    "growing": "📈",
    "stable": "➡️",
    "declining": "📉",
}

SEVERITY_EMOJI = {
    "critical": "🚨",
    "minor": "⚠️",
    "inaccuracy": "ℹ️",
}

RESOURCE_EMOJI = {
    "course": "🎓",
    "book": "📚",
    "documentation": "📖",
    "tutorial": "🛠️",
    "site": "🌐",
}


def _fmt_rub(value: int) -> str:
    """
    {число:,} позволяет числа по 3 знака отображать. Дальше просто делю на space + sign.
    :param value: сумма.
    :return: красивый формат в виде строки.
    """
    return f"{value:,}".replace(",", " ") + " ₽"


def _fmt_usd(value: int) -> str:
    """
    Отображение суммы в $.
    :param value: сумма.
    :return: красивый формат в виде строки.
    """
    return f"{value:,}".replace(",", " ") + " $"


def generate_report(data: dict, output_path: str = "report.md") -> None:
    """
    Генерирует красивый Markdown-отчёт из структурированного JSON.

    :param data: полный словарь с результатами всех агентов.
    :param output_path: путь для сохранения report.md.
    :return ничего. Просто генерирует md отчёт.
    """
    lines: list[str] = []

    role = data.get("role", "Unknown Role")
    generated_at_raw = data.get("generated_at", "")

    dt = datetime.fromisoformat(generated_at_raw)
    generated_at = dt.strftime("%d.%m.%Y %H:%M UTC")

    # Заголовок
    lines += [
        f"# Job Market Analysis Report",
        f"",
        f"> **Role:** {role}  ",
        f"> **Generated:** {generated_at}",
        f"",
        "---",
        "",
    ]

    # Анализ рынка
    ma = data.get("market_analyst", {}).get("data", {})
    if ma:
        lines += [
            "## 📊 Market Analysis",
            "",
            f"> {ma.get('market_trend_reason', '')}",
            "",
        ]

        skill_map = ma.get("skill_map", {})

        for name, skills in skill_map.items():
            if not skills:
                continue
            lines += [
                f"### {name.title()}",
                "",
                "| Skill | Importance | Trend |",
                "|-------|-----------|-------|",
            ]
            for s in skills:
                imp = s.get("importance", "")
                trend = s.get("trend", "")
                lines.append(
                    f"| {s.get('name', '')} "
                    f"| {IMPORTANCE_EMOJI.get(imp, '')} {imp} "
                    f"| {TREND_EMOJI.get(trend, '')} {trend} |"
                )
            lines.append("")

        lines += ["---", ""]

    # Зарплата
    se = data.get("salary_estimator", {}).get("data", {})
    if se:
        market_trend = se.get("market_trend", {})
        top_employers = se.get("top_employers", [])

        lines += [
            "## 💰 Salary Expectations",
            "",
            f"> **Market trend:** {TREND_EMOJI.get(market_trend.get('trend', ''), '')} "
            f"{market_trend.get('trend', '').capitalize()}  ",
            f"> {market_trend.get('reason', '')}",
            "",
        ]

        salary_table = se.get("salary_table", {})
        levels = ["junior", "middle", "senior", "lead"]
        regions = [
            ("russian_province", "Region (RU)", _fmt_rub),
            ("moscow", "Moscow", _fmt_rub),
            ("remote_jobs", "Remote (USD)", _fmt_usd),
        ]

        lines += [
            "### Salary Table",
            "",
            "| Level | Region (RU) | Moscow | Remote (USD) |",
            "|-------|-------------|--------|--------------|",
        ]

        for level in levels:
            level_data = salary_table.get(level, {})
            cells = []
            for region_key, _, fmt in regions:
                r = level_data.get(region_key, {})
                mn = fmt(r.get("min_income", 0))
                med = fmt(r.get("median_income", 0))
                mx = fmt(r.get("max_income", 0))
                cells.append(f"{mn} – {med} – {mx}")
            lines.append(f"| **{level.capitalize()}** | {' | '.join(cells)} |")

        lines += [
            "",
            "> Format: min – median – max",
            "",
        ]

        if top_employers:
            lines += [
                "### Top Employers",
                "",
            ]
            for emp in top_employers:
                lines.append(f"- {emp}")
            lines.append("")

        lines += ["---", ""]

    # Агент 3: Карьерный путь
    ca = data.get("career_advisor", {}).get("data", {})
    if ca:
        lines += [
            "## 🗺️ Career Roadmap",
            "",
        ]

        learning_path = ca.get("learning_path", [])
        stage_emoji = {"Foundation": "🏗️", "Practice": "⚙️", "Portfolio": "🎨"}

        for phase in learning_path:
            stage = phase.get("stage", "")
            milestone = phase.get("milestone", "")
            emoji = stage_emoji.get(stage, "📌")

            lines += [
                f"### {emoji} {stage}",
                "",
                f"**Milestone:** {milestone}",
                "",
            ]

            for topic in phase.get("topics", []):
                theme = topic.get("theme", "")
                lines += [f"**{theme}**", ""]
                for res in topic.get("resources", []):
                    r_type = res.get("type", "")
                    r_name = res.get("name", "")
                    lines.append(f"- {RESOURCE_EMOJI.get(r_type, '📄')} `{r_type}` — {r_name}")
                lines.append("")

        # Gap Analysis
        gap = ca.get("gap_analysis", {})
        if gap:
            lines += [
                "### 🎯 Gap Analysis",
                "",
                "#### Quick Wins _(2–4 weeks)_",
                "",
            ]
            for item in gap.get("quick_wins", []):
                lines.append(f"- **{item.get('skill', '')}** — {item.get('description', '')}")
            lines += [
                "",
                "#### Long-term Goals _(3+ months)_",
                "",
            ]
            for item in gap.get("long_term", []):
                lines.append(f"- **{item.get('skill', '')}** — {item.get('description', '')}")
            lines.append("")

        # Portfolio project
        portfolio = ca.get("portfolio_project", {})
        if portfolio:
            lines += [
                "### 💼 Portfolio Project",
                "",
                f"**{portfolio.get('title', '')}**",
                "",
                portfolio.get("description", ""),
                "",
                "**Skills demonstrated:**",
                "",
            ]
            for skill in portfolio.get("skills_demonstrated", []):
                lines.append(f"- `{skill}`")
            lines.append("")

        lines += ["---", ""]

    # Агент 4: Критик
    cv = data.get("critic_verifier", {}).get("data", {})
    if cv:
        score_data = cv.get("score", {})
        quality_index = score_data.get("quality_index", 0)
        is_consistent = cv.get("is_consistent", False)
        warnings = cv.get("warnings", [])

        verdict_emoji = "✅" if is_consistent else "❌"
        score_bar = _build_score_bar(quality_index)

        lines += [
            "## 🔍 Quality Assessment",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Quality Index | {score_bar} **{quality_index}/100** |",
            f"| Is Consistent | {verdict_emoji} {'Yes' if is_consistent else 'No'} |",
            "",
            f"> {score_data.get('reason', '')}",
            "",
        ]

        if warnings:
            lines += [
                "### Warnings",
                "",
            ]
            for w in warnings:
                sev = w.get("severity", "")
                emoji = SEVERITY_EMOJI.get(sev, "⚠️")
                lines += [
                    f"#### {emoji} {sev.capitalize()} — `{w.get('field', '')}`",
                    "",
                    w.get("message", ""),
                    "",
                ]
        else:
            lines += ["_No warnings detected._", ""]

        lines += ["---", ""]

    # Футер
    lines += [
        f"*Report generated automatically by the Job Market Analyzer agentic system.*",
    ]

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"[ReportGenerator] report.md сохранён -> {output_path}")


def _build_score_bar(score: int, length: int = 10) -> str:
    """Строит текстовый прогресс-бар для оценки качества."""
    filled = round(score / 100 * length)
    return "█" * filled + "░" * (length - filled)


def save_json(data: dict, output_path: str = "report.json") -> None:
    """
    Сохраняет структурированный результат всех агентов в JSON-файл.

    :param data: словарь со всеми данными от агентов.
    :param output_path: название файла для сохранения.
    :return ничего. Просто сохраняет JSON.
    """
    Path(output_path).write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[ReportGenerator] report.json сохранён -> {output_path}")
