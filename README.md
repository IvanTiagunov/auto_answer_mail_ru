# Программа позволяет автоматически отвечать на новые вопросы в сервисе "Ответы mail.ru"
## Для взаимодействия с браузером используются библиотеки selenium

Для начала работы необходимо создать файл .env с параметрами:

MISTRAL_API_KEY - ключ апи от ИИ mistral
MODEL_NAME - название mistral модели. Можно указать mistral-large-latest, чтобы не обновлять руками 
GOOGLE_PROFILE_PATH - путь до папки с гугл профилем, чтобы обходить авторизацию

