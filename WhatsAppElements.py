from selenium.webdriver.common.by import By

class WhatsAppElements:
    # div._ak9t > div > label > div
    # search = (By.CSS_SELECTOR, "#side > div.copyable-text.selectable-text")
    search = (By.CSS_SELECTOR, "div[role='textbox'] > p.selectable-text.copyable-text")
    attach_icon = (By.CSS_SELECTOR, ".bDS3i > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)")