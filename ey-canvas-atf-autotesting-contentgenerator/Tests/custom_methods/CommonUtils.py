from datetime import datetime
import time
from scriptless.Core.framework.data_handler import Data_handler
from scriptless.Core.library.common.CustomBase import CustomBase
from scriptless.Core.framework.logger import LOGGER  
from robot.utils.asserts import assert_equal,fail,assert_true
from time import sleep
from selenium.webdriver.common.by import By
from scriptless.Core.library.common.CustomBase import CustomBase
from scriptless.Core.library.common.ExtendedSeleniumLibrary import ExtendedSeleniumLibrary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import jsonpath
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException,StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class CommonUtils(CustomBase):

  MAX_RETRIES = 3

  def _webelement_input_text(self,text,input_web_element,clear_text=True):
    """
    This method types a text inside a web element of input type
    text (str): String to be introduced in to de input element, acept Keys().ENTER to
    input_web_element (Selenium web_element): The input web element, or this method suport locator too
    """
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    extendedSeleniumLibrary.wait_for_element_to_be_visible(input_web_element)
    if clear_text:
      extendedSeleniumLibrary.clear_text(input_web_element)
    extendedSeleniumLibrary.send_keys(input_web_element,text)


  def _get_web_element(self,driver,locator,time_out = '30', retry_count=0):
    """
    This method receives locators from scriptles and returns the corresponding web element, it supports only the scriptles locators syntax 
    "xpath://example"
    "id:example"
    "css:.example"
    driver (Selenium WebDriver): current Web Driver
    locator (str): locator of the element
    returns (Webelement)
    """
    if retry_count > self.MAX_RETRIES:
       raise StaleElementReferenceException("Exceeded maximum retry count for StaleElementReferenceException")

    locator_strategy = CommonUtils()._get_locator_strategy(locator)

    try:
        wait = WebDriverWait(driver, timeout=time_out)
        web_element = wait.until(EC.presence_of_element_located((locator_strategy['locator_type'], locator_strategy['element_locator'])))
        self.log_message(f"The element was found: {locator}")
        return web_element
    except StaleElementReferenceException:
        self.log_message(f"StaleElementReferenceException occurred while waiting for element: {locator}")
        return self._get_web_element(driver, locator, time_out, retry_count + 1)


  def _get_web_elements(self,driver,locator,time_out = '30'):
    """
    This method receives locators from scriptles and returns the corresponding web elements, it supports only the scriptles locators syntax 
    "xpath://example"
    "id:example"
    "css:.example"
    driver (Selenium WebDriver): current Web Driver
    locator (str): locator of the element
    returns (Webelement)
    """
    try :
      web_elements = None
      locator_startergy = CommonUtils()._get_locator_strategy(locator)
      wait = WebDriverWait(driver, timeout=int(time_out), poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
      wait.until(EC.visibility_of_any_elements_located((locator_startergy['locator_type'], locator_startergy['element_locator'])))
      web_elements = driver.find_elements(locator_startergy['locator_type'],locator_startergy['element_locator'])
      return web_elements
    except:
      self.log_message(f"Elements {locator} not Found")
      return None
  

  def _get_locator_strategy(self,locator):
    """
    This function return a dic with 'locator_type' and 'element_locator'
    locator (str): locator in scriptless format
    return (dic)
    """
    try:
      locator_data = re.search(r'^([\w_+?]{2,12}):(.*)$', locator)
      locator_type = locator_data.group(1) # type: ignore
      element_locator = locator_data.group(2) # type: ignore
      locator_startergy ={
        'locator_type':locator_type,
        'element_locator':element_locator
        }
      return locator_startergy
    except:
      fail(f'All locators must be defined in the "Elements" section in Scriptles') #
    

  def calendar_date_picker(self,locator,date):
    """
    This function allows you to select a specific date from a calendar.
    locator (srt): the locator of the element that contains the calendar
    date (str): The date to enter in the calendar
    """
    format_data = "%Y-%m-%d %H:%M:%S.%f"
    time_data = datetime.strptime(date, format_data)
    year = str(time_data.year)
    month = str(time_data.month)
    day = str(time_data.day)
    driver = self.get_webdriver()
    current_calendar_locator =  Data_handler().parse_parameter("<%elm:calendar Date:section_calendar_be_open%>", "").replace("xpath:", "").replace("\n", "")
    locator = locator.replace("xpath:", "").replace("\n", "")
    calendar = driver.find_element(By.XPATH,locator)
    calendar.click()
    locator_btn_date_above = Data_handler().parse_parameter("<%elm:calendar Date:btn_date_above%>", "").replace("xpath:", "").replace("\n", "")
    btn_date_above= calendar.find_element(By.XPATH,current_calendar_locator + locator_btn_date_above)
    btn_date_above.click()
    sleep(0.2)
    btn_date_above.click()
    locator_btn_date_year = Data_handler().parse_parameter("<%elm:calendar Date:btn_date_year%>", "").replace('{{year}}', year).replace("xpath:", "").replace("\n", "")
    btn_date_year= calendar.find_element(By.XPATH,current_calendar_locator + locator_btn_date_year)
    btn_date_year.click()
    locator_btn_date_month = Data_handler().parse_parameter("<%elm:calendar Date:btn_date_month%>", "").replace('{{month}}', month).replace("xpath:", "").replace("\n", "")
    btn_date_month = calendar.find_element(By.XPATH,locator_btn_date_month)
    btn_date_month.click()
    locator_btn_date_day = Data_handler().parse_parameter("<%elm:calendar Date:btn_date_day%>", "").replace('{{day}}', day).replace("xpath:", "").replace("\n", "")
    btn_date_day = calendar.find_element(By.XPATH,locator_btn_date_day)
    btn_date_day.click()
    print(f"date: {year}-{month}-{day}")
    selected_year = calendar.find_element(By.XPATH,locator + "//input[@aria-label='Year']")
    selected_month = calendar.find_element(By.XPATH,locator + "//input[@aria-label='Month']")
    selected_day = calendar.find_element(By.XPATH,locator + "//input[@aria-label='Day']")
    selected_date = selected_year.get_attribute('value') +" "+selected_month.get_attribute('value')+ " "+ selected_day.get_attribute('value')
    expected_date = f"{year} {month} {day}"
    assert_equal(selected_date,expected_date)
  
  	
  def input_text_search_bar(self, text_to_serch, search_bar_locator,results_section_locator, loader_content_locator, searching_time = '60', reload_required= 'False'):
    """
     This function performs a search in a "Search Bar" and waits for the result to be present on the current page.
    text_to_serch (str): Text to be searched for
    search_bar_locator (str): The search bar locator (SUPORTS XPATH only)
    loader_content_locator (str):  
    results_section_locator (str): The section where the searched item will appear
    searching_time (str): Time that the automation wait for the results
    reload_requerided (bool): True if you need to reload the page if the search bar is not present
                              False if don't need to reload the page before te search
    """
    driver = self.get_webdriver()
    
    if reload_required:
      CommonUtils()._wait_and_refresh_for_page_to_load(search_bar_locator)

    search_bar = CommonUtils()._get_web_element(driver,search_bar_locator,searching_time)
    CommonUtils()._webelement_input_text(text_to_serch,search_bar)
    CommonUtils()._webelement_input_text(Keys().ENTER,search_bar)
    loader = CommonUtils()._get_locator_strategy(loader_content_locator)
    wait = WebDriverWait(driver, timeout=int(searching_time), poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
    wait.until(EC.invisibility_of_element_located((loader['locator_type'], loader['element_locator'])))
    results_section = CommonUtils()._get_locator_strategy(results_section_locator)
    wait.until(EC.visibility_of_element_located((results_section['locator_type'], results_section['element_locator'])))

    try:
      result_section = CommonUtils()._get_web_element(driver,results_section_locator,searching_time)
      extendedSeleniumLibrary = ExtendedSeleniumLibrary()
      text = ''
      cont = 0
      while text == '' and cont < int(searching_time)*5:
        sleep(0.2)
        text =  extendedSeleniumLibrary.get_element_text(result_section).replace("\n","").replace(" ","")
        cont += 1
        
    except:
      fail(f"the search did not generate results in the selected section {results_section_locator}")
    assert_true(text.__contains__(text_to_serch.replace(" ","")))

  def click_element_and_wait(self,locator,loader_locator,time_out):
    """
    locator (str): The input locator in scriptles format
    loader_locator (str): locator in Scriptless format that you need to be invisible
    time_out (int): time in seconds that the automation wait for the element
    """
    driver = self.get_webdriver()
    element = self._get_web_element(driver,locator,time_out)
    try:
      element.click()
    except:
      element = self._get_web_element(driver,locator,time_out)
      element.click()
    if loader_locator is not None:
      self.wait_for_element_not_visible(loader_locator,time_out)
  
  def click_element_with_js(self, locator, loader_locator, time_out):
    """
    locator (str): The input locator in scriptles format
    loader_locator (str): locator in Scriptless format that you need to be invisible
    time_out (int): time in seconds that the automation wait for the element
    """
    driver = self.get_webdriver()
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    element = CommonUtils()._get_web_element(driver, locator, time_out)

    try:
        driver.execute_script("arguments[0].click();", element)
    except:
        extendedSeleniumLibrary.click_button(element)

    if loader_locator is not None:
        CommonUtils().wait_for_element_not_visible(loader_locator, time_out)


  def input_text(self,text,locator,time_out,clear_input=True): 
    """
    This method types a text inside a locator in Scriptles Format
    text (str): String to be introduced in to de input element, yo can send the Key "ENTER"
    locator (Selenium web_element): The input locator in scriptles format
    time_out (int): time in seconds that the automation wait for the element
    """
    driver = self.get_webdriver()
    input_web_element = CommonUtils()._get_web_element(driver,locator,time_out)
    CommonUtils()._webelement_input_text(text,input_web_element,clear_input)


  def input_text_and_enter(self,text,locator,time_out,clear_input=True):
    """
    This method types a text inside a locator in Scriptles Format
    text (str): String to be introduced in to de input element, yo can send the Key "ENTER"
    locator (str): The input locator in scriptles format
    """
    driver = self.get_webdriver()
    input_web_element = CommonUtils()._get_web_element(driver,locator,time_out)
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    extendedSeleniumLibrary.wait_for_element_to_be_visible(input_web_element)
    CommonUtils()._webelement_input_text(text,input_web_element,clear_input)
    extendedSeleniumLibrary.input_text(input_web_element,Keys().ENTER,False) 

      
  def select_value_in_drop_down(self,text,locator,time_out):
    """
    This method types a text inside a locator in Scriptles Format
    text (str): String to be introduced in to de input element, yo can send the Key "ENTER"
    locator ( str): The input locator in scriptles format
    time_out (int): time in seconds that the automation wait for the element
    """
    CommonUtils().input_text_and_enter(text,locator,time_out)


  def select_check_box(self,locator,time_out):
    """
    locator (str): The input locator in scriptles format
    time_out (int): time in seconds that the automation wait for the element
    """
    driver = self.get_webdriver()
    element = CommonUtils()._get_web_element(driver,locator,time_out)
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    extendedSeleniumLibrary.wait_for_element_to_be_visible(element)
    extendedSeleniumLibrary.select_checkbox(element)
    extendedSeleniumLibrary.checkbox_should_be_selected(element)

  def unselect_check_box(self,locator,time_out):
    """
    locator (str): The input locator in scriptles format
    time_out (int): time in seconds that the automation wait for the element
    """
    driver = self.get_webdriver()
    element = CommonUtils()._get_web_element(driver,locator,time_out)
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    extendedSeleniumLibrary.unselect_checkbox(element)
    extendedSeleniumLibrary.checkbox_should_not_be_selected(element)


  def get_text(self,locator,time_out):
    """
    locator (str): The input locator in scriptles format
    time_out (int): time in seconds that the automation wait for the element
    return (str)
    """
    driver = self.get_webdriver()
    element = CommonUtils()._get_web_element(driver,locator,time_out)
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    text = extendedSeleniumLibrary.get_element_text(element)
    return text


  def is_element_displayed(self,locator,time_out):
    """
    This method returns a bool if the element is present on the screen or not
    locator (str): The input locator in scriptles format
    time_out (int): time in seconds that the automation wait for the element
    return (bool)
    """
    driver = self.get_webdriver()
    try:
        element = CommonUtils()._get_web_element(driver, locator, time_out)
        element_displayed = element.is_displayed()
        return element_displayed
    except TimeoutException:
        self.log_message(f"TimeoutException occurred for is_element_displayed: {locator}")
        return False
    except Exception as e:
        self.log_message(f"Exception occurred for is_element_displayed: {locator} - {str(e)}")
        return False  


  def get_value(self,locator,time_out):
    """
    This method returns the value attribute of the element identified by locator
    locator (str): The input locator in scriptles format
    time_out (int): time in seconds that the automation wait for the element
    return  (str)
    """
    driver = self.get_webdriver()
    element = CommonUtils()._get_web_element(driver,locator,time_out)
    try:
      value = element.get_attribute('value')
    except:
      value = element.get_property('value')
    return value


  def get_attribute(self,locator,attribute,time_out):
    """
    This method returns the value of attribute from the element locator.
    locator (str): The input locator in scriptles format
    attribute (str) The attribute of the element 
    time_out (int): time in seconds that the automation wait for the element
    return (srt)
    """
    driver = self.get_webdriver()
    element = CommonUtils()._get_web_element(driver,locator,time_out)
    attribute = element.get_attribute(attribute)
    return attribute


  def _wait_and_refresh_for_page_to_load(self,locator):
    """
    This method waits for an element to be visible, if the element is not visible it reloads the page and tries again
    locator (str): The input locator in scriptles format
    """
    element = None
    retry_counter = Data_handler().get_env_var_value("maximumAmountOfRetriesWhileEnteringAPage")
    retries = retry_counter
    driver = self.get_webdriver()
    wait_time = Data_handler().get_env_var_value("veryLongTimeOut")
    #driver.implicitly_wait(int(wait_time))
    while element is None:
      try:
        element =  CommonUtils()._get_web_element(driver, locator) 
      except:
        page_state = driver.execute_script('return document.readyState;')
        if(page_state == 'complete'):
          driver.refresh()
          retry_counter = retry_counter - 1
          if retry_counter< 0:
            raise Exception ("Page Loading Failed ,tried {} times to relaod page with wait in between of {} Seconds".format(retries, wait_time))


  def wait_for_element_not_visible(self,locator,time_out):
    """
    This method wait for the  element is not visible, or pass if the element dosen't exist
    locator (str): locator in Scriptless format that you need to be invisible
    time_out (str): time that the automation wait for the element
    """
    driver = self.get_webdriver()
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    try:
      loader = CommonUtils()._get_locator_strategy(locator) 
      WebDriverWait(driver, int(time_out)).until(EC.invisibility_of_element_located((loader['locator_type'],loader['element_locator'])))
    except:
      print(f"element isn't in the page")

  def click_with_javascript(self,locator,time_out):
    """
    locator (str): The input locator in scriptles format
    time_out (int): time in seconds that the automation wait for the element
    """
    driver = self.get_webdriver()
    element = CommonUtils()._get_web_element(driver,locator,time_out)
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    extendedSeleniumLibrary.wait_for_element_to_be_clickable(element)
    extendedSeleniumLibrary.javascript_click(element)

  def select_dropdown_option(self,dropdown_locator,list_locator,options_locators, option,time_out):
    """
    This method select an specif option from dropdown list
    dropdown_locator (str): The dropdown locator in scriptles format
    list_locator ( str): The list locator after click on dropdown in scriptles format
    option (str): String to be select into the dropdown element
    time_out (int): time in seconds that the automation wait for the element
    """
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    driver = self.get_webdriver()
    CommonUtils().click_element_and_wait(dropdown_locator, None, time_out)
    element_list = CommonUtils()._get_web_element(driver, list_locator,time_out)
    optionElements =  CommonUtils()._get_web_elements(driver,options_locators,time_out)
    for optionElement in optionElements:
      extendedSeleniumLibrary.wait_for_element_to_be_visible(optionElement)
      text = extendedSeleniumLibrary.get_element_text(optionElement)
      if text == option:
        optionElement.click()
        return

  def find_matching_element(self, list_locator: str, locator_to_find: str ,value_to_search: str, time_out: str) -> WebElement:
    """
    Finds and returns an element based on the specified criteria.

    Args:
        list_locator (str): Locator to find the list of elements (Multiple elements with the same locator)
        locator_to_find (str): Locator to find the desired element within the list
        value_to_search (str): Value to search within the elements' text
        time_out (str): Time limit for element search

    Returns:
        element (WebElement): Found element matching the criteria or None if not found
    """
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    driver = self.get_webdriver()
    element_list = CommonUtils()._get_web_elements(driver,list_locator,time_out)   
    sub_element_locator = CommonUtils()._get_locator_strategy(locator_to_find)
    
    if element_list is not  None:      
      for element in element_list:
        try:
          sub_element = element.find_element(sub_element_locator['locator_type'],f".{sub_element_locator['element_locator']}")
          text = extendedSeleniumLibrary.get_element_text(sub_element)
          self.log_message(f'webelement text: {text}')
          if value_to_search in text:
            return element
        except:
          pass
    return None

    
  def wait_matching_element(self,live_notifications_locator: str, label_locator_to_check: str, text_to_search, time_out: str) -> WebElement:
    """
    Waits for a specific live notification, and returns its text if found.

    Args:
        live_notifications_locator (str): Locator to find the list of live notifications.
        label_locator_to_check (str): Locator to find the desired label within each live notification.
        text_to_search (str): Text to search within the label of the live notifications.
        time_out (str): Time limit for waiting for the specific live notification.

    Returns:
        WebElement: 
    """
    live_notification = None
    start_time = time.time()
    while live_notification is None and (time.time() - start_time) < int(time_out):     
      live_notification = CommonUtils().find_matching_element(live_notifications_locator,label_locator_to_check,text_to_search,'20')
      print(f'live_notification: {live_notification}')
    return live_notification
  
  
  def get_text_from_webElement(self, webelement: WebElement, sub_element_locator: str) -> str:
    """
        Gets the text from a sub-element within the given web element based on the specified locator.

        Args:
            webelement (WebElement): Parent web element to find the sub-element within.
            sub_element_locator (str): Locator to find the desired sub-element.

        Returns:
            str: Text of the sub-element if found, None otherwise.
    """
    try:
      sub_element = self._get_sub_web_element(webelement, sub_element_locator)
    except:
      self.log_error_message(f'Subelement {sub_element_locator} is not in the web element {webelement}')
    return sub_element.text if sub_element is not None else None


  def is_webElement_displayed(self, webelement: WebElement, sub_element_locator: str) -> bool:
    """
    Checks if a sub-element within the given web element is displayed based on the specified locator.
    Args:
          webelement (WebElement): Parent web element to find the sub-element within.
          sub_element_locator (str): Locator to find the desired sub-element.
    Returns:
          bool: True if the sub-element is displayed, False otherwise.
    """
    try:
      sub_element = self._get_sub_web_element(webelement, sub_element_locator)
    except:
      self.log_error_message(f'Subelement {sub_element_locator} is not in the web element {webelement}')
    return sub_element.is_displayed() if sub_element is not None else False


  def _get_sub_web_element(self, webelement: WebElement, sub_element_locator : str) -> WebElement:
    """
    Finds and returns a sub-element within the given web element based on the specified locator.
    Args:
         webelement (WebElement): Parent web element to find the sub-element within.
         sub_element_locator (str): Locator to find the desired sub-element.

    Returns:
         WebElement: Found sub-element matching the criteria.
    """
    try:
      locator_startergy = CommonUtils()._get_locator_strategy(sub_element_locator)
      sub_element = webelement.find_element(locator_startergy['locator_type'],f".{locator_startergy['element_locator']}")
      return sub_element
    except:
      self.log_error_message(f'Subelement {sub_element_locator} is not in the web element {webelement}')
      return None
  
  def hidden_element(self,locator_to_hiden: str,time_out: str, disable: bool = True):
    """
    Finds Element and Hidden in the DOM.
    Args:
         locator_to_hiden (str): Locator of the element to be hidden.
         time_out (str): Time Out for seach the element.
         disable (bool): Set in True if you need to hidden the element 
    """
    driver = self.get_webdriver()
    locator_strategy = CommonUtils()._get_locator_strategy(locator_to_hiden)
    try:
      wait = WebDriverWait(driver, timeout=int(time_out), poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
      element_to_hiden =wait.until(EC.presence_of_element_located((locator_strategy['locator_type'], locator_strategy['element_locator'])))
      script = f"arguments[0].style.display = '{'none' if disable else 'initial'}';"
      driver.execute_script(script, element_to_hiden)
    except:
      self.log_message(f"The element: {locator_to_hiden} is not present in the Page")

  def count_web_elements(self,locator,time_out):
    extendedSeleniumLibrary = ExtendedSeleniumLibrary()
    driver = self.get_webdriver()
    element_list = CommonUtils()._get_web_elements(driver,locator,time_out)   
    return len(element_list)
  
  def wait_until_attribute_change(self,locator: str, attribute:str, expected_value:str, time_out:str=10):
    """
      Waits until a web element's attribute value changes to the expected value or until the time-out period expires.

      Parameters:
        locator (str): The locator to identify the web element (e.g., ID, Name, XPath, etc.)
        attribute (str): The attribute name to check (e.g., 'title', 'class', etc.)
        expected_value (str): The expected attribute value to wait for.
        time_out (int, optional): The maximum time (in seconds) to wait for the attribute to change to the expected value. Default is 10 seconds.

      Returns:
        None: This function logs the current attribute value once the wait is over or the condition is met.

      Example usage:
      wait_until_attribute_change('id=button', 'title', 'Mark complete', time_out=15)
    """
    current_value = None 
    start_time = time.time()
    while current_value != expected_value and (time.time() - start_time) < int(time_out):
      try:
        current_value = self.get_attribute(locator,attribute,30)
      except:
        self.log_message(f'The element "{locator}"  not found')
    self.log_message(f'The current value of the attribute "{attribute}" is: {current_value}')

  def scroll_element_into_view(self, locator: str, time_out: str = '30'):
    """
      Scrolls the web element identified by 'locator' into view.

      Args:
        locator (str): The locator to identify the web element on the page.
        time_out (tr): The maximum time (in seconds) to wait for the element to appear.

    """
    driver = self.get_webdriver()
    element = self._get_web_element(driver,locator,time_out)
    try:
      driver.execute_script("arguments[0].scrollIntoView();", element)
    except:
      acciones = ActionChains(driver)
      acciones.move_to_element(element).perform()

  def get_value_from_json_by_json_path(self, json_data: any, json_path: str) -> list:
    """
    Get the value from a JSON object using a JSON path.

    Args:
      json_data (dict): The JSON object to extract the value from.
      json_path (str): The JSON path to locate the value.

    Returns:
      list: A list of values found at the specified JSON path, or an empty list if none are found.
    """


    try:
      result = jsonpath.jsonpath(json_data, json_path)
      if not result:
        result = []
      return result
    except Exception as e:
      print(f"Error parsing JSONPath: {e}")
      return []  