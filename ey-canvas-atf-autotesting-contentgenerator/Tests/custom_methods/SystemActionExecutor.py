from typing import List, Dict
import time

from scriptless.Core.library.common.CustomBase import CustomBase
from dotenv import load_dotenv
import pygetwindow as gw
import re
import os


class SystemActionExecutor(CustomBase):

    def _get_windows_names(self) -> List:
        """
        Extracts window names enclosed in single quotes from the currently active windows.

        Returns:
            list: A list of window names.
        """
        for window in gw.getAllWindows():
            if window.title and "'" in window.title:
                print(f"Original Title: {window.title}")
                window_names = window_names.extend(self.extract_quoted_text(window.title))
        return window_names

    def extract_quoted_text(title):

        return re.findall(r"'([^']*)'", title)

    def _get_window_by_name(self, window_name: str) -> str:
        """
        Get a reference to a window by its name.
        Args:
            window_name (str): The name of the window to search for.

        Returns:
            Window or None: The window object if found, None if not found.
        """
        window = gw.getWindowsWithTitle(window_name)
        return window

    def _is_window_opened(self, window_name: str) -> bool:
        """
        Search for a window by its name.
        Args:
            window_name (str): The name of the window to search for.

        Returns:
            bool: True if a window with the specified name is found, False otherwise.
        """
        return self._get_window_by_name(window_name) is not None

    def wait_until_the_desktop_window_is_visible(self, window_name: str, timeout: str = '30') -> bool:
        """
        Waits for a window by its name to become visible within a specified time limit.
        Args:
            window_name (str): The name of the window to search for.
            timeout (float): The maximum time (in seconds) to search for the window.

        Returns:
            bool: True if a window with the specified name is found within the specified time, False otherwise.
        """
        start_time = time.time()

        while time.time() - start_time < int(timeout):
            if self._is_window_opened(window_name):
                return True
            time.sleep(1)
        return False

    def get_edge_url(self, title_text: str) -> str:
        """
        Get the URL from a Microsoft Edge window based on its title text.
        Args:
            title_text (str): The text to search for in the window title.

        Returns:
            str or None: The URL if found, None if not found or the window is not open.
        """
        windows = self._get_windows_names()
        for window_name in windows:
            if title_text in window_name and "Edge" in window_name.replace("\u200b", ""):
                if self._is_window_opened(window_name):
                    window = self._get_window_by_name(title_text)
                    window.set_focus()
                    url_edit = window(title_re=window.window_text()).child_window(control_type="Edit",
                                                                                  found_index=0)
                    url = url_edit.get_value()
                    print(window.window_text())
                    return url
        return None

    def close_window_by_name(self, window_name: str):
        """
        Close a window by its name.
        Args:
            window_name (str): The name of the window to search for.
        """
        window = self._get_window_by_name(window_name)
        window.close()

    def _get_credentials_password(self, credential_user_name: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        Retrieves user credentials, including username and password, based on a provided credential user name.
        Args:
            credential_user_name (str): The credential user name for which the credentials are being retrieved.
                                        Defaults to 'CanvasAutomationUser1'. This name is used to form specific keys for
                                        fetching the email and password values.
        Returns:
            Dict[str, any]: A dictionary containing three key-value pairs:

        """
        try:
            load_dotenv()
            credential = os.getenv(f'{credential_user_name}')
            credential = eval(credential)
            return credential
        except (TypeError, SyntaxError, NameError) as e:
            self.log_error_message(f"Error retrieving credentials: {e}")
            return {}