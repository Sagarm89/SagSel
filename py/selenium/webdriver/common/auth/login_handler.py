# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from typing import Optional, Union

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .credentials import Credentials, UsernamePasswordCredentials


class LoginHandler:
    """Handles login operations for web applications."""

    # Default selectors
    DEFAULT_USERNAME_SELECTOR = "input[type='text'], input[type='email'], input[name='username'], input[id='username'], input[name='user'], input[id='user'], input[name='email'], input[id='email']"
    DEFAULT_PASSWORD_SELECTOR = "input[type='password'], input[name='password'], input[id='password'], input[name='pass'], input[id='pass']"
    DEFAULT_SUBMIT_SELECTOR = "button[type='submit'], input[type='submit'], button:contains('Login'), button:contains('Sign in'), button:contains('Log in'), input[value='Login'], input[value='Sign in'], input[value='Log in']"
    DEFAULT_LOGOUT_SELECTOR = "a:contains('Logout'), a:contains('Log out'), a:contains('Sign out'), button:contains('Logout'), button:contains('Log out'), button:contains('Sign out')"

    def __init__(self, driver: WebDriver, timeout: float = 10):
        """
        Creates a new LoginHandler instance.

        Args:
            driver: The WebDriver instance to use
            timeout: The timeout in seconds for wait operations
        """
        self.driver = driver
        self.timeout = timeout

    def login(self, credentials: Credentials, username_selector: Optional[str] = None,
              password_selector: Optional[str] = None, submit_selector: Optional[str] = None) -> bool:
        """
        Attempts to log in to a website using the provided credentials.

        Args:
            credentials: The credentials to use for login
            username_selector: The selector for the username field (optional)
            password_selector: The selector for the password field (optional)
            submit_selector: The selector for the submit button (optional)

        Returns:
            True if login was successful, False otherwise
        """
        if not isinstance(credentials, UsernamePasswordCredentials):
            raise TypeError("Credentials must be an instance of UsernamePasswordCredentials")

        username_selector = username_selector or self.DEFAULT_USERNAME_SELECTOR
        password_selector = password_selector or self.DEFAULT_PASSWORD_SELECTOR
        submit_selector = submit_selector or self.DEFAULT_SUBMIT_SELECTOR

        try:
            # Find username field and enter username
            username_field = self._find_element(By.CSS_SELECTOR, username_selector)
            username_field.clear()
            username_field.send_keys(credentials.username)

            # Find password field and enter password
            password_field = self._find_element(By.CSS_SELECTOR, password_selector)
            password_field.clear()
            password_field.send_keys(credentials.password)

            # Find and click submit button
            submit_button = self._find_element(By.CSS_SELECTOR, submit_selector)
            submit_button.click()

            # Wait for page to load after login
            wait = WebDriverWait(self.driver, self.timeout)
            wait.until(
                EC.any_of(
                    EC.url_contains("dashboard"),
                    EC.url_contains("account"),
                    EC.url_contains("home"),
                    EC.url_contains("profile")
                )
            )

            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def logout(self, logout_selector: Optional[str] = None) -> bool:
        """
        Logs out from the current session.

        Args:
            logout_selector: The selector for the logout button/link (optional)

        Returns:
            True if logout was successful, False otherwise
        """
        logout_selector = logout_selector or self.DEFAULT_LOGOUT_SELECTOR

        try:
            logout_element = self._find_element(By.CSS_SELECTOR, logout_selector)
            logout_element.click()

            # Wait for logout to complete
            wait = WebDriverWait(self.driver, self.timeout)
            wait.until(
                EC.any_of(
                    EC.url_contains("login"),
                    EC.url_contains("signin"),
                    EC.url_contains("logout"),
                    EC.url_contains("signout")
                )
            )

            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def is_logged_in(self, logged_in_indicator_selector: Optional[str] = None) -> bool:
        """
        Checks if the user is currently logged in.

        Args:
            logged_in_indicator_selector: The selector for an element that indicates a logged-in state (optional)

        Returns:
            True if the user is logged in, False otherwise
        """
        if logged_in_indicator_selector:
            try:
                return len(self.driver.find_elements(By.CSS_SELECTOR, logged_in_indicator_selector)) > 0
            except Exception:
                return False
        else:
            # Default implementation checks for common logout links/buttons
            # If a logout option is present, user is likely logged in
            try:
                return len(self.driver.find_elements(By.CSS_SELECTOR, self.DEFAULT_LOGOUT_SELECTOR)) > 0
            except Exception:
                return False

    def _find_element(self, by: By, value: str):
        """
        Helper method to find an element with wait.

        Args:
            by: The locator strategy to use
            value: The locator value

        Returns:
            The found WebElement

        Raises:
            NoSuchElementException: If the element is not found
        """
        wait = WebDriverWait(self.driver, self.timeout)
        return wait.until(EC.presence_of_element_located((by, value)))