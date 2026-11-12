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

import org.openqa.selenium.By;
import org.openqa.selenium.Credentials;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.UsernameAndPassword;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/**
 * Default implementation of the LoginHandler interface.
 * Provides standard methods for handling login and logout operations.
 */
public class DefaultLoginHandler implements LoginHandler {

  private final WebDriver driver;
  private final Duration timeout;
  
  // Default selectors
  private static final String DEFAULT_USERNAME_SELECTOR = "input[type='text'], input[type='email'], input[name='username'], input[id='username'], input[name='user'], input[id='user'], input[name='email'], input[id='email']";
  private static final String DEFAULT_PASSWORD_SELECTOR = "input[type='password'], input[name='password'], input[id='password'], input[name='pass'], input[id='pass']";
  private static final String DEFAULT_SUBMIT_SELECTOR = "button[type='submit'], input[type='submit'], button:contains('Login'), button:contains('Sign in'), button:contains('Log in'), input[value='Login'], input[value='Sign in'], input[value='Log in']";
  private static final String DEFAULT_LOGOUT_SELECTOR = "a:contains('Logout'), a:contains('Log out'), a:contains('Sign out'), button:contains('Logout'), button:contains('Log out'), button:contains('Sign out')";

  /**
   * Creates a new DefaultLoginHandler with the specified WebDriver.
   *
   * @param driver The WebDriver instance to use
   */
  public DefaultLoginHandler(WebDriver driver) {
    this(driver, Duration.ofSeconds(10));
  }

  /**
   * Creates a new DefaultLoginHandler with the specified WebDriver and timeout.
   *
   * @param driver The WebDriver instance to use
   * @param timeout The timeout duration for wait operations
   */
  public DefaultLoginHandler(WebDriver driver, Duration timeout) {
    this.driver = driver;
    this.timeout = timeout;
  }

  @Override
  public boolean login(Credentials credentials) {
    return login(credentials, DEFAULT_USERNAME_SELECTOR, DEFAULT_PASSWORD_SELECTOR, DEFAULT_SUBMIT_SELECTOR);
  }

  @Override
  public boolean login(Credentials credentials, String usernameSelector, String passwordSelector, String submitSelector) {
    if (!(credentials instanceof UsernameAndPassword)) {
      throw new IllegalArgumentException("Credentials must be an instance of UsernameAndPassword");
    }

    UsernameAndPassword userPass = (UsernameAndPassword) credentials;
    
    try {
      // Find username field and enter username
      WebElement usernameField = findElement(By.cssSelector(usernameSelector));
      usernameField.clear();
      usernameField.sendKeys(userPass.username());

      // Find password field and enter password
      WebElement passwordField = findElement(By.cssSelector(passwordSelector));
      passwordField.clear();
      passwordField.sendKeys(userPass.password());

      // Find and click submit button
      WebElement submitButton = findElement(By.cssSelector(submitSelector));
      submitButton.click();

      // Wait for page to load after login
      new WebDriverWait(driver, timeout).until(
          ExpectedConditions.or(
              ExpectedConditions.urlContains("dashboard"),
              ExpectedConditions.urlContains("account"),
              ExpectedConditions.urlContains("home"),
              ExpectedConditions.urlContains("profile")
          )
      );

      return true;
    } catch (NoSuchElementException | TimeoutException e) {
      return false;
    }
  }

  @Override
  public boolean logout() {
    return logout(DEFAULT_LOGOUT_SELECTOR);
  }

  @Override
  public boolean logout(String logoutSelector) {
    try {
      WebElement logoutElement = findElement(By.cssSelector(logoutSelector));
      logoutElement.click();

      // Wait for logout to complete
      new WebDriverWait(driver, timeout).until(
          ExpectedConditions.or(
              ExpectedConditions.urlContains("login"),
              ExpectedConditions.urlContains("signin"),
              ExpectedConditions.urlContains("logout"),
              ExpectedConditions.urlContains("signout")
          )
      );

      return true;
    } catch (NoSuchElementException | TimeoutException e) {
      return false;
    }
  }

  @Override
  public boolean isLoggedIn() {
    // Default implementation checks for common logout links/buttons
    // If a logout option is present, user is likely logged in
    try {
      return driver.findElements(By.cssSelector(DEFAULT_LOGOUT_SELECTOR)).size() > 0;
    } catch (Exception e) {
      return false;
    }
  }

  @Override
  public boolean isLoggedIn(String loggedInIndicatorSelector) {
    try {
      return driver.findElements(By.cssSelector(loggedInIndicatorSelector)).size() > 0;
    } catch (Exception e) {
      return false;
    }
  }

  /**
   * Helper method to find an element with wait.
   *
   * @param by The locator to find the element
   * @return The found WebElement
   * @throws NoSuchElementException if the element is not found
   */
  private WebElement findElement(By by) {
    return new WebDriverWait(driver, timeout)
        .until(ExpectedConditions.presenceOfElementLocated(by));
  }
}