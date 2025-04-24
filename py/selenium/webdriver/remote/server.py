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

import os
import re
import shutil
import socket
import subprocess
import time
import urllib

from selenium.webdriver.common.selenium_manager import SeleniumManager


class Server:
    """Manage the Selenium Remote (Grid) Server.

    Parameters:
    -----------
    host : str
        Hostname or IP address to bind to.
    port : str
        Port to listen on.
    path : str
        Path/filename of existing server .jar file (if not specified, server will be downloaded).
    version : str
        Version of server to download (if not specified, latest will be downloaded).
    env: dict
        Environment variables passed to server environment.
    """

    def __init__(self, host="localhost", port="4444", path=None, version=None, env=None):
        if path and version:
            raise TypeError("Not allowed to specify a version when using an existing server path")

        self.host = host
        self.port = port
        self.path = self._validate_path(path)
        self.version = self._validate_version(version)
        self.env = env

        self.process = None
        self.status_url = f"http://{self.host}:{self.port}/status"

    def _validate_path(self, path):
        if path and not os.path.exists(path):
            raise OSError(f"Can't find server .jar located at {path}")
        return path

    def _validate_version(self, version):
        if version:
            if not re.match(r"^\d+\.\d+\.\d+$", str(version)):
                raise TypeError(f"{__class__}.__init__() invalid version argument: '{version}'")
        return version

    def _wait_for_server(self, timeout=10):
        start = time.time()
        while time.time() - start < timeout:
            try:
                urllib.request.urlopen(self.status_url)
                return True
            except urllib.error.URLError:
                time.sleep(0.2)
        return False

    def start(self):
        """Start the server."""
        if not self.path:
            selenium_manager = SeleniumManager()
            args = ["--grid"]
            if self.version:
                args.append(self.version)
            self.path = selenium_manager.binary_paths(args)["driver_path"]
        java = shutil.which("java")
        if java is None:
            raise OSError("Can't find java on system PATH. JRE is required to run the Selenium server")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, int(self.port)))
            raise ConnectionError(
                f"The remote driver server is already running or something else is using port {self.port}"
            )
        except ConnectionRefusedError:
            print("Starting Selenium server")
            self.process = subprocess.Popen(
                [
                    "java",
                    "-jar",
                    self.path,
                    "standalone",
                    "--port",
                    self.port,
                    "--selenium-manager",
                    "true",
                    "--enable-managed-downloads",
                    "true",
                ],
                env=self.env,
            )
            print(f"Selenium server running as process: {self.process.pid}")
            if not self._wait_for_server():
                f"Timed out waiting for Selenium server at {self.status_url}"
            print("Selenium server is ready")
            return self.process

    def stop(self):
        """Stop the server."""
        if self.process is None:
            raise RuntimeError("Selenium server isn't running")
        else:
            self.process.terminate()
            self.process.wait()
            self.process = None
            print("Selenium server has been terminated")
