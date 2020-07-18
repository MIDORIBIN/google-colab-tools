from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import apt
import time
import datetime
import os
import glob
import sys
import threading


def install_chromium():
    cache = apt.Cache()
    cache.update()
    cache.open(None)
    cache.commit()

    pkg = cache['chromium-chromedriver']
    pkg.mark_install()
    cache.commit()

def create_notebook_page(notebook_url: str, user_data_dir: str) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=" + user_data_dir)
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("chromedriver", options=options)
    driver.get(notebook_url)

    return driver

def save_screenshot(driver: webdriver.Chrome, path: str = 'screenshot.png') -> None:
    original_size = driver.get_window_size()
    driver.set_window_size(1080, 4000)
    driver.find_element_by_tag_name('body').screenshot(path)
    driver.set_window_size(original_size['width'], original_size['height'])

def periodic_process(driver: webdriver.Chrome):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,'connect'))).click()
    path = '/content/drive/My Drive/ETTTS/screenshot.png'
    save_screenshot(driver, path)

def end_process():
    pass

def persistence_notebook(driver: webdriver.Chrome):
    hour = 9
    for i in range(hour * 6):
        time.sleep(10 * 60)
        periodic_process(driver)
    end_process()

def start(notebook_url: str, user_data_dir: str):
    print('start install chromium')
    install_chromium()
    print('end install chromium')

    driver = create_notebook_page(notebook_url, user_data_dir)

    save_screenshot(driver, 'drive/My Drive/ETTTS/screenshot.png')

    print('start unlock 90 min')
    threading.Thread(target=persistence_notebook, args=(driver, )).start()
