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

from unittest.mock import Mock

import pytest

from selenium.webdriver.common.fedcm.dialog import Dialog


@pytest.fixture
def mock_driver():
    return Mock()


@pytest.fixture
def dialog(mock_driver):
    return Dialog(mock_driver)


def test_click_continue(dialog, mock_driver):
    dialog.click_continue()
    mock_driver.execute.assert_called_with("clickFedCmDialogButton", {"dialogButton": "ConfirmIdpLoginContinue"})


def test_cancel(dialog, mock_driver):
    dialog.cancel()
    mock_driver.execute.assert_called_with("cancelFedCmDialog")


def test_select_account(dialog, mock_driver):
    dialog.select_account(1)
    mock_driver.execute.assert_called_with("selectFedCmAccount", {"accountIndex": 1})


def test_type(dialog, mock_driver):
    mock_driver.execute.return_value = {"value": "AccountChooser"}
    assert dialog.type == "AccountChooser"


def test_title(dialog, mock_driver):
    mock_driver.execute.return_value = {"title": "Sign in"}
    assert dialog.title == "Sign in"


def test_subtitle(dialog, mock_driver):
    mock_driver.execute.return_value = {"subtitle": "Choose an account"}
    assert dialog.subtitle == "Choose an account"


def test_get_accounts(dialog, mock_driver):
    accounts_data = [
        {"name": "Account1", "email": "account1@example.com"},
        {"name": "Account2", "email": "account2@example.com"},
    ]
    mock_driver.execute.return_value = accounts_data
    accounts = dialog.get_accounts()
    assert len(accounts) == 2
    assert accounts[0].name == "Account1"
    assert accounts[0].email == "account1@example.com"
