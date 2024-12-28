from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import logging
import requests
import time
import datetime
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class WebInteractions:
    def __init__(self, driver, context=None):
        self.driver = driver
        self.context = context

    def open_url(self, url):
        self.driver.get(url)

    def wait_for_element(self, locator, timeout=12):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def enter_text(self, locator, text):
        element = self.wait_for_element(locator)
        element.send_keys(text)

    def click_element(self, locator):
        element = self.wait_for_element(locator)
        element.click()

    def get_text(self, locator):
        element = self.wait_for_element(locator)
        return element.text

    def take_screenshot(self, filename="screenshot.png"):
        self.driver.save_screenshot(filename)

    def take_screenshot_on_error(self, filename_prefix="error_screenshot"):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshots_folder = os.path.join(os.path.dirname(__file__), "../", 'screenshots')
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)
        filename = os.path.join(screenshots_folder, f"{filename_prefix}_{timestamp}.png")

        try:
            self.driver.save_screenshot(filename)
            logging.info(f"Screenshot captured: {filename}")
        except Exception as e:
            logging.error(f"Failed to capture screenshot: {e}")


    def wait_on_screen(self, seconds):
        time.sleep(int(seconds))

    def get_current_page_url(self):
        return self.driver.current_url
    
    def clear_text_js(self, locator):
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].value = '';", element)
    
    def set_text_via_js(self, locator, text):
        element = self.wait_for_element(locator)
        self.clear_text_js(locator)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, text)

    def send_text_with_actions(self, locator, text):
        element = self.wait_for_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().send_keys(text).perform()
        
    def hover_on_the_element(self, locator):
        element = self.wait_for_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def wait_until_clickable(self, locator, timeout=12):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def slow_type(self, locator, text):
        element = self.wait_for_element(locator)
        for char in text:
            # self.enter_text(locator, char)
            element.send_keys(char)
            time.sleep(0.8)

    # iFrame methods
    def switch_to_iframe(self, frame_webelement):
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it(frame_webelement))
        self.wait_on_screen(2)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    #  dropdown helpers
    def select_by_visible_text(self, dropdown_locator, value):
        element = self.wait_for_element(dropdown_locator)
        dropdown = Select(element)
        dropdown.select_by_visible_text(value)

    def select_by_visible_index(self, dropdown_locator, index):
        self.driver.switch_to.default_content(index)
    
    def press_tab_on_page(self):
        ActionChains(self.driver).send_keys(Keys.TAB).perform()

    def press_enter_on_page(self):
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    def enter_text_at_focus(self, text):
        script = f"document.activeElement.value = '{text}'"
        self.driver.execute_script(script)

    def enter_text_with_focus(self, text):
        self.driver.execute_script("""
            const focusedElement = document.activeElement;
            focusedElement.value = arguments[0];
            const inputEvent = new Event('input', { bubbles: true });
            const keyupEvent = new Event('keyup', { bubbles: true });
            const changeEvent = new Event('change', { bubbles: true });
            focusedElement.dispatchEvent(inputEvent);
            focusedElement.dispatchEvent(keyupEvent);
            focusedElement.dispatchEvent(changeEvent);
        """, text)

    def remove_text_at_focus(self):
        script = f"document.activeElement.value = ''"
        self.driver.execute_script(script)

    def check_element_visibility(self, locator):
        element = self.wait_for_element(locator)
        return element.is_displayed()

    def scroll_to_element(self, locator):
        # element = self.driver.find_element(*locator)
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def login_with_tab(self, username, password):
        self.press_tab_on_page() 
        self.enter_text_at_focus(username)
        self.press_tab_on_page()
        self.enter_text_at_focus(password)
        self.press_tab_on_page()
        self.press_enter_on_page()
        self.wait_on_screen(2.5)

    def enter_mfa_code(self, mfa_token):
        self.press_tab_on_page()
        self.enter_text_with_focus(mfa_token)
        self.press_enter_on_page()
        self.wait_on_screen(5)

    def is_element_not_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return False
        except TimeoutException:
            return True
        
    def wait_till_element_invisible(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        
    def is_element_not_visiblee(self, locator, timeout=5):
        try:
            self.wait_for_element
            return False
        except TimeoutException:
            return True
        
    def verify_links_status(self, links):
        broken_links = []
        for link in links:
            try:
                response = requests.head(link, timeout=5)
                if response.status_code >= 400:
                    broken_links.append((link, response.status_code))
            except requests.RequestException as e:
                broken_links.append((link, str(e)))

        if broken_links:
            raise AssertionError(f"Broken links found: {broken_links}")

    def get_all_hyperlinks(self, locator):
        elements = self.driver.find_elements(*locator)
        return [element.get_attribute('href') for element in elements]
    
    def get_custom_table_data(self, container_locator):
        container = self.wait_for_element(container_locator)
        # container = self.driver.find_element(*container_locator)  # Locate the container
        rows = container.find_elements(By.CLASS_NAME, "row")  # Find all row elements

        table_data = {}

        for row in rows:
                try:
                    key_element = row.find_element(By.CSS_SELECTOR, "div.col-12.col-sm-12.col-md-6.col-lg-4")
                    key = key_element.text.strip().replace(":", "")
                    value_element = row.find_element(By.CSS_SELECTOR, "div.col")
                    value = value_element.text.strip()
                    table_data[key] = value
                except Exception as e:
                    print(f"Skipping row due to error: {e}")
        # logging.info(f"table data : {table_data}")
        return table_data
    
    # extracts adjacent values from the table
    def get_value_from_table(self, field_name):
        elements = f"//*[text()='{field_name}']//following-sibling::td"
        print(f"### Updated locator: {elements}") 
        try:   
            value = self.driver.find_element(By.XPATH, elements).text
            return value
        except Exception as e:
            print(f"Invalid value found: {e}")         
            return None