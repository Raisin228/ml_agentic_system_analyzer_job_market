"""Базовая логика для работы Агентов. Атрошенко Б. С."""

import os

import logging
from abc import ABC, abstractmethod
from openai import OpenAI, max_retries
from dotenv import load_dotenv
from pydantic import Json
from datetime import UTC, datetime

from consts import AvailableModels

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


class BaseAgent(ABC):
    """Начальная логика для Агентов."""

    def __init__(self, model: str = AvailableModels.QWEN, name: str = "BASE_AGENT") -> None:
        """Обычный инициализатор."""
        self.model: str = model
        self.api_key: str = os.getenv("AI_API_KEY", "ollama")
        self.client = OpenAI(api_key=self.api_key, base_url="http://localhost:11434/v1")
        self.agent_name: str = name

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Системный промпт c ролью и заданием для агента."""

    @abstractmethod
    def build_prompt(self, input_data: str | Json) -> str:
        """
        Подготавливает итоговый промпт для вызова LLM.

        :param input_data: для первого агента это строка с названием должности,
        для следующих это JSON от прошлого агента.
        :return строка с ответом.
        """

    def call_llm(self, user_prompt: str) -> str:
        """
        Вызов модели и получение сырого ответа.

        :param user_prompt: подготовленный и преобразованный запрос пользователя.
        :return: сырой формат ответа модели.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "system", "content": self.system_prompt()}, {"role": "user", "content": user_prompt}],
            stream=False,
        )

        return response.choices[0].message.content

    def convert_to_json(self, data: str) -> dict:
        print(data)


    def response_parser(self, raw_data: str):
        data = self.convert_to_json(raw_data)

    def run(self, input_data: str | Json, retries: int = 5) -> dict | Exception:
        """
        Механизм для запуска агентов.

        :param input_data: для первого агента это строка с названием должности,
        для следующих это JSON от прошлого агента.
        :param retries: кол-во попыток, которое модель будет пытаться
        генерить ответ в соответствии со схемой Pydantic.
        :return словарик с ответом от модели.
        """
        user_prompt = self.build_prompt(input_data)
        last_wrong = None

        for attempt in range(1, retries + 1):
            logger.info(f"[{self.agent_name}] Попытка {attempt}/{retries}")

            prompt: str = user_prompt
            if last_wrong:
                prompt += (
                    f"Прошлый ответ не прошёл валидацию по схеме Pydantic. {last_wrong}"
                    f"Перегенерируй ответ так чтоб он удовлетворял модели ответа."
                )

            try:
                raw_resp = self.call_llm(prompt)
                logger.debug(f"[{self.agent_name}] Сырой ответ агента {raw_resp}")

                # успешная попытка None проблема в parser
                response = self.response_parser(raw_resp)

                logger.info(f"[{self.agent_name}] Успешная попытка. {response}")
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
            f"[{self.agent_name}] Не смог создать валидный ответ за {max_retries} попыток."
        )
