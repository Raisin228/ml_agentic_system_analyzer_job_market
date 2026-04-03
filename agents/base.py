"""Базовая логика для работы Агентов. Атрошенко Б. С."""

import os
import json

import logging
from abc import ABC, abstractmethod
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import Json
from datetime import UTC, datetime
import instructor

from consts import AvailableModels

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, handlers=[logging.StreamHandler(), logging.FileHandler("run.log", mode='w')]
)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("instructor").setLevel(logging.WARNING)


class BaseAgent(ABC):
    """Начальная логика для Агентов."""

    def __init__(
            self, resp_model, model: str = AvailableModels.QWEN, name: str = "BASE_AGENT", retries: int = 5
    ) -> None:
        """
        Обычный инициализатор.

        :param resp_model: модель по которой будет формироваться ответ от Агента.
        :param model: модель для обработки запроса.
        :param name: имя агента, которое будет использоваться в логах.
        :param retries: кол-во попыток, которое модель будет пытаться
        генерить ответ в соответствии со схемой Pydantic.
        """
        self.model: str = model
        self.api_key: str = os.getenv("AI_API_KEY", "ollama")

        self.resp_model = resp_model
        self.retries: int = retries
        self.agent_name: str = name
        self.client = instructor.from_openai(
            OpenAI(api_key=self.api_key, base_url="http://localhost:11434/v1"),
            mode=instructor.Mode.JSON
        )

    @abstractmethod
    def system_prompt(self):
        """Системный промпт c ролью и заданием для агента."""

    @abstractmethod
    def build_prompt(self, input_data: str | dict) -> str:
        """
        Подготавливает итоговый промпт для вызова LLM.

        :param input_data: для первого агента это строка с названием должности,
        для следующих это dict от прошлого агента.
        :return строка с ответом.
        """

    def call_llm(self, user_prompt: str):
        """
        Вызов модели и получение сырого ответа.

        :param user_prompt: подготовленный и преобразованный запрос пользователя.
        :return: ответ от агента в определённом формате.
        """
        response = self.client.chat.completions.create(  # type: ignore
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "system", "content": self.system_prompt()}, {"role": "user", "content": user_prompt}],
            response_model=self.resp_model,
            max_retries=self.retries,
        )

        return response

    def run(self, input_data: str | dict) -> dict | Exception:
        """
        Механизм для запуска агентов.

        :param input_data: для первого агента это строка с названием должности,
        для следующих это JSON от прошлого агента.
        :return словарик с ответом от модели.
        """
        user_prompt = self.build_prompt(input_data)
        last_wrong = None

        for attempt in range(1, self.retries + 1):
            logger.info(f"[{self.agent_name}] Попытка {attempt}/{self.retries}")

            prompt: str = user_prompt
            if last_wrong:
                prompt += (
                    f"The previous response failed Pydantic schema validation. {last_wrong}"
                    f"Regenerate the response so that it satisfies the response model."
                )

            try:
                response = self.call_llm(prompt)
                logger.info(
                    f"[{self.agent_name}] Успешная попытка.\n"
                    f"generated_at: {datetime.now(tz=UTC).isoformat()}\n"
                    f"data = {
                        json.dumps(response.model_dump(), indent=2, ensure_ascii=False)
                    }\n"
                    f"====================="
                )
                return {
                    "agent": self.agent_name,
                    "generated_at": datetime.now(tz=UTC).isoformat(),
                    "data": response.model_dump(),
                }

            except Exception as ex:
                logger.warning(
                    f"[{self.agent_name}] Неудача на попытке {attempt}. Ошибка: {ex}"
                )

        raise RuntimeError(
            f"[{self.agent_name}] Не смог создать валидный ответ за {self.retries} попыток."
        )
