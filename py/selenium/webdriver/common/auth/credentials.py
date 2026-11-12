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

from abc import ABC
from typing import Optional


class Credentials(ABC):
    """Base class for all types of credentials used for authentication."""
    pass


class UsernamePasswordCredentials(Credentials):
    """Username and password credentials for basic authentication."""

    def __init__(self, username: str, password: str):
        """
        Creates a new UsernamePasswordCredentials instance.

        Args:
            username: The username to use for authentication
            password: The password to use for authentication
        """
        if not username:
            raise ValueError("Username cannot be empty")
        if password is None:
            raise ValueError("Password cannot be None")

        self.username = username
        self.password = password