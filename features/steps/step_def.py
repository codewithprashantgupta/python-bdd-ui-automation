from behave import given, when, then
from features.element_locators.landing_page import Landing_Locators as land_page
from features.element_locators.dashboard_page import Dashboard_Locators as dash_page
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@given(u'the user is on the OrangeHRM landing page')
def step_impl(context):
    context.helper.open_url(context.url)
    context.helper.wait_on_screen(2)

@when(u'the user enters "{uname}" as the username and "{pwd}" as the password')
def step_impl(context, uname, pwd):
    context.helper.click_element(land_page.username)
    context.helper.enter_text(land_page.username, uname)
    context.helper.click_element(land_page.password)
    context.helper.enter_text(land_page.password, pwd)

@when(u'clicks the Login button')
def step_impl(context):
    context.helper.click_element(land_page.login_btn)
    

@then(u'the user is navigated to the homepage')
def step_impl(context):
    context.helper.wait_for_element(dash_page.dashboard)
    assert context.helper.check_element_visibility(dash_page.dashboard) is True  
    assert str(context.helper.get_current_page_url()) == str("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")


@then(u'the user gets an error message "{err_msg}"')
def step_impl(context, err_msg):
    assert context.helper.check_element_visibility(land_page.invalid_login_alert) is True

