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
import requests

class UserInfoHandler:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_status(self, name):
        response = requests.get(f"{self.api_url}/get_status", params={"name": name, "api_key": self.api_key})
        if response.status_code == 200:
            return response.json().get("status", "Status não disponível")
        else:
            return "Erro ao obter o status"

    def get_last_seen(self, name, timeout=10):
        try:
            response = requests.get(f"{self.api_url}/get_last_seen", params={"name": name, "api_key": self.api_key}, timeout=timeout)
            if response.status_code == 200:
                return response.json().get("last_seen", "Última visualização não disponível")
            else:
                return "Erro ao obter a última visualização"
        except requests.Timeout:
            return "Requisição expirou"

    def get_profile_pic(self, name):
        response = requests.get(f"{self.api_url}/get_profile_pic", params={"name": name, "api_key": self.api_key})
        if response.status_code == 200:
            return response.json().get("profile_pic_url", "Foto de perfil não disponível")
        else:
            return "Erro ao obter a foto de perfil"

