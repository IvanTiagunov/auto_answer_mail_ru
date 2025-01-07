import logging

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.exceptions import ParseException
import pyperclip


class QuestionCard:
    """Карточка вопроса в mail.ru"""

    def __init__(self, question=None, sub=None):
        self.question = question
        self.sub = sub

    def get_text(self):
        if self.sub:
            return self.question + " " + self.sub
        else:
            return self.question


class MailRuParser:
    """Парсер ответов mail.ru"""

    def __init__(self, profile_path=None):
        if profile_path:
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir={profile_path}")
        else:
            options = None
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.main_url = "https://otvet.mail.ru/"

    def __enter__(self):
        """Контекстный менеджер"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Контекстный менеджер"""
        self.__close_all()

    def __close_all(self):
        """Закрываем вкладки и завершаем сессию"""
        for _ in self.driver.window_handles:
            try:
                # пробуем переключить контекст на первую вкладку
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.close_tab()
            except:
                pass
        self.driver.quit()

    def open_main_page(self):
        """Открытие главной страницы через клик по логотипу"""
        logging.info("Открыли главную страницу")
        self.driver.get(self.main_url)
        self.driver.switch_to.window(window_name=self.driver.window_handles[0])
        logo = self.driver.find_element(By.XPATH, "//div[@title='Праздничные Ответы Mail']")
        logo.click()

    def get_visible_questions_url_list(self):
        """Получить список отображенных вопросов"""
        visible_questions = self.driver.find_elements(By.XPATH,
                                                      "//a[starts-with(@href, '/question/') and @class='ZePiW']")
        if len(visible_questions) == 0:
            raise ParseException("На странице отстутствуют вопросы")
        question_urls = [q.get_attribute("href") for q in visible_questions]
        return question_urls

    def choose_question(self, num=0):
        """Выбрать вопрос из списка и получить ссылку на него"""
        questions_list = self.get_visible_questions_url_list()
        if len(questions_list) <= num:
            raise IndexError(f"Отсутствует вопрос с порядковым номером {num}")
        return questions_list[num]

    def get_question_card(self, question_url):
        """Получение вопроса из карточки"""
        self.open_new_tab(question_url)
        question_text = self.driver.find_element(
            by=By.XPATH,
            value="/html/body/div[2]/div[3]/div/div[2]/div/div/div[2]/div/div/div[3]/div[3]/div/h1"
        ).text
        try:
            question_sub = self.driver.find_element(
                by=By.XPATH,
                value="/html/body/div[2]/div[3]/div/div[2]/div/div/div[2]/div/div/div[3]/div[3]/div/div/div/div/p"
            ).text
        except:
            question_sub = None

        q_card = QuestionCard(question=question_text, sub=question_sub)

        return q_card

    def write_answer(self, text):
        """Записать ответ"""
        pyperclip.copy(text)
        try:
            answer_button = self.driver.find_element(By.XPATH, "//a[@title='Ответить']")
            answer_button.click()
        except Exception as e:
            print(e)
        input_field = self.driver.find_element(By.XPATH, "//p[@data-placeholder='Введите текст ответа']")
        input_field.click()
        input_field.send_keys(Keys.CONTROL + 'v')
        input_field.send_keys(Keys.CONTROL + Keys.ENTER)

    def open_new_tab(self, url):
        """Открыть ссылку вопроса в новой вкладке браузера"""
        logging.info("Открыли страницу")
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        self.driver.switch_to.window(window_name=self.driver.window_handles[1])

    def close_tab(self):
        """Загруть вкладку браузера"""
        logging.info("Закрыли страницу")
        self.driver.execute_script(f"window.close();")
        self.driver.switch_to.window(window_name=self.driver.window_handles[0])
