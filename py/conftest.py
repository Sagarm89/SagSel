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
import platform
import socket
import subprocess
import time
from test.selenium.webdriver.common.network import get_lan_ip
from test.selenium.webdriver.common.webserver import SimpleWebServer
from urllib.request import urlopen

import pytest

from selenium import webdriver

drivers = (
    "chrome",
    "edge",
    "firefox",
    "ie",
    "remote",
    "safari",
    "webkitgtk",
    "wpewebkit",
)


def pytest_addoption(parser):
    parser.addoption(
        "--driver",
        action="append",
        choices=drivers,
        dest="drivers",
        metavar="DRIVER",
        help="driver to run tests against ({})".format(", ".join(drivers)),
    )
    parser.addoption(
        "--browser-binary",
        action="store",
        dest="binary",
        help="location of the browser binary",
    )
    parser.addoption(
        "--driver-binary",
        action="store",
        dest="executable",
        help="location of the service executable binary",
    )
    parser.addoption(
        "--browser-args",
        action="store",
        dest="args",
        help="arguments to start the browser with",
    )
    parser.addoption(
        "--headless",
        action="store",
        dest="headless",
        help="Allow tests to run in headless",
    )
    parser.addoption(
        "--use-lan-ip",
        action="store_true",
        dest="use_lan_ip",
        help="Whether to start test server with lan ip instead of localhost",
    )
    parser.addoption(
        "--bidi",
        action="store",
        dest="bidi",
        metavar="BIDI",
        help="Whether to enable BiDi support",
    )


def pytest_ignore_collect(path, config):
    drivers_opt = config.getoption("drivers")
    _drivers = set(drivers).difference(drivers_opt or drivers)
    if drivers_opt:
        _drivers.add("unit")
    parts = path.dirname.split(os.path.sep)
    return len([d for d in _drivers if d.lower() in parts]) > 0


driver_instance = None


class Driver:
    def __init__(self, driver_class, request):
        self._driver_class = driver_class
        self._request = request
        self._driver = None
        self._options = None
        self._platform = None
        self._service = None
        self.kwargs = {}

    @property
    def exe_platform(self):
        self._platform = platform
        return self._platform

    @property
    def browser_path(self):
        return self._request.config.option.binary

    @property
    def browser_args(self):
        return self._request.config.option.args

    @property
    def driver_path(self):
        return self._request.config.option.executable

    @property
    def headless(self):
        return bool(self._request.config.option.headless)

    @property
    def bidi(self):
        return bool(self._request.config.option.bidi)

    @property
    def options(self):
        if self.browser_path or self.browser_args:
            if not self._options:
                if self._driver_class == "Remote":
                    self._options = getattr(webdriver, "FirefoxOptions")() or webdriver.FirefoxOptions()
                    self._options.set_capability("moz:firefoxOptions", {})
                    self._options.enable_downloads = True
                elif self._driver_class.lower() == "webkitgtk":
                    self._driver_class = "WebKitGTK"
                    self._options = getattr(webdriver, f"{self._driver_class}Options")()
                    self._options.overlay_scrollbars_enabled = False
                elif self._driver_class.lower() == "wpewebkit":
                    self._driver_class = "WPEWebKit"
                    self._options = getattr(webdriver, f"{self._driver_class}Options")()
                else:
                    self._options = getattr(webdriver, f"{self._driver_class}Options")()

            if self.browser_path is not None:
                self._options.binary_location = self.browser_path.strip("'")
            if self.browser_args is not None:
                for arg in self.browser_args.split():
                    self._options.add_argument(arg)

        if self.headless:
            if self._driver_class == "Chrome" or self._driver_class == "Edge":
                self._options.add_argument("--headless=new")
            if self._driver_class == "Firefox":
                self._options.add_argument("-headless")

        if self.bidi:
            self._options.web_socket_url = True
            self._options.unhandled_prompt_behavior = "ignore"

        if self.driver_path:
            self.service = self.driver_path
        return self._options

    @property
    def service(self):
        executable = self.driver_path
        if executable:
            module = getattr(webdriver, self._driver_class.lower())
            self._service = module.service.Service(executable_path=executable)
            return self._service

    @property
    def driver(self):
        if not self._driver:
            return self._initialize_driver()

    def _initialize_driver(self):
        self.kwargs["options"] = self.options
        self.kwargs["service"] = self.service
        self._driver = getattr(webdriver, self._driver_class)(**self.kwargs)
        return self._driver

    @property
    def stop_driver(self):
        def fin():
            if self._driver is not None:
                self._driver.quit()

        return fin


@pytest.fixture(scope="function")
def driver(request):
    global driver_instance
    driver_class = getattr(request, "param", "Chrome").capitalize()
    selenium_driver = Driver(driver_class, request)
    driver_instance = selenium_driver.driver

    # skip tests if not available on the platform
    if driver_class == "Safari" and driver_instance.exe_platform != "Darwin":
        pytest.skip("Safari tests can only run on an Apple OS")
    if driver_class == "Ie" and driver_instance.exe_platform != "Windows":
        pytest.skip("IE and EdgeHTML Tests can only run on Windows")
    if "WebKit" in driver_class and driver_instance.exe_platform != "Linux":
        pytest.skip("Webkit tests can only run on Linux")
        # conditionally mark tests as expected to fail based on driver
    marker = request.node.get_closest_marker(f"xfail_{driver_class.lower()}")

    if marker is not None:
        if "run" in marker.kwargs:
            if marker.kwargs["run"] is False:
                pytest.skip()
                yield
                return
        if "raises" in marker.kwargs:
            marker.kwargs.pop("raises")
        pytest.xfail(**marker.kwargs)

    request.addfinalizer(selenium_driver.stop_driver)

    yield driver_instance


@pytest.fixture(scope="session", autouse=True)
def stop_driver(request):
    def fin():
        global driver_instance
        if driver_instance is not None:
            driver_instance.quit()
        driver_instance = None

    request.addfinalizer(fin)


def pytest_exception_interact(node, call, report):
    if report.failed:
        global driver_instance
        if driver_instance is not None:
            driver_instance.quit()
        driver_instance = None


@pytest.fixture
def pages(driver, webserver):
    class Pages:
        def url(self, name, localhost=False):
            return webserver.where_is(name, localhost)

        def load(self, name):
            driver.get(self.url(name))

    return Pages()


@pytest.fixture(autouse=True, scope="session")
def server(request):
    drivers = request.config.getoption("drivers")
    if drivers is None or "remote" not in drivers:
        yield None
        return

    _host = "localhost"
    _port = 4444
    _path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "java/src/org/openqa/selenium/grid/selenium_server_deploy.jar",
    )

    def wait_for_server(url, timeout):
        start = time.time()
        while time.time() - start < timeout:
            try:
                urlopen(url)
                return 1
            except OSError:
                time.sleep(0.2)
        return 0

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    url = f"http://{_host}:{_port}/status"
    try:
        _socket.connect((_host, _port))
        print(
            "The remote driver server is already running or something else"
            "is using port {}, continuing...".format(_port)
        )
    except Exception:
        print("Starting the Selenium server")
        process = subprocess.Popen(
            [
                "java",
                "-jar",
                _path,
                "standalone",
                "--port",
                "4444",
                "--selenium-manager",
                "true",
                "--enable-managed-downloads",
                "true",
            ]
        )
        print(f"Selenium server running as process: {process.pid}")
        assert wait_for_server(url, 10), f"Timed out waiting for Selenium server at {url}"
        print("Selenium server is ready")
        yield process
        process.terminate()
        process.wait()
        print("Selenium server has been terminated")


@pytest.fixture(autouse=True, scope="session")
def webserver(request):
    host = get_lan_ip() if request.config.getoption("use_lan_ip") else None

    webserver = SimpleWebServer(host=host)
    webserver.start()
    yield webserver
    webserver.stop()


@pytest.fixture
def edge_service():
    from selenium.webdriver.edge.service import Service as EdgeService

    return EdgeService


@pytest.fixture(scope="function")
def driver_executable(request):
    return request.config.option.executable


@pytest.fixture(scope="function")
def clean_service(request):
    try:
        driver_class = request.config.option.drivers[0].capitalize()
    except AttributeError:
        raise Exception("This test requires a --driver to be specified.")
    selenium_driver = Driver(driver_class, request)
    yield selenium_driver.service


@pytest.fixture(scope="function")
def clean_driver(request):
    try:
        driver_class = request.config.option.drivers[0].capitalize()
    except AttributeError:
        raise Exception("This test requires a --driver to be specified.")
    driver_reference = getattr(webdriver, driver_class)
    yield driver_reference

    if request.node.get_closest_marker("no_driver_after_test"):
        driver_reference = None
