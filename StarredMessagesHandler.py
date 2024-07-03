import time
import datetime as dt
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert

class StarredMessagesHandler:
    def __init__(self, browser, timeout):
        self.browser = browser
        self.timeout = timeout
    
    def get_starred_messages(self, delay=10):
        starred_messages = []
        self.browser.find_element_by_css_selector("div.rAUz7:nth-child(3) > div:nth-child(1) > span:nth-child(1)").click()
        chains = ActionChains(self.browser)
        time.sleep(2)
        for i in range(4):
            chains.send_keys(Keys.ARROW_DOWN)
        chains.send_keys(Keys.ENTER)
        chains.perform()
        time.sleep(delay)
        messages = self.browser.find_elements_by_class_name("MS-DH")
        for message in messages:
            try:
                message_html = message.get_attribute("innerHTML")
                soup = BeautifulSoup(message_html, "html.parser")
                _from = soup.find("span", class_="_1qUQi")["title"]
                to = soup.find("div", class_="copyable-text")["data-pre-plain-text"]
                message_text = soup.find("span", class_="selectable-text invisible-space copyable-text").text
                message.click()
                selector = self.browser.find_element_by_css_selector("#main > header > div._5SiUq > div._16vzP > div > span")
                title = selector.text
                selector.click()
                time.sleep(2)
                WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div._14oqx:nth-child(3) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)"))
                )
                phone = self.browser.find_element_by_css_selector("div._14oqx:nth-child(3) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)").text
                if title in _from:
                    _from = _from.replace(title, phone)
                else:
                    to = to.replace(title, phone)
                starred_messages.append([_from, to, message_text])
            except Exception as e:
                print("Handled: ", e)
        return starred_messages
