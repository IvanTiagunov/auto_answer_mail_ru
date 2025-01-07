import logging

from mistralai import Mistral, UserMessage

from src.exceptions import TextProcessingException
from src.opts import config

api_key = config.get("MISTRAL_API_KEY")
model = config.get("MODEL_NAME")

client = Mistral(api_key=api_key)


def call_gpt(message):
    """
    Route message to from user to AI and return answer
    """
    logging.info(f"Задаём вопрос с текстом {message}")

    prompt = (
        "Представь, что ты всезнающий мудрец и отвечаешь на вопросы текстом. "
        "Твоя задача — сделать ответ максимально естественным и живым, чтобы он не выглядел как генерированный ИИ. "
        "Вот несколько советов, которые помогут тебе в этом:\n\n"
        "1. Используй разнообразные предложения: Человеческий текст часто состоит из предложений разной длины и структуры. Избегай однообразия.\n"
        "2. Добавь эмоции и личные мнения: Включай свои мысли, чувства и опыт. Это делает текст более живым и уникальным.\n"
        "3. Используй неформальный язык: В зависимости от контекста, неформальный язык может сделать текст более естественным.\n"
        "4. Добавь ошибки и неточности: Люди иногда делают грамматические ошибки или используют неточные выражения. Это нормально и делает текст более человечным.\n"
        "5. Используй метафоры и сравнения: Это добавляет тексту глубины и делает его более интересным для чтения.\n"
        "6. Добавь диалоги или цитаты: Это помогает разнообразить текст и сделать его более динамичным.\n\n"
        "Теперь напиши текст на следующую тему: "
    )
    full_message = prompt + message
    message_from_user = [UserMessage(content=full_message)]
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=message_from_user,

        )
    except Exception as e:
        print("Бот не смог обработать сообщение, измените запрос")
        return TextProcessingException(message)

    response_text = chat_response.choices[0].message.content
    logging.info(f"Получили от ГПТ: {response_text}")
    return response_text
