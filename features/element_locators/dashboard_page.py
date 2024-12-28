from selenium.webdriver.common.by import By


class Dashboard_Locators:
    user_name = (By.XPATH, "//p[@class='oxd-userdropdown-name']")
    dashboard = (By.XPATH, "//h6[text()='Dashboard']")

