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

class WebDriverHandler:
    def __init__(self, session=None):
        self.session = session
        self.browser = None
    
    def initialize_driver(self):
        chrome_options = Options()
        if self.session:
            chrome_options.add_argument(f"--user-data-dir={self.session}")
        self.browser = webdriver.Chrome(executable_path = "C:\ITA\Csi-projeto2\chromedriver-win64\chromedriver.exe")
        self.browser.get("https://web.whatsapp.com/")
        return self.browser
