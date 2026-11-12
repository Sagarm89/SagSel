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

'use strict'

/**
 * @fileoverview Provides classes for handling login operations.
 */

const { By, until } = require('..')
const { UsernameAndPassword } = require('./credentials')

/**
 * Default selectors used for login operations.
 * @enum {string}
 */
const DEFAULT_SELECTORS = {
  USERNAME: "input[type='text'], input[type='email'], input[name='username'], input[id='username'], input[name='user'], input[id='user'], input[name='email'], input[id='email']",
  PASSWORD: "input[type='password'], input[name='password'], input[id='password'], input[name='pass'], input[id='pass']",
  SUBMIT: "button[type='submit'], input[type='submit'], button:contains('Login'), button:contains('Sign in'), button:contains('Log in'), input[value='Login'], input[value='Sign in'], input[value='Log in']",
  LOGOUT: "a:contains('Logout'), a:contains('Log out'), a:contains('Sign out'), button:contains('Logout'), button:contains('Log out'), button:contains('Sign out')"
}

/**
 * Class for handling login operations in WebDriver.
 */
class LoginHandler {
  /**
   * @param {!WebDriver} driver The WebDriver instance to use.
   * @param {number=} timeout The timeout in milliseconds for wait operations (default: 10000).
   */
  constructor(driver, timeout = 10000) {
    /** @private {!WebDriver} */
    this.driver_ = driver
    
    /** @private {number} */
    this.timeout_ = timeout
  }

  /**
   * Attempts to log in to a website using the provided credentials.
   * 
   * @param {!Credentials} credentials The credentials to use for login.
   * @param {string=} usernameSelector The selector for the username field (optional).
   * @param {string=} passwordSelector The selector for the password field (optional).
   * @param {string=} submitSelector The selector for the submit button (optional).
   * @return {!Promise<boolean>} A promise that resolves to true if login was successful, false otherwise.
   */
  async login(credentials, usernameSelector, passwordSelector, submitSelector) {
    if (!(credentials instanceof UsernameAndPassword)) {
      throw new TypeError('Credentials must be an instance of UsernameAndPassword')
    }

    usernameSelector = usernameSelector || DEFAULT_SELECTORS.USERNAME
    passwordSelector = passwordSelector || DEFAULT_SELECTORS.PASSWORD
    submitSelector = submitSelector || DEFAULT_SELECTORS.SUBMIT

    try {
      // Find username field and enter username
      const usernameField = await this.findElement_(By.css(usernameSelector))
      await usernameField.clear()
      await usernameField.sendKeys(credentials.getUsername())

      // Find password field and enter password
      const passwordField = await this.findElement_(By.css(passwordSelector))
      await passwordField.clear()
      await passwordField.sendKeys(credentials.getPassword())

      // Find and click submit button
      const submitButton = await this.findElement_(By.css(submitSelector))
      await submitButton.click()

      // Wait for page to load after login
      await this.driver_.wait(
        until.or(
          until.urlContains('dashboard'),
          until.urlContains('account'),
          until.urlContains('home'),
          until.urlContains('profile')
        ),
        this.timeout_
      )

      return true
    } catch (error) {
      return false
    }
  }

  /**
   * Logs out from the current session.
   * 
   * @param {string=} logoutSelector The selector for the logout button/link (optional).
   * @return {!Promise<boolean>} A promise that resolves to true if logout was successful, false otherwise.
   */
  async logout(logoutSelector) {
    logoutSelector = logoutSelector || DEFAULT_SELECTORS.LOGOUT

    try {
      const logoutElement = await this.findElement_(By.css(logoutSelector))
      await logoutElement.click()

      // Wait for logout to complete
      await this.driver_.wait(
        until.or(
          until.urlContains('login'),
          until.urlContains('signin'),
          until.urlContains('logout'),
          until.urlContains('signout')
        ),
        this.timeout_
      )

      return true
    } catch (error) {
      return false
    }
  }

  /**
   * Checks if the user is currently logged in.
   * 
   * @param {string=} loggedInIndicatorSelector The selector for an element that indicates a logged-in state (optional).
   * @return {!Promise<boolean>} A promise that resolves to true if the user is logged in, false otherwise.
   */
  async isLoggedIn(loggedInIndicatorSelector) {
    try {
      if (loggedInIndicatorSelector) {
        const elements = await this.driver_.findElements(By.css(loggedInIndicatorSelector))
        return elements.length > 0
      } else {
        // Default implementation checks for common logout links/buttons
        // If a logout option is present, user is likely logged in
        const elements = await this.driver_.findElements(By.css(DEFAULT_SELECTORS.LOGOUT))
        return elements.length > 0
      }
    } catch (error) {
      return false
    }
  }

  /**
   * Helper method to find an element with wait.
   * 
   * @private
   * @param {!By} locator The locator to find the element.
   * @return {!Promise<!WebElement>} A promise that resolves to the found WebElement.
   */
  async findElement_(locator) {
    return await this.driver_.wait(until.elementLocated(locator), this.timeout_)
  }
}

// PUBLIC API

module.exports = {
  LoginHandler,
  DEFAULT_SELECTORS
}