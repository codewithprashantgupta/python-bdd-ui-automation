import os
import logging
import configparser
import datetime
from behave import fixture
import requests, json, re, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from utilities.web_interactions import WebInteractions


logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()

hidden_config_file_path = os.path.join(os.path.dirname(__file__), '.config.ini')
default_config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')


if os.path.exists(hidden_config_file_path):
    config.read(hidden_config_file_path)
else:
    config.read(default_config_file_path)

 
def before_all(context):
    context.stage = context.config.userdata.get("stage", "test")
    context.url = config[context.stage]['url']
    context.secret = config[context.stage]['secret']
    context.username = config[context.stage]['username']
    context.password = config[context.stage]['password']

def before_feature(context, feature):
    context.feature_organizations = []

def before_step(context, step):
    context.step = step
    context.step_number = context.scenario.steps.index(step) + 1

def before_scenario(context, scenario):
    context.scenario_organizations = []
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36")
    # options.add_argument("--headless")
    service = Service("./test_data/driver/chromedriver")
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.maximize_window()
    context.helper = WebInteractions(context.driver, context)


def after_scenario(context, scenario):
    if 'response' in context:
        save_response(context)
    context.driver.quit()

def after_step(context, step):
    if step.status == "failed":
        context.helper.take_screenshot_on_error(f"step_failure_{step.name}")

def after_feature(context, feature):
    
