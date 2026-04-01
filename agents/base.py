import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('AI_API_KEY', 'ollama')

client = OpenAI(api_key=API_KEY, base_url="http://localhost:11434/v1")

response = client.chat.completions.create(
    model="deepseek-r1:8b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello. Which day is today?"},
    ],
    stream=False
)

print(f'сырой ответ: {response}', f'подготовленные данные {response.choices[0].message.content}')
