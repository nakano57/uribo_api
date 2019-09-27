from uribo_login import uribo
import keys


import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class uribo_api(uribo.login):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_cookie_to_selenium()

    def set_cookie_to_selenium(self):

        self.driver = webdriver.Chrome()
        # 一度なんか開いておかないとエラーが出る
        self.driver.get('https://example.com')

        # uriからCookieをもらう。辞書型で帰ってくる
        cookie = self.cookies.get_dict()

        # 渡す
        for cookie_value in cookie:
            self.driver.add_cookie({'name': cookie_value,
                                    'value': cookie[cookie_value],
                                    'domain': 'kobe-u.ac.jp'})

        return self.driver

    def _get_json(self, code):
        pass

    def get_syllabus(self, code):
        self.driver.get(
            'https://kym-web.ofc.kobe-u.ac.jp/campusweb/campusportal.do?page=main&tabId=sy')

        WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located)
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it("portlet-body"))
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, 'jikanwaricd')))

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        data = {
            "_eventId": "byCode",
            "_flowExecutionKey": soup.find_all("input")[2].get('value'),
            "backTo": "input",
            "nendo": "2019",
            "gakkiKubunCode": int(code[0])+2,
            "jikanwaricd": code
        }

        postadr = "https://kym-web.ofc.kobe-u.ac.jp/campusweb/campussquare.do"
        res = uri.post(postadr, data=data)
        self.driver.get(res.url)
        print(res.url)

        return res.text


if __name__ == "__main__":

    uri = uribo_api(id=keys.userid, password=keys.passwd)

    uri.get_syllabus("4T305")
