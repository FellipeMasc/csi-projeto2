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
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from WhatsAppElements import *

class GroupHandler:
    def __init__(self, browser, timeout):
        self.browser = browser
        self.timeout = timeout
    
    def create_group(self, group_name, members):
        more = self.browser.find_element_by_css_selector("#side > header > div._20NlL > div > span > div:nth-child(3) > div > span")
        more.click()
        chains = ActionChains(self.browser)
        chains.send_keys(Keys.ARROW_DOWN + Keys.ENTER)
        chains.perform()
        for member in members:
            contact_name = self.browser.find_element_by_css_selector("._16RnB")
            contact_name.send_keys(member + Keys.ENTER)
        time.sleep(3)
        next_step = self.browser.find_element_by_css_selector("._3hV1n > span:nth-child(1)")
        next_step.click()
        group_text = self.browser.find_element_by_css_selector(".bsmJe > div:nth-child(2)")
        group_text.send_keys(group_name + Keys.ENTER)
    
    def set_group_picture(self, group_name, picture_location):
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(group_name + Keys.ENTER)  # we will send the group name to the input key box
        try:
            menu_xpath = '/html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[3]/div/span'
            group_info_xpath = '/html/body/div[1]/div/div/div[4]/div/header/div[3]/div/div[3]/span/div/ul/li[1]/div'
            image_input_xpath = '/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[1]/div[1]/div/input'
            zoom_out_xpath = '/html/body/div[1]/div/span[2]/div/div/div/div/div/div/span/div/div/div[1]/div[1]/div[2]/span'
            save_btn_xpath = '/html/body/div[1]/div/span[2]/div/div/div/div/div/div/span/div/div/div[2]/span/div/div'
            exit_group_info_xpath = '/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/header/div/div[1]/button/span'

            # open group info
            menu = self.browser.find_element_by_xpath(menu_xpath)
            menu.click()
            time.sleep(1)
            group_info = self.browser.find_element_by_xpath(group_info_xpath)
            group_info.click()

            # find image input and send picture path
            time.sleep(1)
            image_input = self.browser.find_element_by_xpath(image_input_xpath)
            image_input.send_keys(picture_location)

            # zoom out picture and save
            time.sleep(1)
            zoom_out = self.browser.find_element_by_xpath(zoom_out_xpath)
            for i in range(0, 5):
                zoom_out.click()
            save_btn = self.browser.find_element_by_xpath(save_btn_xpath)
            save_btn.click()

            # close the group info
            time.sleep(1)
            exit_group_info = self.browser.find_element_by_xpath(exit_group_info_xpath)
            exit_group_info.click()
        except (NoSuchElementException, ElementNotVisibleException) as e:
            print(str(e))

    def join_group(self, invite_link):
        self.browser.get(invite_link)
        try:
            Alert(self.browser).accept()
        except:
            print("No alert Found")
        join_chat = self.browser.find_element_by_css_selector("#action-button")
        join_chat.click()
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/span[3]/div/div/div/div/div/div/div[2]/div[2]')))
        join_group = self.browser.find_element_by_xpath('//*[@id="app"]/div/span[3]/div/div/div/div/div/div/div[2]/div[2]')
        join_group.click()

    def get_invite_link_for_group(self, groupname):
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(groupname + Keys.ENTER)
        self.browser.find_element_by_css_selector("#main > header > div._5SiUq > div._16vzP > div > span").click()
        try:
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#app > div > div > div.MZIyP > div._3q4NP._2yeJ5 > span > div > span > div > div > div > div:nth-child(5) > div:nth-child(3) > div._3j7s9 > div > div")))
            invite_link = self.browser.find_element_by_css_selector("#app > div > div > div.MZIyP > div._3q4NP._2yeJ5 > span > div > span > div > div > div > div:nth-child(5) > div:nth-child(3) > div._3j7s9 > div > div")
            invite_link.click()
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                    (By.ID, "group-invite-link-anchor")))
            link = self.browser.find_element_by_id("group-invite-link-anchor")
            return link.text
        except:
            print("Cannot get the link")
    
    def exit_group(self, group_name):
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(group_name + Keys.ENTER)
        self.browser.find_element_by_css_selector("._2zCDG > span:nth-child(1)").click()
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._1CRb5:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)")))
        time.sleep(3)
        _exit = self.browser.find_element_by_css_selector("div._1CRb5:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)")
        _exit.click()
        WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._1WZqU:nth-child(2)")))
        confirm_exit = self.browser.find_element_by_css_selector("div._1WZqU:nth-child(2)")
        confirm_exit.click()

    def participants_count_for_group(self, group_name):
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(group_name+Keys.ENTER)  # we will send the name to the input key box
        # some say this two try catch below can be grouped into one
        # but I have some version specific issues with chrome [Other element would receive a click]
        # in older versions. So I have handled it spereately since it clicks and throws the exception
        # it is handled safely
        try:
            click_menu = WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]/div[2]/span")))
            click_menu.click()
        except TimeoutException:
            raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        except NoSuchElementException as e:
            return "None"
        except Exception as e:
            return "None"

        participants_selector = "/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/div/section/div[7]/div[1]/div/div[1]/span"
        elemento = WebDriverWait(self.browser, 100).until(
        EC.visibility_of_element_located((By.XPATH, participants_selector))
        )
        return elemento.text.split(': ')[1]
    
    def get_group_participants(self, group_name):
        search = self.browser.find_element(*WhatsAppElements.search)
        time.sleep(4)
        search.send_keys(group_name+Keys.ENTER)
        # try:
        #     click_menu = WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
        #         (By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]/div[2]/span")))
        #     time.sleep(4)
        #     click_menu.click()
        # except TimeoutException:
        #     raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        
        participants_menu = WebDriverWait(self.browser,self.timeout).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]/div[2]/span")))
        return participants_menu.text
        # try:
        #     click_menu = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
        #         (By.CSS_SELECTOR, "#main > header > div._1WBXd > div._2EbF- > div > span")))
        #     click_menu.click()
        # except TimeoutException:
        #     raise TimeoutError("Your request has been timed out! Try overriding timeout!")
        # except NoSuchElementException as e:
        #     return "None"
        # except Exception as e:
        #     return "None"
        # participants = []
        # scrollbar = self.browser.find_element_by_css_selector("#app > div > div > div.MZIyP > div._3q4NP._2yeJ5 > span > div > span > div > div")
        # for v in range(1, 70):
        #     print(v)
        #     self.browser.execute_script('arguments[0].scrollTop = ' + str(v * 300), scrollbar)
        #     time.sleep(0.10)
        #     elements = self.browser.find_elements_by_tag_name("span")
        #     for element in elements:
        #         try:
        #             html = element.get_attribute('innerHTML')
        #             soup = BeautifulSoup(html, "html.parser")
        #             for i in soup.find_all("span", class_="_3TEwt"):
        #                 if i.text not in participants:
        #                     participants.append(i.text)
        #                     print(i.text)
        #         except Exception as e:
        #             pass
        #     elements = self.browser.find_elements_by_tag_name("div")
        #     for element in elements:
        #         try:
        #             html = element.get_attribute('innerHTML')
        #             soup = BeautifulSoup(html, "html.parser")
        #             for i in soup.find_all("div", class_="_25Ooe"):
        #                 j = i.find("span", class_="_1wjpf")
        #                 if j:
        #                     j = j.text
        #                     if "\n" in j:
        #                         j = j.split("\n")[0].strip()
        #                         if j not in participants:
        #                             participants.append(j)
        #                             print(j)
        #         except Exception as e:
        #             pass
        # return participants
