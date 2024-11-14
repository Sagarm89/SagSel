import pytest

from selenium import webdriver
from selenium.webdriver.common.bidi.network import Network
from selenium.webdriver.common.bidi.network import Response
from selenium.webdriver.common.bidi.network import Request


@pytest.fixture
def network(driver):
    yield Network(driver)

@pytest.fixture
def network_response(network):
    yield Response(network)

@pytest.fixture
def network_request(network):
    yield Request(network)

def test_add_response_handler(response):
    passed = [False]

    def callback(event):
        if event['response']['status'] == 200:
            passed[0] = True

    network_response.add_response_handler(callback)
    pages.load("basicAuth")
    assert passed[0] == True, "Callback was NOT successful"

def test_remove_response_handler(response):
    passed = [False]

    def callback(event):
        if event['response']['status'] == 200:
            passed[0] = True

    network_response.add_response_handler(callback)
    network_response.remove_response_handler(callback)
    pages.load("basicAuth")
    assert passed[0] == False, "Callback was successful"

def test_add_request_handler(request):
    passed = [False]

    def callback(event):
        if event['request']['method'] == 'GET':
            passed[0] = True

    network_request.add_request_handler(callback)
    pages.load("basicAuth")
    assert passed[0] == True, "Callback was NOT successful"

def test_remove_request_handler(request):
    passed = [False]

    def callback(event):
        if event['request']['method'] == 'GET':
            passed[0] = True

    network_request.add_request_handler(callback)
    network_request.remove_request_handler(callback)
    pages.load("basicAuth")
    assert passed[0] == False, "Callback was successful"

def test_add_authentication_handler(network):
    network.add_authentication_handler('test','test')
    pages.load("basicAuth")
    assert driver.find_element_by_tag_name('h1').text == 'authorized', "Authentication was NOT successful"

def test_remove_authentication_handler(network):
    network.add_authentication_handler('test', 'test')
    network.remove_authentication_handler()
    pages.load("basicAuth")
    assert driver.find_element_by_tag_name('h1').text != 'authorized', "Authentication was successful"