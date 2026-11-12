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

import org.openqa.selenium.Credentials;

/**
 * Interface for handling login operations in WebDriver.
 * Provides methods to log in and log out of web applications.
 */
public interface LoginHandler {

  /**
   * Attempts to log in to a website using the provided credentials.
   * This method should handle the login form submission and verification.
   *
   * @param credentials The credentials to use for login
   * @return true if login was successful, false otherwise
   */
  boolean login(Credentials credentials);

  /**
   * Attempts to log in to a website using the provided credentials and custom selectors.
   * This method allows specifying custom selectors for username, password fields and submit button.
   *
   * @param credentials The credentials to use for login
   * @param usernameSelector The selector for the username field
   * @param passwordSelector The selector for the password field
   * @param submitSelector The selector for the submit button
   * @return true if login was successful, false otherwise
   */
  boolean login(Credentials credentials, String usernameSelector, String passwordSelector, String submitSelector);

  /**
   * Logs out from the current session.
   * This method should handle finding and clicking the logout button/link.
   *
   * @return true if logout was successful, false otherwise
   */
  boolean logout();

  /**
   * Logs out from the current session using a custom logout selector.
   *
   * @param logoutSelector The selector for the logout button/link
   * @return true if logout was successful, false otherwise
   */
  boolean logout(String logoutSelector);

  /**
   * Checks if the user is currently logged in.
   *
   * @return true if the user is logged in, false otherwise
   */
  boolean isLoggedIn();

  /**
   * Checks if the user is currently logged in by checking for the presence of an element.
   *
   * @param loggedInIndicatorSelector The selector for an element that indicates a logged-in state
   * @return true if the user is logged in, false otherwise
   */
  boolean isLoggedIn(String loggedInIndicatorSelector);
}