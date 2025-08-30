from scriptless.Core.library.common.ExtendedSeleniumLibrary import ExtendedSeleniumLibrary
from scriptless.Core.library.common.CustomBase import CustomBase
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    ElementNotSelectableException, StaleElementReferenceException
from scriptless.Core.framework.page_object import PageObject
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
from scriptless.Core.framework.data_handler import Data_handler
from Tests.custom_methods.CommonMethods import CommonMethods as CM
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from robot.utils.asserts import assert_equal,fail
import re

class SeleniumMethods(CustomBase):

    @staticmethod
    def get_correct_webelement_from_webelement_list(driver, parent_list_locator, child_locator_to_filter, child_locator_to_return):
        #Trimming the locators to making them strings
        parent_list_locator = parent_list_locator.replace("xpath:", "").replace("\n", "")
        child_locator_to_filter = child_locator_to_filter.replace("xpath:", "").replace("\n", "")
        child_locator_to_return = child_locator_to_return.replace("xpath:", "").replace("\n", "")
        #Method logic
        webelements_parent_list = driver.find_elements(By.XPATH, parent_list_locator)
        for webelement in webelements_parent_list:
            amount_of_matches = webelement.find_elements(By.XPATH, f".{child_locator_to_filter}")
            if (len(amount_of_matches) == 1):
                return webelement
            if (len(amount_of_matches) == 0):
                continue
            raise Exception(f"There was more than one element found for the list {parent_list_locator} with the locator {child_locator_to_filter}")
        raise Exception(f"There were no elements found for the list {parent_list_locator} with the locator {child_locator_to_filter}")

    @staticmethod
    def click_webelement_if_property_not_met(webelement, property_to_validate, locator):
        #Trimming the locators to making them strings
        property_to_validate = property_to_validate.replace("xpath:", "").replace("\n", "")
        locator = locator.replace("xpath:", "").replace("\n", "")
        webelements_with_property = SeleniumMethods.get_sub_webelements_by_xpath(webelement, property_to_validate)
        if (len(webelements_with_property) != 1 and len(webelements_with_property) != 0):
            raise Exception(f"There was more than one element found for the property {property_to_validate}")
        else:
            SeleniumMethods.click_webelement(SeleniumMethods.get_sub_webelement_by_xpath(webelement, locator))


    @staticmethod
    def wait_for_a_certain_amount_of_elements(driver, locator, amount_expected, timeout):
        #Trimming the locators to making them strings
        locator = locator.replace("xpath:", "").replace("\n", "")
        timeout_to_use = int(timeout)
        while (timeout_to_use>=0):
            webelements = driver.find_elements(By.XPATH, locator)
            if (len(webelements) == int(amount_expected)):
                return True
            timeout_to_use = timeout_to_use - 1
            time.sleep(1)
        raise Exception(f"After {timeout_to_use} seconds, there were not {amount_expected} elements for the locator xpath:{locator}")

    @staticmethod
    def wait_for_more_than_certain_amount_of_elements(driver, locator, amount_of_expected_elements, timeout):
        #Trimming the locators to making them strings
        locator = locator.replace("xpath:", "").replace("\n", "")
        timeout_to_use = int(timeout)
        while (timeout_to_use>=0):
            webelements = driver.find_elements(By.XPATH, locator)
            if (len(webelements) > int(amount_of_expected_elements)):
                return True
            timeout_to_use = timeout_to_use - 1
            time.sleep(1)
        raise Exception(f"After {timeout_to_use} seconds, there were not more than {amount_of_expected_elements} elements for the locator xpath:{locator}")


    @staticmethod
    def get_sub_webelement_by_xpath(webelement, locator):
        #Trimming the locators to making them strings
        try:
            locator = locator.replace("xpath:", "").replace("\n", "")
            sub_webelement =  webelement.find_element(By.XPATH, f".{locator}")
            return sub_webelement
        except:
            return None

    @staticmethod
    def get_sub_webelements_by_xpath(webelement, locator):
        #Trimming the locators to making them strings
        locator = locator.replace("xpath:", "").replace("\n", "")
        return webelement.find_elements(By.XPATH, f".{locator}")
    

    @staticmethod
    def iterate_through_webelements_and_click_waitforvisibility_waitforinvisibility(driver, locator_to_click, locator_to_wait_visibility, locator_to_wait_invisibility):
        #Trimming the locators to making them strings
        locator_to_click = locator_to_click.replace("xpath:", "").replace("\n", "")
        locator_to_wait_visibility = locator_to_wait_visibility.replace("xpath:", "").replace("\n", "")
        locator_to_wait_invisibility = locator_to_wait_invisibility.replace("xpath:", "").replace("\n", "")
        webelements = driver.find_elements(By.XPATH, f".{locator_to_click}")
        count = 1
        for webelement in webelements:
            SeleniumMethods.click_webelement(webelement)
            SeleniumMethods.wait_for_a_certain_amount_of_elements(driver, locator_to_wait_visibility, count, 30)
            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, locator_to_wait_invisibility)))
            count += 1


    @staticmethod
    def click_element_if_other_element_not_visible(driver, locator_element_to_click, locator_element_to_check, waiting_time):
        locator_element_to_click = locator_element_to_click.replace("xpath:", "").replace("\n", "")
        locator_element_to_check = locator_element_to_check.replace("xpath:", "").replace("\n", "")
        waiting_time_int = int(waiting_time)
        try:
            WebDriverWait(driver, waiting_time_int).until(
                EC.presence_of_element_located((By.XPATH, locator_element_to_check))
            )
        except Exception:
            webelement = SeleniumMethods.get_webelement_by_xpath(driver, locator_element_to_click)
            SeleniumMethods.click_webelement(webelement)

    @staticmethod
    def count_amount_of_webelements(driver, locator):
        #Trimming the locators to making them strings
        locator = locator.replace("xpath:", "").replace("\n", "")
        #Method logic
        webelements_list = driver.find_elements(By.XPATH, locator)
        return len(webelements_list)

    @staticmethod
    def wait_for_visibility_of_one_of_two_elements(driver, locator_first_element, locator_second_item, timeout):
        locator_first_element = locator_first_element.replace("xpath:", "").replace("\n", "")
        locator_second_item = locator_second_item.replace("xpath:", "").replace("\n", "")
        timeout_int = int(timeout)
        while timeout_int >= 0:
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, locator_first_element))
                )
                timeout_int = -1000
            except Exception:
                try:
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, locator_second_item))
                    )
                    timeout_int = -2000
                except Exception:
                    timeout_int = timeout_int - 4
        if timeout_int == -1000:
            return driver.find_element(By.XPATH, locator_first_element)      
        if timeout_int == -2000:
            return driver.find_element(By.XPATH, locator_second_item)
        raise Exception(f'Waited for {timeout} seconds, but neither the element with locator {locator_first_element} not the element with locator {locator_second_item} were found.')


    @staticmethod
    def wait_for_visibility_of_multiple_elements(driver, locators, timeout):
        locators = locators.split("|")
        timeout_int = int(timeout)
        while timeout_int >= 0:
            for index, locator in enumerate(locators):
                locator = locator.replace("xpath:", "").replace("\n", "")
                try:
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, locator))
                    )
                    return (index+1)
                except:
                    timeout_int = timeout_int - 2
        raise Exception(f'Waited for {timeout} seconds, but no element in the locators {locators} were found.')

    @staticmethod
    def wait_for_visibility_of_multiple_elements_with_status(driver, locators, timeout):
        return_dict = {
            "status": "FAIL",
            "element_index": 0
        }
        locators = locators.split("|")
        timeout_int = int(timeout)
        while timeout_int >= 0:
            for index, locator in enumerate(locators):
                locator = locator.replace("xpath:", "").replace("\n", "")
                try:
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, locator))
                    )
                    return_dict["status"] = "PASS"
                    return_dict["element_index"] = index+1
                    return return_dict
                except:
                    timeout_int = timeout_int - 2
        return return_dict

    @staticmethod
    def click_element_until_condition_is_met(driver, locator_element_to_click, locator_element_to_complete, timeout, time_between_clicks):
        locator_element_to_click = locator_element_to_click.replace("xpath:", "").replace("\n", "")
        locator_element_to_complete = locator_element_to_complete.replace("xpath:", "").replace("\n", "")
        time_between_clicks_int = int(time_between_clicks)
        timeout_int = int(timeout)
        while timeout_int >= 0:
            driver.find_element(By.XPATH, locator_element_to_click).click()
            time.sleep(time_between_clicks_int)
            try:
                driver.find_element(By.XPATH, locator_element_to_complete)
                timeout_int = -1000
            except NoSuchElementException as e:
                timeout_int = timeout_int - time_between_clicks_int
        if timeout_int != -1000:
            raise Exception(f"The button {locator_element_to_click} was clicked multiple times but the element {locator_element_to_complete} was never found")
    
    @staticmethod
    def javascript_click_element_until_condition_is_met(driver, locator_element_to_click, locator_element_to_complete, timeout, time_between_clicks):
        locator_element_to_click = locator_element_to_click.replace("xpath:", "").replace("\n", "").replace("\"", "\'")
        locator_element_to_complete = locator_element_to_complete.replace("xpath:", "").replace("\n", "")
        time_between_clicks_int = int(time_between_clicks)
        timeout_int = int(timeout)
        while timeout_int >= 0:
            javaScript = f"document.evaluate(\"{locator_element_to_click}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();"           
            driver.execute_script(javaScript)
            time.sleep(time_between_clicks_int)
            try:
                driver.find_element(By.XPATH, locator_element_to_complete)
                timeout_int = -1000
            except NoSuchElementException as e:
                timeout_int = timeout_int - time_between_clicks_int
        if timeout_int != -1000:
            raise Exception(f"The button {locator_element_to_click} was clicked multiple times but the element {locator_element_to_complete} was never found")

    @staticmethod
    def click_element_until_invisibility_of_element(driver, locator_element_to_click, timeout, time_between_clicks):
        locator_element_to_click = locator_element_to_click.replace("xpath:", "").replace("\n", "")
        time_between_clicks_int = int(time_between_clicks)
        timeout_int = int(timeout)
        while timeout_int >= 0:
            try:
                driver.find_element(By.XPATH, locator_element_to_click).click()
            except:
                pass
            time.sleep(time_between_clicks_int)
            webelements_located = driver.find_elements(By.XPATH, locator_element_to_click)
            if (len(webelements_located) == 0):
                timeout_int = -1000
            else:
                timeout_int = timeout_int - time_between_clicks_int  
        if timeout_int != -1000:
            raise Exception(f"The button {locator_element_to_click} was clicked multiple times but the element {locator_element_to_complete} was never found")

    @staticmethod
    def refresh_until_function_is_met(driver, function_file, fuction_name, number_of_retries, *args):
        number_of_retries_int = int(number_of_retries)
        file_name = os.path.join(os.getcwd(), "Tests", "app_modules", f"{function_file}.xml")
        obj_common = PageObject(file_name=file_name, driver=driver)
        success_flag = False
        for x in range(0,number_of_retries_int):
            try:
                obj_common.execute_page_object_method(keyword=fuction_name, *args)
                success_flag = True
                break
            except Exception as e:
                driver.refresh()
        if success_flag == False:
            raise Exception(f"It was not posibile to execute the function {fuction_name}, it was tried {number_of_retries} times")

    @staticmethod
    def get_webelement_by_xpath(driver, locator):
        locator = locator.replace("xpath:", "").replace("\n", "")
        webelement = driver.find_element(By.XPATH, locator)
        return webelement
    
    @staticmethod
    def get_webelements_by_xpath(driver, locator):
        locator = locator.replace("xpath:", "").replace("\n", "")
        webelements = driver.find_elements(By.XPATH, locator)
        return webelements

    @staticmethod
    def click_webelement(webelement):
        webelement.click()
            
    @staticmethod
    def wait_click_webelement(driver,webelement):
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(webelement))
        webelement.click()

    @staticmethod
    def input_text_on_webelement(webelement, text):
        webelement.send_keys(text)

    @staticmethod
    def clear_webelement(webelement):
        webelement.clear()

    @staticmethod
    def get_current_url(driver):
        return driver.current_url
        
    @staticmethod
    def go_to_url(driver, url):
        driver.get(url)

    @staticmethod
    def get_attribute_of_webelement(webelement, attribute_name):
        return webelement.get_attribute(attribute_name)

    @staticmethod
    def switch_to_next_tab(driver, timeout):
        timeout_initial = timeout
        timeout = int(timeout)
        current_tab = driver.current_window_handle
        while timeout >= 0:
            tabs = driver.window_handles
            if len(tabs) > 1:
                timeout = -1000
            else:
                timeout -= 1
                time.sleep(1)
        if timeout != -1000:
            raise Exception(f"Waited for {timeout_initial} seconds, but there was no other tab opened")
        for tab in tabs:
            if(tab!=current_tab):
                driver.switch_to.window(tab)

    @staticmethod
    def close_all_other_tabs(driver):
        current_tab = driver.current_window_handle
        tabs = driver.window_handles
        if len(tabs) != 1:
            for tab in tabs:
                if(tab!=current_tab):
                    driver.switch_to.window(tab)
                    driver.close()
        driver.switch_to.window(current_tab)

    @staticmethod
    def wait_for_element_invisibility_by_xpath(driver, locator):
        locator = locator.replace("xpath:", "").replace("\n", "")
        wait_time = Data_handler().get_env_var_value("veryLongTimeOut")
        WebDriverWait(driver, wait_time).until(EC.invisibility_of_element_located((By.XPATH, locator)), message="The Element is visible {} after wait time {}".format(locator, wait_time))
        
    @staticmethod
    def wait_for_element_visibility_by_xpath(driver, locator):
        locator = locator.replace("xpath:", "").replace("\n", "")
        wait_time = Data_handler().get_env_var_value("veryLongTimeOut")
        webelement = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, locator)), message="The Element is not visible {} after wait time {}".format(locator, wait_time))
        return webelement

    @staticmethod
    def wait_for_configurable_element_visibility_by_xpath(driver, locator, timeout):
        locator = locator.replace("xpath:", "").replace("\n", "")
        wait_time = Data_handler().get_env_var_value("veryLongTimeOut")
        webelement = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, locator)), message="The Element is not visible {} after wait time {}".format(locator, wait_time))
        return webelement

    @staticmethod
    def wait_for_element_to_be_clickeable_by_xpath(driver, locator, timeout = 60):
        locator = locator.replace("xpath:", "").replace("\n", "")
        wait_time = Data_handler().get_env_var_value("veryLongTimeOut")
        webelement = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, locator)), message="The Element is not clickeable {} after wait time {}".format(locator, wait_time))
        return webelement
    
    @staticmethod
    def wait_for_element_to_be_clickeable_by_web_element(driver, web_element, timeout = 60):
        webelement =  WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(web_element))
        return webelement

    @staticmethod
    def get_text_of_webelement(webelement):
        return webelement.text
    
    @staticmethod
    def wait_and_refresh_for_page_to_load(driver, is_pageLoaded_locator, loader_content_locator, retries, wait_time=10):
        element = None
        retries = int(retries)
        if is_pageLoaded_locator.__contains__('|'):
            is_pageLoaded_locator = is_pageLoaded_locator.replace("xpath:", "").replace("\n", "")
            loader_content_locator = loader_content_locator.replace("xpath:", "").replace("\n", "")
            locator_startergy = "xpath"
            page_loaded_locator = is_pageLoaded_locator
        else:
            is_pageLoaded_locator = is_pageLoaded_locator.split(":")
            loader_content_locator = loader_content_locator.split(":")[1]
            locator_startergy = is_pageLoaded_locator[0]
            page_loaded_locator = is_pageLoaded_locator[1]
        while element is None:
            try:
                element =  WebDriverWait(driver, wait_time).until(
                   EC.visibility_of_element_located((locator_startergy, page_loaded_locator)))
            except:
                ele = SeleniumMethods.get_webelements_by_xpath(driver, loader_content_locator)
                page_state = driver.execute_script('return document.readyState;')
                if(page_state == 'complete' and len(ele)==0):
                    driver.refresh()
                retries = retries - 1
                if retries< 0:
                    raise Exception ("Page Loading Failed")
        return element
    
    @staticmethod
    def javascript_click_webelement(driver,locator):
            element_to_click = SeleniumMethods.get_webelement_by_xpath(driver, locator)
            driver.execute_script("arguments[0].click();", element_to_click)

    @staticmethod
    def skip_digital_gam_page(driver, timeout, sub_menu_locator="<%elm:scotsummary:Digital_Gam_SubMenu_ScotSummary%>"):
        CM.wait_page_to_load(driver)
        timeout = int(timeout) 
        tabs = driver.window_handles
        if len(tabs) > 1:
            SeleniumMethods.switch_to_next_tab(driver, timeout)
            
        wait_time = Data_handler().get_env_var_value("defaultTimeOut")
        is_pageLoaded_locator = Data_handler().parse_parameter("<%elm:scotsummary:Engagement Status Container%>| <%elm:scotsummary:Breadcrum Steps%>", "").replace('{{step}}', "1")
        loading_message = Data_handler().parse_parameter("<%elm:scotsummary:Loading Message%>","")
        retries = 5
        hamburger_webelement = SeleniumMethods.wait_and_refresh_for_page_to_load(driver, is_pageLoaded_locator, loading_message, retries, wait_time)
        breadcrumb_locator = Data_handler().parse_parameter("<%elm:scotsummary:Breadcrum Steps%>", "").replace('{{step}}', "1") 
        breadcrumb_webelement = SeleniumMethods.get_webelements_by_xpath(driver, breadcrumb_locator)
        if len(breadcrumb_webelement)==0:
            hamburger_locator = Data_handler().parse_parameter("<%elm:scotsummary:Hamburguer%>","").split(":")
            hamburger_webelement =  WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((hamburger_locator[0], hamburger_locator[1])))
            hamburger_webelement.click()
            sub_menu_locator = Data_handler().parse_parameter(sub_menu_locator,"").split(":") 
            sub_menu_webelement = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((sub_menu_locator[0], sub_menu_locator[1])))
            sub_menu_webelement.click()

    @staticmethod
    def get_network_log_by_name(driver, name):
        """
        This function return a request that be saved into the browser if it's name with some request
        driver (webdriver): current web driver
        name (str): complete name of the APPI (URL+ENDPONT) 
        """
        logs = driver.execute_script("return window.performance.getEntries();")
        print(f'[INFO] get_network_log_by_name')
        log = list(filter(lambda x: name in x["name"], logs))
        return log

    @staticmethod
    def wait_network_log_by_name(driver, name, timeout = 20):
        print(f'[INFO] Wait_network_log_by_name!')
        driver.set_script_timeout(60)
        log_entries = list()
        while len(log_entries) == 0 and timeout > 0:
            sleep(1)
            log_entries = SeleniumMethods.get_network_log_by_name(driver, name)
            timeout-=1
        return  bool(log_entries)


    @staticmethod
    def wait_network_log_by_status(driver, name, expected_status, timeout=20):
        log_entries = list()
        response_status = 0 
        
        while len(log_entries) == 0 and response_status != expected_status and timeout > 0:
            sleep(1)
            log_entries = SeleniumMethods.get_network_log_by_name(driver, name)
            if len(log_entries) != 0:
                response_status = int(log_entries[0]["responseStatus"])
            timeout -= 1
        return  bool(log_entries)

    def get_network_log_by_regex_name(driver, name_regex):
        """
        This function return a request that be saved into the browser if it's name match with a regular expresion or a complete name
        driver (webdriver): current web driver
        name_regex (str): complete name of the APPI (URL+ENDPONT) or regex to perform the search in the browsers's network log
        """
        logs = driver.execute_script("return window.performance.getEntries();")
        for log in logs:
            if re.search(name_regex, log["name"]) != None:
                return log

    @staticmethod
    def wait_network_log_by_name_regex(driver, name_regex, timeout = 20):
        """
        This function wait until a particular request be saved into de browser, this method acepts Regex to search the appi name 
        driver (webdriver): current web driver
        name_regex (str): complete name of the APPI (URL+ENDPONT) or regex to perform the search in the browsers's network log
        timeout (int): Time in seconds that the automation wait
        """
        response = None
        while(response == None and timeout > 0 ):
            sleep(1)
            response = SeleniumMethods.get_network_log_by_regex_name(driver, name_regex)
            timeout-=1
        if  (response == None):
            fail(f"The network log name: {name_regex} was not found")

    @staticmethod
    def perform_drag_and_drop(driver, source_locator, target_locator):
        source = SeleniumMethods.get_webelement_by_xpath(driver, source_locator)
        target = SeleniumMethods.get_webelement_by_xpath(driver, target_locator)
        driver.execute_script(
            "function createEvent(typeOfEvent) {\n" + "var event =document.createEvent(\"CustomEvent\");\n"
            + "event.initCustomEvent(typeOfEvent,true, true, null);\n" + "event.dataTransfer = {\n" + "data: {},\n"
            + "setData: function (key, value) {\n" + "this.data[key] = value;\n" + "},\n"
            + "getData: function (key) {\n" + "return this.data[key];\n" + "}\n" + "};\n" + "return event;\n"
            + "}\n" + "\n" + "function dispatchEvent(element, event,transferData) {\n"
            + "if (transferData !== undefined) {\n" + "event.dataTransfer = transferData;\n" + "}\n"
            + "if (element.dispatchEvent) {\n" + "element.dispatchEvent(event);\n"
            + "} else if (element.fireEvent) {\n" + "element.fireEvent(\"on\" + event.type, event);\n" + "}\n"
            + "}\n" + "\n" + "function simulateHTML5DragAndDrop(element, destination) {\n"
            + "var dragStartEvent =createEvent('dragstart');\n" + "dispatchEvent(element, dragStartEvent);\n"
            + "var dropEvent = createEvent('drop');\n"
            + "dispatchEvent(destination, dropEvent,dragStartEvent.dataTransfer);\n"
            + "var dragEndEvent = createEvent('dragend');\n"
            + "dispatchEvent(element, dragEndEvent,dropEvent.dataTransfer);\n" + "}\n" + "\n"
            + "var source = arguments[0];\n" + "var destination = arguments[1];\n"
            + "simulateHTML5DragAndDrop(source,destination);", source, target);
           
    @staticmethod
    def is_jquery_idle(driver):
        return driver.execute_script("return jQuery.active == 0")


    @staticmethod
    def wait_for_jquery_idle(driver, time_out='300'):
        start_time = time.time()
        loader_completed = False
        while not loader_completed and (time.time() - start_time) < int(time_out):
            try:
                loader_completed = SeleniumMethods.is_jquery_idle(driver)
            except:
                pass

    def get_text_from_list_of_elements(self, locator: str, time_out: str = '30') -> list:
        """
        Retrieves text from a list of web elements identified by the given locator.

        Args:
            locator (str): The locator to identify the list of web elements.
            time_out (str): The maximum time (in seconds) to wait for the elements to appear.

        Returns:
            list: A list containing the text from each web element.
        """
        self.get_selenium_instance().wait_until_page_contains_element(locator=locator, timeout=time_out)
        elements = self.get_selenium_instance().get_elements(locator)
        texts = []
        for element in elements:
            try:
                texts.append(element.text)
            except StaleElementReferenceException:
                continue
        return texts