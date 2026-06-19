// Licensed to the Software Freedom Conservancy (SFC) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The SFC licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

package org.openqa.selenium.auth;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.UsernameAndPassword;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.testing.JupiterTestBase;
import org.openqa.selenium.testing.NotYetImplemented;
import org.openqa.selenium.testing.drivers.WebDriverBuilder;

/**
 * Tests for the LoginHandler functionality.
 */
public class LoginHandlerTest extends JupiterTestBase {

  private WebDriver driver;
  private LoginHandler loginHandler;

  @BeforeEach
  public void setUp() {
    driver = new WebDriverBuilder().get();
    loginHandler = driver.getLoginHandler();
  }

  @AfterEach
  public void tearDown() {
    if (driver != null) {
      driver.quit();
    }
  }

  @Test
  public void testGetLoginHandler() {
    assertNotNull(loginHandler, "LoginHandler should not be null");
  }

  @Test
  public void testSuccessfulLogin() {
    driver.get(pages.loginPage);
    
    UsernameAndPassword credentials = new UsernameAndPassword("test_user", "password");
    boolean result = loginHandler.login(credentials, "#username", "#password", "#login-button");
    
    assertTrue(result, "Login should be successful");
    assertTrue(loginHandler.isLoggedIn("#user-profile"), "User should be logged in");
  }

  @Test
  public void testFailedLogin() {
    driver.get(pages.loginPage);
    
    UsernameAndPassword credentials = new UsernameAndPassword("invalid_user", "wrong_password");
    boolean result = loginHandler.login(credentials, "#username", "#password", "#login-button");
    
    assertFalse(result, "Login should fail with invalid credentials");
    assertFalse(loginHandler.isLoggedIn("#user-profile"), "User should not be logged in");
  }

  @Test
  public void testLogout() {
    driver.get(pages.loginPage);
    
    // First login
    UsernameAndPassword credentials = new UsernameAndPassword("test_user", "password");
    loginHandler.login(credentials, "#username", "#password", "#login-button");
    
    // Then logout
    boolean result = loginHandler.logout("#logout-button");
    
    assertTrue(result, "Logout should be successful");
    assertFalse(loginHandler.isLoggedIn("#user-profile"), "User should be logged out");
  }
}