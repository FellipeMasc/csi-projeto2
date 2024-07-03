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

class UtilityHandler:
    def __init__(self, browser, timeout):
        self.browser = browser
        self.timeout = timeout
    
    def clear_chat(self, name):
        self.browser.find_element(*WhatsAppElements.search).send_keys(name + Keys.ENTER)
        menu_xpath = "/html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[3]/div/span"
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, menu_xpath)))
        menu = self.browser.find_element_by_xpath(menu_xpath)
        menu.click()
        chains = ActionChains(self.browser)
        for i in range(4):
            chains.send_keys(Keys.ARROW_DOWN)
        chains.send_keys(Keys.ENTER)
        chains.perform()
        clear_xpath = '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[2]/div[2]'
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, clear_xpath)))
        self.browser.find_element_by_xpath(clear_xpath).click()
    
    def goto_main(self):
        try:
            self.browser.refresh()
            Alert(self.browser).accept()
        except Exception as e:
            print(e)
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(WhatsAppElements.search))
    
    def override_timeout(self, new_timeout):
        self.timeout = new_timeout
    
    def emojify(self, message):
        with open("emoji.json") as emojies:
            emoji = json.load(emojies)
        for em in emoji:
            message = message.replace(em, emoji[em])
        return message