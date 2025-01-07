import logging
import time

from src.models.mistral_connector import call_gpt
from src.parsers.mail_ru import MailRuParser
from src.opts import config

logging.basicConfig(
    filename='bot_messages.log',
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
    filemode="a+",
    encoding="UTF-8"
)


def run_app():
    with MailRuParser(config.get("GOOGLE_PROFILE_PATH")) as parser:
        parser.open_main_page()
        questions_urls = parser.get_visible_questions_url_list()
        for q_url in questions_urls:
            question_card = parser.get_question_card(q_url)
            gpt_response: str = call_gpt(question_card.get_text())
            gpt_response = gpt_response.replace("*", "")
            result_text = gpt_response.replace("#", "")
            try:
                parser.write_answer(result_text)
                time.sleep(1)
            except:
                pass
            parser.close_tab()


if __name__ == '__main__':
    run_app()
