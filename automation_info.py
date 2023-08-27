import requests
import re

from bs4 import BeautifulSoup
from companies import companies, choose_companies, sold_positions
from profit_loss import profit_loss
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ports:
# 8000, 8080, 3000, 3001, ...
url = 'http://127.0.0.1:3000/'
response = requests.get(url)
# print(response.status_code)
# print(response.headers)

# print(response.json())
# print(response.text)

raw_html = response.content
parsed_html = BeautifulSoup(raw_html, 'html.parser', from_encoding='utf-8')
