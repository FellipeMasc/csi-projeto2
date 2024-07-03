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

class UnreadMessagesHandler:
    def __init__(self, browser, timeout):
        self.browser = browser
        self.timeout = timeout
    
    def unread_usernames(self, scrolls=100):
        self.browser.refresh()
        Alert(self.browser).accept()
        initial = 10
        usernames = []
        for i in range(0, scrolls):
            self.browser.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            for i in soup.find_all("div", class_="_2EXPL CxUIE"):
                if i.find("div", class_="_2FBdJ"):
                    username = i.find("div", class_="_25Ooe").text
                    usernames.append(username)
            initial += 10
        usernames = list(set(usernames))
        return usernames
