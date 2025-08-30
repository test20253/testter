from scriptless.Core.framework.logger import LOGGER
from time import sleep
import autoit as ait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
from Tests.custom_methods.CommonMethods import CommonMethods as CM
import datetime
import urllib

class LogInMethods:

    @staticmethod
    def login_authPopup(username, password):
        if (LogInMethods.try_to_focus_on_window("Windows Security", 20) == False):
            raise Exception("Window with name \"Windows Security\" could not be found")
        try:
            sleep(1)
            ait.control_send("Windows Security", "", username, 1)
            sleep(1)
            ait.control_send("Windows Security", "", "{TAB}", 0)
            sleep(1)
            ait.control_send("Windows Security", "", password, 1)
            sleep(1)
            ait.control_send("Windows Security", "", "{ENTER}", 0)
            sleep(1)
        except Exception as error:
            logger = LOGGER.get_logger()
            logger.error(error)

    @staticmethod
    def login_authPopup_for_upload_document(username, password):
        if (LogInMethods.try_to_focus_on_window("Windows Security", 20) == False):
            raise Exception("Window with name \"Windows Security\" could not be found")
        try:
            ait.control_send("Windows Security", "", password, 1)
            sleep(1)
            ait.control_send("Windows Security", "", "{TAB}", 0)
            sleep(1)
            ait.control_send("Windows Security", "", "{TAB}", 0)
            sleep(1)
            ait.control_send("Windows Security", "", "{TAB}", 0)
            sleep(1)
            ait.control_send("Windows Security", "", "{ENTER}", 0)
            sleep(1)
        except Exception as error:
            logger = LOGGER.get_logger()
            logger.error(error)

    @staticmethod
    def SSO_login(driver, locator, timeout, username, password, retries):
        locator = locator.replace("xpath:", "").replace("\n", "")
        original_timeout_int = int(timeout)
        timeout_int = int(timeout)
        retries = int(retries)
        retry = False
        ait.auto_it_set_option("SendKeyDelay", 10)
        ait.auto_it_set_option("SendKeyDownDelay", 10)
        while (timeout_int >= 0 and retries >= 0):
            try:
                if (LogInMethods.try_to_focus_on_window("Windows Security", 1) == True):
                    LogInMethods.login_authPopup(username, password)
                    retries -= 1
                    if (retries > 0):
                        retry = True
                        break
                else:
                    WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.XPATH, locator))
                    )
                    timeout_int = -1000                    
            except Exception as error:
                logger = LOGGER.get_logger()
                logger.error(error)
                timeout_int -= 4            
        if (retry==True):
            return LogInMethods.SSO_login(driver, locator, timeout, username, password, retries)
        if retries < 0:
            raise Exception("The login window was tried to be used many times, but it keeps appearring (maybe the credentials are expired)")
        if timeout_int == -1000:
            return driver.find_element(By.XPATH, locator)
        raise Exception(f'Waited for {original_timeout_int} seconds, but neither the element with locator {locator} nor the windows security info were found.')


    @staticmethod
    def SSO_login_for_upload_document_without_selenium(username, password, retries):
        retries = int(retries)
        retry = False
        ait.auto_it_set_option("SendKeyDelay", 10)
        ait.auto_it_set_option("SendKeyDownDelay", 10)
        while (retries >= 0):
            try:
                if (LogInMethods.try_to_focus_on_window("Windows Security", 1) == True):
                    LogInMethods.login_authPopup_for_upload_document(username, password)
                    retries -= 1
                    sleep(5)
                    if (retries >= 0):
                        retry = True
                        break
                else:
                    return None                
            except Exception as error:
                logger = LOGGER.get_logger()
                logger.error(error)            
        if (retry==True):
            return LogInMethods.SSO_login_for_upload_document_without_selenium(username, password, retries)
        if retries < 0:
            raise Exception("The login window was tried to be used many times, but it keeps appearring (maybe the credentials are expired)")
        raise Exception(f'This error should not be possible, report it to the QA Canvas Automation Team')


    @staticmethod
    def SSO_login_for_upload_file(driver, locator, timeout, username, password, retries):
        locator = locator.replace("xpath:", "").replace("\n", "")
        original_timeout_int = int(timeout)
        timeout_int = int(timeout)
        retries = int(retries)
        retry = False
        ait.auto_it_set_option("SendKeyDelay", 10)
        ait.auto_it_set_option("SendKeyDownDelay", 10)
        while (timeout_int >= 0 and retries >= 0):
            try:
                if (LogInMethods.try_to_focus_on_window("Windows Security", 1) == True):
                    LogInMethods.login_authPopup(username, password)
                    retries -= 1
                    if (retries > 0):
                        retry = True
                        break
                else:
                    WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.XPATH, locator))
                    )
                    timeout_int = -1000                    
            except Exception as error:
                logger = LOGGER.get_logger()
                logger.error(error)
                timeout_int -= 4            
        if (retry==True):
            return LogInMethods.SSO_login(driver, locator, timeout, username, password, retries)
        if retries < 0:
            raise Exception("The login window was tried to be used many times, but it keeps appearring (maybe the credentials are expired)")
        if timeout_int == -1000:
            return driver.find_element(By.XPATH, locator)
        raise Exception(f'Waited for {original_timeout_int} seconds, but neither the element with locator {locator} nor the windows security info were found.')


    @staticmethod
    def complete_SSO_for_upload_document_if_needed(driver, locator, timeout, username, password, retries):
        result = -1
        ait.auto_it_set_option("SendKeyDelay", 10)
        ait.auto_it_set_option("SendKeyDownDelay", 10)
        timeout_int = int(timeout)
        while (timeout_int >= 0 and result == -1):
            try:
                if (LogInMethods.try_to_focus_on_window("Security Alert", 1) == True):
                    ait.control_send("Security Alert", "", "{ENTER}", 0)
                    sleep(5)
                    result = 1
                else:
                    WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.XPATH, locator))
                    )
                    result = 0                    
            except Exception as error:
                logger = LOGGER.get_logger()
                logger.error(error)
                timeout_int -= 4
        if result == 0:
            return driver.find_element(By.XPATH, locator)
        if result == 1:
            return LogInMethods.SSO_login(driver, locator, timeout, username, password, retries)        
        raise Exception(f'Something failed on the SSO Document Login Method, this should not have happened')

    @staticmethod
    def authenticate_incognito_user(driver, credential_user_name='CanvasAutomationUser1'):

        # Wait until url matches global access, where auth is required
        WebDriverWait(driver, 10).until(EC.url_contains('globalaccess.ey.com'))
        # Retrieve url access
        try:
            LogInMethods.modify_login_url_with_credentials(driver,credential_user_name)
        except:
            driver.refresh()
            WebDriverWait(driver, 10).until(EC.url_contains('globalaccess.ey.com'))
            LogInMethods.modify_login_url_with_credentials(driver,credential_user_name)


    @staticmethod
    def login_SSO_for_upload_document_if_needed(username, password, retries):
        result = -1
        ait.auto_it_set_option("SendKeyDelay", 10)
        ait.auto_it_set_option("SendKeyDownDelay", 10)
        try:
            if (LogInMethods.try_to_focus_on_window("Security Alert", 1) == True):
                ait.control_send("Security Alert", "", "{ENTER}", 0)
                sleep(5)
                result = 1
            else:
                result = 0                   
        except Exception as error:
            logger = LOGGER.get_logger()
            logger.error(error)
        if result == 0:
            return None
        if result == 1:
            return LogInMethods.SSO_login_for_upload_document_without_selenium(username, password, retries)        
        raise Exception(f'Something failed on the SSO Document Login Method, this should not have happened')

    
    @staticmethod
    def try_to_focus_on_window(window_title, timeout):
        while (timeout >= 0):
            try:
                ait.control_focus(window_title, "")
                return True
            except:
                sleep(1)
                timeout -= 1
        return False

    @staticmethod
    def get_agent_id():
        return os.getcwd()

    @staticmethod
    def send_queue_for_sync_windows_request(agent_id, window_name, timeout):
        time = datetime.datetime.now()
        time_formatted = time.strftime("%Y%m%d%H%M%S%f")
        request = {
            "agent_id": "",
            "timeout": "",
            "window_name": "",
            "status": "CREATED",
            "job_id": ""
        }
        request["agent_id"] = agent_id
        request["timeout"] = timeout
        request["window_name"] = window_name
        request["job_id"] = time_formatted
        CM.write_json_file(os.path.join("C:", os.sep , "agents_information", "lock_windows", f"{time_formatted}.json"), request)
        return request["job_id"]
    
    @staticmethod
    def send_queue_for_desync_windows_request(agent_id, window_name, job_id):
        time = datetime.datetime.now()
        time_formatted = time.strftime("%Y%m%d%H%M%S%f")
        request = {
            "agent_id": "",
            "window_name": "",
            "status": "CREATED",
            "job_id": ""
        }
        request["agent_id"] = agent_id
        request["window_name"] = window_name
        request["job_id"] = job_id
        CM.write_json_file(os.path.join("C:", os.sep, "agents_information", "unlock_windows", f"{time_formatted}.json"), request)
        return request["job_id"]

    @staticmethod
    def kill_window_by_name(window_name):
        ait.win_kill(window_name)

    @staticmethod
    def select_account_if_not_logged_or_continue_if_logged(driver, locator_expected_element_while_not_logged, locator_expected_element_while_logged, timeout):
        locator_expected_element_while_not_logged = locator_expected_element_while_not_logged.replace("xpath:", "").replace("\n", "")
        locator_expected_element_while_logged = locator_expected_element_while_logged.replace("xpath:", "").replace("\n", "")
        original_timeout_int = int(timeout)
        timeout_int = int(timeout)
        while timeout_int >= 0:
            try:
                WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, locator_expected_element_while_not_logged))
                )
                timeout_int = -1000
            except Exception:
                try:
                    WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.XPATH, locator_expected_element_while_logged))
                    )
                    timeout_int = -2000
                except Exception:
                    timeout_int = timeout_int - 4
        if timeout_int == -1000:
            WebDriverWait(driver, original_timeout_int).until(
                    EC.element_to_be_clickable((By.XPATH, locator_expected_element_while_not_logged))
            )
            webelement = driver.find_element(By.XPATH, locator_expected_element_while_not_logged)
            webelement.click()
            WebDriverWait(driver, original_timeout_int).until(
                        EC.visibility_of_element_located((By.XPATH, locator_expected_element_while_logged))
            )
            return driver.find_element(By.XPATH, locator_expected_element_while_logged)      
        if timeout_int == -2000:
            return driver.find_element(By.XPATH, locator_expected_element_while_logged)
        raise Exception(f'Waited for {original_timeout_int} seconds, but neither the element with locator {locator_expected_element_while_logged} not the element with locator {locator_expected_element_while_not_logged} were found.')

    @staticmethod
    def select_account_if_not_logged_or_continue_if_logged_with_posible_double_login(driver, locator_expected_element_while_not_logged, locator_expected_element_while_logged, timeout):
        locator_expected_element_while_not_logged = locator_expected_element_while_not_logged.replace("xpath:", "").replace("\n", "")
        locator_expected_element_while_logged = locator_expected_element_while_logged.replace("xpath:", "").replace("\n", "")
        original_timeout_int = int(timeout)
        timeout_int = int(timeout)
        while timeout_int >= 0:
            try:
                WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, locator_expected_element_while_not_logged))
                )
                timeout_int = -1000
            except Exception:
                try:
                    WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.XPATH, locator_expected_element_while_logged))
                    )
                    timeout_int = -2000
                except Exception:
                    timeout_int = timeout_int - 4
        if timeout_int == -1000:
            WebDriverWait(driver, original_timeout_int).until(
                    EC.element_to_be_clickable((By.XPATH, locator_expected_element_while_not_logged))
            )
            webelement = driver.find_element(By.XPATH, locator_expected_element_while_not_logged)
            webelement.click()
            return LogInMethods.select_account_if_not_logged_or_continue_if_logged(driver, locator_expected_element_while_not_logged, locator_expected_element_while_logged, timeout)     
        if timeout_int == -2000:
            return driver.find_element(By.XPATH, locator_expected_element_while_logged)
        raise Exception(f'Waited for {original_timeout_int} seconds, but neither the element with locator {locator_expected_element_while_logged} not the element with locator {locator_expected_element_while_not_logged} were found.')


    @staticmethod
    def try_to_update(driver, locator_of_update_button):
        locator_of_update_button = locator_of_update_button.replace("xpath:", "").replace("\n", "")
        try:
            webelement = driver.find_element(By.XPATH, locator_of_update_button)
            webelement.click()
        except Exception:
            pass
    
    @staticmethod
    def delete_cache(driver):
        driver.execute_script("window.open('');")
        sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        sleep(2)
        driver.get('chrome://settings/clearBrowserData') # for old chromedriver versions use cleardriverData
        sleep(2)
        actions = ActionChains(driver) 
        actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3) # send right combination
        actions.perform()
        sleep(2)
        actions = ActionChains(driver) 
        actions.send_keys(Keys.TAB * 4 + Keys.ENTER) # confirm
        actions.perform()
        sleep(5) # wait some time to finish
        driver.close() # close this tab
        driver.switch_to.window(driver.window_handles[0]) # switch back

    @staticmethod
    def modify_login_url_with_credentials(driver,credential_user_name ='CanvasAutomationUser1'):
        """
        This method perfomr the login after the firts click in a specific report
        """
        credential = CM.get_automation_user_info_from_credential_manager(credential_user_name)
        username = credential['userName']
        password = credential['password']
        encoded_username = urllib.parse.quote_plus(username)
        encoded_password = urllib.parse.quote_plus(password)
        url = driver.current_url
        domain_start = url.find("//") + 2
        new_url = url[:domain_start] + encoded_username + ":" + encoded_password + "@" + url[domain_start:]
        sleep(5)
        driver.get(new_url)
        return new_url
