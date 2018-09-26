from behave import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
import unittest

validUsername = 'test'
validPassword = 'test'

@given('I have navigated to the CAIRIS web application')
def step_impl(context):
  NavigateToApp(context)

@when('I supply valid credentials')
def step_impl(context):
  EnterValidCredentials(context)

@then('I am granted access to the application')
def step_impl(context):
  LoggedIn(context)

@when('I supply {username} and {password}')
def step_impl(context, username, password):
  EnterCredentials(context, username, password)
  ClickButtonWithId(context, 'submit')

@then('I am refused access to the application')
def step_impl(context):
  assert OnLandingPage(context) is True

@given('I have successfully authenticated with CAIRIS')
def step_impl(context):
  NavigateToApp(context)
  EnterValidCredentials(context)
  LoggedIn(context)

@when('I click logout')
def step_impl(context):
  logout = context.browser.find_element_by_id('logoutClick')
  logout.click()

@then('I am returned to the landing page')
def step_impl(context):
  assert OnLandingPage(context) is True

def NavigateToApp(context):
  context.browser.get("https://demo.cairis.org")

def EnterValidCredentials(context):
  EnterCredentials(context, validUsername, validPassword)
  ClickButtonWithId(context, 'submit')

def EnterCredentials(context, username, password):
  usernameEl = FindElementById(context, 'email')
  passwordEl = FindElementById(context, 'password')
  
  EnterText(usernameEl, username)
  EnterText(passwordEl, password)

def LoggedIn(context):
  WaitForSpinningWheelOfDoom(context)
  ClickButtonWithId(context, 'homeClick')

def OnLandingPage(context):
  WaitForVisibleById(context, 'email')
  WaitForVisibleById(context, 'password')
  return True

def ClickButtonWithId(context, id):
  button = FindElementById(context, id)
  button.click()

def FindElementById(context, id):
  return context.browser.find_element_by_id(id)

def EnterText(element, text):
  element.send_keys(text)

def ElementWithIdInvisible(context, id):
  elelement = FindElementById(context, id);
  assert element.is_displayed is False

def WaitForSpinningWheelOfDoom(context):
  spinningWheelOfDoom = 'displayWrapper'
  WaitForInvisibleByClass(context, 'divLoading')

def WaitForVisibleByClass(context, className):
  return WaitForVisibleStateByClass(context, className, True)

def WaitForInvisibleByClass(context, className):
  return WaitForVisibleStateByClass(context, className, False)

def WaitForVisibleStateByClass(context, className, displayState):
  if(displayState == True):
    element = WebDriverWait(context.browser, 30, 0.5, (ElementNotVisibleException)).until(lambda x: x.find_element_by_class_name(className).is_displayed())
  else:
    element = WebDriverWait(context.browser, 30, 0.5, (ElementNotVisibleException)).until_not(lambda x: x.find_element_by_class_name(className).is_displayed())
  return element

def WaitForVisibleById(context, id):
  return WaitForVisibleStateById(context, id, True)

def WaitForInvisibleById(context, id):
  return WaitForVisibleStateById(context, id, False)

def WaitForVisibleStateById(context, id, displayState):
  if(displayState == True):
    element = WebDriverWait(context.browser, 30, 0.5, (ElementNotVisibleException)).until(lambda x: x.find_element_by_id(id).is_displayed())
  else:
    element = WebDriverWait(context.browser, 30, 0.5, (ElementNotVisibleException)).until_not(lambda x: x.find_element_by_id(id).is_displayed())
  return element    