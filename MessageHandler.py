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
from WhatsAppElements import *
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

class MessageHandler:
    def __init__(self, browser, timeout):
        self.browser = browser
        self.timeout = timeout
    
    def send_message(self, name, message):
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(name + Keys.ENTER)
        try:
            send_msg = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]"))
            )
            messages = message.split("\n")
            for msg in messages:
                send_msg.send_keys(msg)
                send_msg.send_keys(Keys.SHIFT + Keys.ENTER)
            send_msg.send_keys(Keys.ENTER)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def send_blind_message(self, message):
        try:
            message = self.emojify(message)
            send_msg = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]"))
            )
            messages = message.split("\n")
            for msg in messages:
                send_msg.send_keys(msg)
                send_msg.send_keys(Keys.SHIFT + Keys.ENTER)
            send_msg.send_keys(Keys.ENTER)
            return True
        except NoSuchElementException:
            return "Unable to Locate the element"
        except Exception as e:
            print(e)
            return False

    def send_picture(self, name, picture_location, caption=None):
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(name + Keys.ENTER)
        try:
            send_file_xpath = '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span'
            attach_type_xpath = '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'
            # open attach menu
            attach_btn = self.browser.find_element(*WhatsAppElements.attach_icon)
            attach_btn.click()

            # Find attach file btn and send screenshot path to input
            time.sleep(1)
            attach_img_btn = self.browser.find_element_by_xpath(attach_type_xpath)
            attach_img_btn.send_keys(picture_location)
            time.sleep(1)
            if caption:
                caption_xpath = "/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]"
                send_caption = self.browser.find_element_by_xpath(caption_xpath)
                send_caption.send_keys(caption)
            send_btn = self.browser.find_element_by_xpath(send_file_xpath)
            send_btn.click()

        except (NoSuchElementException, ElementNotVisibleException) as e:
            print(str(e))

    def send_document(self, name, document_location):
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(name + Keys.ENTER)
        try:
            attach_xpath = '//*[@id="main"]/header/div[3]/div/div[2]/div'
            send_file_xpath = '/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span'
            attach_type_xpath = '/html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button/input'
            # open attach menu
            attach_btn = self.browser.find_element_by_xpath(attach_xpath)
            attach_btn.click()

            # Find attach file btn and send document path to input
            time.sleep(1)
            attach_img_btn = self.browser.find_element_by_xpath(attach_type_xpath)
            attach_img_btn.send_keys(document_location)
            time.sleep(1)
            send_btn = self.browser.find_element_by_xpath(send_file_xpath)
            send_btn.click()

        except (NoSuchElementException, ElementNotVisibleException) as e:
            print(str(e))

    def send_anon_message(self, phone, text):
        payload = urlencode({"phone": phone, "text": text, "source": "", "data": ""})
        self.browser.get("https://api.whatsapp.com/send?" + payload)
        try:
            Alert(self.browser).accept()
        except:
            print("No alert Found")
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#action-button")))
        send_message = self.browser.find_element_by_css_selector("#action-button")
        send_message.click()
        confirm = WebDriverWait(self.browser, self.timeout + 5).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]")))
        confirm.clear()
        confirm.send_keys(text + Keys.ENTER)

    def is_message_present(self, username, message):
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(username + Keys.ENTER)
        search_bar = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._1i0-u > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)")))
        search_bar.click()
        message_search = self.browser.find_element_by_css_selector("._1iopp > div:nth-child(1) > label:nth-child(4) > input:nth-child(1)")
        message_search.clear()
        message_search.send_keys(message + Keys.ENTER)
        try:
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/span/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div[1]/span/span/span")))
            return True
        except TimeoutException:
            return False

    def emojify(self, message):
        with open("emoji.json") as emojies:
            emoji = json.load(emojies)
        for em in emoji:
            message = message.replace(em, emoji[em])
        return message
