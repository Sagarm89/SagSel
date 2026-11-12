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

import pytest

from selenium.webdriver.common.auth import LoginHandler, UsernamePasswordCredentials
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class TestLoginHandler:
    
    def test_login_handler_property(self, driver):
        """Test that the login_handler property returns a LoginHandler instance."""
        assert isinstance(driver.login_handler, LoginHandler)
        
    def test_login_success(self, driver, pages):
        """Test successful login with valid credentials."""
        pages.load("login.html")
        
        credentials = UsernamePasswordCredentials("test_user", "password")
        result = driver.login_handler.login(
            credentials, 
            username_selector="#username", 
            password_selector="#password", 
            submit_selector="#login-button"
        )
        
        assert result is True
        assert driver.login_handler.is_logged_in("#user-profile") is True
        
    def test_login_failure(self, driver, pages):
        """Test failed login with invalid credentials."""
        pages.load("login.html")
        
        credentials = UsernamePasswordCredentials("invalid_user", "wrong_password")
        result = driver.login_handler.login(
            credentials, 
            username_selector="#username", 
            password_selector="#password", 
            submit_selector="#login-button"
        )
        
        assert result is False
        assert driver.login_handler.is_logged_in("#user-profile") is False
        
    def test_logout(self, driver, pages):
        """Test logout functionality."""
        pages.load("login.html")
        
        # First login
        credentials = UsernamePasswordCredentials("test_user", "password")
        driver.login_handler.login(
            credentials, 
            username_selector="#username", 
            password_selector="#password", 
            submit_selector="#login-button"
        )
        
        # Then logout
        result = driver.login_handler.logout("#logout-button")
        
        assert result is True
        assert driver.login_handler.is_logged_in("#user-profile") is False