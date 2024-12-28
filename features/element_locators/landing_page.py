from selenium.webdriver.common.by import By

class Landing_Locators:
    username = (By.NAME, "username")
    password = (By.NAME, "password")
    login_btn = (By.CSS_SELECTOR, "button[type='submit']")
    invalid_login_alert = (By.XPATH, "//*[text()='Invalid credentials']")
