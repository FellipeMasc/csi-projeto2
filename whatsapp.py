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
from WebDriverHandler import *
from MessageHandler import *
from GroupHandler import *
from UserInfoHandler import *
from StarredMessagesHandler import *
from UnreadMessagesHandler import *
from UtilityHandler import *

class WhatsApp:
    def __init__(self, wait, screenshot=None, session=None):
        self.timeout = 100
        self.web_driver_handler = WebDriverHandler(session)
        self.browser = self.web_driver_handler.initialize_driver()
        WebDriverWait(self.browser, wait).until(EC.presence_of_element_located(WhatsAppElements.search))
        if screenshot is not None:
            self.browser.save_screenshot(screenshot)
        
        self.message_handler = MessageHandler(self.browser, self.timeout)
        self.group_handler = GroupHandler(self.browser, self.timeout)
        self.starred_messages_handler = StarredMessagesHandler(self.browser, self.timeout)
        self.unread_messages_handler = UnreadMessagesHandler(self.browser, self.timeout)
        self.utility_handler = UtilityHandler(self.browser, self.timeout)
        # self.user_info_handler = UserInfoHandler(self.browser, self.timeout)
    
    def send_message(self, name, message):
        return self.message_handler.send_message(name, message)
    
    def send_blind_message(self, message):
        return self.message_handler.send_blind_message(message)
    
    def send_picture(self, name, picture_location, caption=None):
        return self.message_handler.send_picture(name, picture_location, caption)
    
    def send_document(self, name, document_location):
        return self.message_handler.send_document(name, document_location)
    
    def send_anon_message(self, phone, text):
        return self.message_handler.send_anon_message(phone, text)
    
    def is_message_present(self, username, message):
        return self.message_handler.is_message_present(username, message)

    def create_group(self, group_name, members):
        return self.group_handler.create_group(group_name, members)
    
    def set_group_picture(self, group_name, picture_location):
        return self.group_handler.set_group_picture(group_name, picture_location)
    
    def join_group(self, invite_link):
        return self.group_handler.join_group(invite_link)

    def get_invite_link_for_group(self, groupname):
        return self.group_handler.get_invite_link_for_group(groupname)
    
    def exit_group(self, group_name):
        return self.group_handler.exit_group(group_name)
    
    def participants_count_for_group(self, group_name):
        return self.group_handler.participants_count_for_group(group_name)
    
    def get_group_participants(self, group_name):
        return self.group_handler.get_group_participants(group_name)
    
    def get_status(self, name):
        return self.user_info_handler.get_status(name)
    
    def get_last_seen(self, name, timeout=10):
        return self.user_info_handler.get_last_seen(name, timeout)
    
    def get_profile_pic(self, name):
        return self.user_info_handler.get_profile_pic(name)
    
    def get_starred_messages(self, delay=10):
        return self.starred_messages_handler.get_starred_messages(delay)
    
    def unread_usernames(self, scrolls=100):
        return self.unread_messages_handler.unread_usernames(scrolls)
    
    def clear_chat(self, name):
        return self.utility_handler.clear_chat(name)
    
    def goto_main(self):
        return self.utility_handler.goto_main()
    
    def override_timeout(self, new_timeout):
        return self.utility_handler.override_timeout(new_timeout)
    
    def emojify(self, message):
        return self.utility_handler.emojify(message)
    
    def quit(self):
        self.browser.quit()

# Uso da classe WhatsApp:
whatsapp = WhatsApp(wait=100)
texto = "Olá, esta é uma mensagem de teste.\n"
    
whatsapp.send_message("Holder T26", texto)
    
# participants = whatsapp.get_group_participants("Computos 26")

# print(participants)