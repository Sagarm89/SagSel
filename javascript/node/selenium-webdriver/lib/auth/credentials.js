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
 * @fileoverview Defines credentials classes for authentication.
 */

/**
 * Base class for all types of credentials used for authentication.
 * @interface
 */
class Credentials {}

/**
 * Username and password credentials for basic authentication.
 * @implements {Credentials}
 */
class UsernameAndPassword extends Credentials {
  /**
   * @param {string} username The username to use for authentication.
   * @param {string} password The password to use for authentication.
   */
  constructor(username, password) {
    super()
    
    if (!username) {
      throw new Error('Username cannot be empty')
    }
    if (password === undefined || password === null) {
      throw new Error('Password cannot be null or undefined')
    }
    
    /** @private {string} */
    this.username_ = username
    
    /** @private {string} */
    this.password_ = password
  }

  /**
   * @return {string} The username.
   */
  getUsername() {
    return this.username_
  }

  /**
   * @return {string} The password.
   */
  getPassword() {
    return this.password_
  }
}

// PUBLIC API

module.exports = {
  Credentials,
  UsernameAndPassword
}