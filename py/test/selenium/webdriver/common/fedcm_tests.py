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

import pytest

from selenium.common.exceptions import NoAlertPresentException


@pytest.mark.xfail_safari(reason="FedCM not supported")
@pytest.mark.xfail_firefox(reason="FedCM not supported")
@pytest.mark.xfail_ie(reason="FedCM not supported")
@pytest.mark.xfail_edge(reason="FedCM not supported")
class TestFedCM:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        html_file_path = os.path.abspath(
            "/Users/navinchandra/Documents/Projects/selenium/common/src/web/fedcm/fedcm.html"
        )
        print("File path is: ", html_file_path)

        driver.get(f"file://{html_file_path}")
        # driver.get('fedcm/fedcm.html')
        self.dialog = driver.fedcm_dialog

    def test_no_dialog_present(self, driver):
        with pytest.raises(NoAlertPresentException):
            self.dialog.title
        with pytest.raises(NoAlertPresentException):
            self.dialog.subtitle
        with pytest.raises(NoAlertPresentException):
            self.dialog.type
        with pytest.raises(NoAlertPresentException):
            self.dialog.get_accounts()
        with pytest.raises(NoAlertPresentException):
            self.dialog.select_account(1)
        with pytest.raises(NoAlertPresentException):
            self.dialog.cancel()

    def test_dialog_present(self, driver):
        driver.execute_script("triggerFedCm();")
        dialog = driver.wait_for_fedcm_dialog()

        assert dialog.title == "Sign in to localhost with localhost"
        assert dialog.subtitle is None
        assert dialog.type == "AccountChooser"

        accounts = dialog.get_accounts()
        assert accounts[0].name == "John Doe"

        dialog.select_account(1)
        dialog.cancel()

        with pytest.raises(NoAlertPresentException):
            dialog.title

    def test_fedcm_delay(self, driver):
        driver.set_fedcm_delay(True)

    def test_reset_cooldown(self, driver):
        driver.fedcm_cooldown()

    def test_fedcm_commands(self, driver):
        # Test get_fedcm_dialog_type
        with pytest.raises(NoAlertPresentException):
            driver.get_fedcm_dialog_type()

        # Test get_fedcm_title
        with pytest.raises(NoAlertPresentException):
            driver.get_fedcm_title()

        # Test get_fedcm_subtitle
        with pytest.raises(NoAlertPresentException):
            driver.get_fedcm_subtitle()

        # Test get_fedcm_account_list
        with pytest.raises(NoAlertPresentException):
            driver.get_fedcm_account_list()

        # Test select_fedcm_account
        with pytest.raises(NoAlertPresentException):
            driver.select_fedcm_account(1)

        # Test cancel_fedcm_dialog
        with pytest.raises(NoAlertPresentException):
            driver.cancel_fedcm_dialog()

        # Test click_fedcm_dialog_button
        with pytest.raises(NoAlertPresentException):
            driver.click_fedcm_dialog_button()

    def test_fedcm_dialog_flow(self, driver):
        driver.execute_script("triggerFedCm();")
        dialog = driver.wait_for_fedcm_dialog()

        # Test dialog properties
        assert dialog.type == "AccountChooser"
        assert dialog.title == "Sign in to localhost with localhost"
        assert dialog.subtitle is None

        # Test account list
        accounts = dialog.get_accounts()
        assert len(accounts) > 0
        assert accounts[0].name == "John Doe"

        # Test account selection
        dialog.select_account(1)

        # Test dialog button click
        dialog.click_continue()

        # Test dialog cancellation
        dialog.cancel()
        with pytest.raises(NoAlertPresentException):
            dialog.title

    def test_fedcm_delay_settings(self, driver):
        # Test enabling delay
        driver.set_fedcm_delay(True)

        # Test disabling delay
        driver.set_fedcm_delay(False)

    def test_fedcm_cooldown_management(self, driver):
        # Test cooldown reset
        driver.fedcm_cooldown()

        # Verify dialog can be triggered after reset
        driver.execute_script("triggerFedCm();")
        dialog = driver.wait_for_fedcm_dialog()
        assert dialog.type == "AccountChooser"
