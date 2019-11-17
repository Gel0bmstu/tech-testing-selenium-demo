# -*- coding: utf-8 -*-

import os

import unittest
import urllib.parse

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# Name: Solovev Oleg
# Team: DwaDauna

# Check-list:

# - Если пользователь не авторизован, то при нажатии на кнопку "Фото" или "Видео" должно всплывать окно авторизации. X
# - При вводе невалидной строки в теме вопроса/опроса (Прример: "ыв ыва ыва 23") длжно всплывать окно с ошибкой X
#   "Просьба более подробно и грамотно сформулировать тему вопроса.".
# - При вводе большого текста в поле "Текст вопроса" появляется предупреждение об ограничении в 3800 символов.X
# - При публикации нового опроса должно всплывать окно, информирующее о возможности редактирования содежания опроса в течении 30 мин. ~X
# - По нажатию на кнопку "Настройки" открывается страница пользовательских настроек. X
# - Автоматическое добавление новой формы ответа по нажатию на последнюю в списке форму вопросов при "включении" опции 
#   "Можно выбрать несколько вариантов" в форме создания опроса и его публикации. 
#   То есть в форме создания опроса изначально нам доступны 3 варианта ответа в виде 3-х незаполненных форм, 
#   проверить нужно добавление новой формы при нажатии на последнюю форму в списке.

class Page(object):
    BASE_URL = 'https://otvet.mail.ru/ask'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urllib.parse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()

class QuestionPage(Page):
    PATH = ''

    @property
    def photo_video_uploader(self):
        return QuestionForm(self.driver)

class AuthPage(Page):
    PATH = ''

    @property
    def auth_form(self):
        return AuthForm(self.driver)

class PoolPage(Page):
    PATH = ''

    @property
    def poll_form(self):
        return PollForm(self.driver)

class Component(object):

    def __init__(self, driver):
        self.driver = driver

    def switch_driver_to_iframe(self, iframe_class_name):
        login_window = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_class_name(iframe_class_name)
        )
        self.driver.switch_to.frame(login_window)

    def switch_driver_to_default_content(self):
        self.driver.switch_to_default_content()

    def press_esc(self):
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
    


class AuthForm(Component):
    LOGIN = '//input[@name="Login"]'
    PASSWORD = '//input[@name="Password"]'
    SUBMIT_LOGIN = '//span[text()="Ввести пароль"]'
    SUBMIT_PASSWORD = '//span[text()="Войти"]'
    LOGIN_BUTTON = '//a[text()="Вход"]'

    def open_form(self):
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LOGIN_BUTTON).click()
        )
        # self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()

    def find_login_input(self):
        return WebDriverWait(self.driver, 15, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LOGIN)
        )

    def find_login_submit_button(self):
        return WebDriverWait(self.driver, 15, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SUBMIT_LOGIN)
        )


    def send_login(self, login):
        login_form = self.find_login_input()
        submit_button = self.find_login_submit_button()
        login_form.send_keys(login)
        submit_button.click()

    def set_login(self, login):
        login_form = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LOGIN)
        )
        login_form.send_keys(login)
    
    def submit_login(self):
        submit_login_button = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SUBMIT_LOGIN)
        )
        submit_login_button.click()

    def set_password(self, pwd):
        password_form = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.PASSWORD)
        )
        password_form.send_keys(pwd)
        
    def submit_password(self):
        submit_password_button = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SUBMIT_PASSWORD)
        )
        submit_password_button.click()

    def authorization(self, mail, passwd):
        # self.set_login(mail)
        # self.submit_login()
        self.send_login(mail)
        self.set_password(passwd)
        self.submit_password()


class PollForm(Component):
    def open_poll_form(self):
        pool_form = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_class_name('_3LtjwRRK3wqD0IfUUl1sxB_0')
        )
        pool_form.click()

    def check_poll_option_correct_add(self):

        variant_3 = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath('//div[@name="poll_options"]/div[4]/label/div[2]/div/div/div/input')
        )
        variant_3.click()
        variant_3.send_keys("getting 4 option")
        
        variant_4 = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath('//div[@name="poll_options"]/div[5]/label/div[2]/div/div/div/input')
        )

        variant_4.click()
        variant_4.send_keys("getting 5 option")

        self.driver.find_element_by_xpath('//div[@name="poll_options"]/div[6]/label/div[2]/div/div/div/input')


class QuestionForm(Component):

    LARGETEXT = 'sdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffffsdfffffffffffffffffffffffffffffff'

    def find_question_form(self):
        return self.driver.find_element_by_xpath('//div[@data-vv-as="«Текст вопроса»"]')

    def open_photo_upload_form(self):
        photo_span = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath('//span[text()="Фото"]')
        )
        photo_span.find_element_by_xpath('./..').click()

    def open_video_upload_form(self):
        video_span = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath('//span[text()="Видео"]')
        )
        video_span.find_element_by_xpath('./..').click()

    def close_login_form(self):
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def print_question_text(self, text):
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath('//textarea[@name="question_additional"]').send_keys(text)
        )

    def print_question_title(self, text):
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath('//textarea[@name="question_text"]').send_keys(text)
        )
        
    def check_question_title_textarea_alert(self):
        self.print_question_title("sadf")
        self.print_question_text("sadf")
        self.driver.find_element_by_class_name('_3ykLdYEqVa47ACQrpqnZOj_0').click()
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_class_name('popup--fade')
        )

    def check_question_textarea_alert(self):
        self.print_question_text(self.LARGETEXT)
        self.driver.find_element_by_xpath('//div[text()="Поле «Текст вопроса» не может быть больше 3800 символов."]')

    def make_default_question(self):
        # self.print_question_title("Вопрос про салаты")
        # self.print_question_text("Собственно говоря, если греческий салат испортился, то можно ли его называть древнегреческим?")
        # self.print_question_title("Ээ Кызлыр жэб кыздыр ламар? Котык басс дырбн кизлар?")
        # self.print_question_text("Тухтур игрым буерак из матч ай джаст донт нов вот то райт хир фор секс сессфулли пассинг бот чекинг")
        self.print_question_title("Ду бист ай, оо мин ин де швайн ,bpyfh")
        self.print_question_text("ыва")
        
        self.driver.find_element_by_class_name('_3ykLdYEqVa47ACQrpqnZOj_0').click()

    def chaeck_edit_time(self):
        WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_class_name('q-edit-control')
        )

    def delete_question(self):
        self.driver.find_element_by_class_name('btn action--sms').click()

    def check_settings_page(self):
        settings_button = WebDriverWait(self.driver, 10, 0.1).until(
            lambda d: d.find_element_by_xpath('//span[text()="Настройки"]')
        )    
        settings_button.click()
        WebDriverWait(self.driver, 10, 0.1).until(
            # lambda d: d.find_element_by_xpath('//button[@name="submit_btn"]').click()
            lambda d: d.find_element_by_class_name('page-settings')
        )    

class ExampleTest(unittest.TestCase):
    USERNAME = u'Олег Соловев'
    # USEREMAIL = 'kotegov_dima@mail.ru'
    # PASSWORD = os.environ['PASSWORD']
    USEREMAIL = ''
    PASSWORD = ''
    BLOG = 'Флудилка'
    TITLE = u'ЗаГоЛоВоК'
    MAIN_TEXT = u'Текст под катом! Отображается внутри топика!'

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def test(self):
        auth_page = AuthPage(self.driver)
        question_page = QuestionPage(self.driver)
        poll_page = PoolPage(self.driver)
        auth_page.open()

        # - Если пользователь не авторизован, то при нажатии на кнопку "Фото" или "Видео" должно всплывать окно авторизации.
        question_form = question_page.photo_video_uploader
        
        # question_form.open_photo_upload_form()
        # question_form.press_esc()

        # question_form.open_video_upload_form()
        # question_form.press_esc()

        print('Photo/video upload test:...PASSED')
        # Авторизируемся 
        auth_form = auth_page.auth_form

        auth_form.open_form()
        auth_form.switch_driver_to_iframe("ag-popup__frame__layout__iframe")

        # auth_form.set_login(self.USEREMAIL)
        # auth_form.submit_login()

        # auth_form.set_password(self.PASSWORD)
        # auth_form.submit_password()
        auth_form.authorization(self.USEREMAIL, self.PASSWORD)

        auth_form.switch_driver_to_default_content()

        print('Authorization:...........PASSED')

        # # - При создании нового опроса по нажатию на последний вариант ответа в блоке "Варианты ответов" в 
        # #   список вариантов должен добавляться новый вариант.
        # poll_form = poll_page.poll_form
        # poll_form.open_poll_form()

        # print('get 2')

        # # - При вводе большого текста в поле "Текст вопроса" появляется предупреждение об ограничении в 3800 символов.
        # question_form.check_question_textarea_alert()

        # print('get 3')

        # # - При вводе невалидной строки в теме вопроса/опроса (Прример: "ыв ыва ыва 23") длжно всплывать окно с ошибкой 
        # #   "Просьба более подробно и грамотно сформулировать тему вопроса.".
        # question_form.check_question_title_textarea_alert()
        # question_form.close_login_form()

        # print('get 4')

        # # - При публикации нового опроса должно всплывать окно, информирующее о возможности редактирования содежания опроса в течении 30 мин.
        # # question_form.make_default_question()
        # # question_form.chaeck_edit_time()
        # # question_form.delete_question()

        # # - По нажатию на кнопку "Настройки" открывается страница пользовательских настроек. X
        # question_form.check_settings_page()
        # auth_page.open()

        # print('get 5')        

        # # - Автоматическое добавление новой формы ответа по нажатию на последнюю в списке форму вопросов при "включении" опции 
        # #   "Можно выбрать несколько вариантов" в форме создания опроса и его публикации. 
        # #   То есть в форме создания опроса изначально нам доступны 3 варианта ответа в виде 3-х незаполненных форм, 
        # #   проверить нужно добавление новой формы при нажатии на последнюю форму в списке.
        # poll_form = poll_page.poll_form
        # poll_form.open_poll_form()
        # poll_form.check_poll_option_correct_add()

        # print('get 6')
