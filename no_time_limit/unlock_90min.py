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

class Unlock90Min:

    @staticmethod
    def install_chromium():
        cache = apt.Cache()
        cache.update()
        cache.open(None)
        cache.commit()

        pkg = cache['chromium-chromedriver']
        pkg.mark_install()
        cache.commit()

    @staticmethod
    def create_notebook_page(notebook_url: str, user_data_dir: str) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=" + user_data_dir)
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome("chromedriver", options=options)
        driver.get(notebook_url)

        return driver

    def __init__(self, notebook_url: str, user_data_dir: str):
        print('start install chromium')
        Unlock90Min.install_chromium()
        print('end install chromium')

        self.driver = Unlock90Min.create_notebook_page(notebook_url, user_data_dir)
        self.__duration_hour = 11

    @property
    def duration_hour(self):
        return self.__duration_hour

    @duration_hour.setter
    def duration_hour(self, duration_hour):
        self.__duration_hour = duration_hour

    def save_screenshot(self, path: str = 'screenshot.png') -> None:
        original_size = self.driver.get_window_size()
        self.driver.set_window_size(1080, 4000)
        self.driver.find_element_by_tag_name('body').screenshot(path)
        self.driver.set_window_size(original_size['width'], original_size['height'])

    def periodic_process(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID,'comments'))).click()
        path = '/content/drive/My Drive/ETTTS/screenshot.png'
        self.save_screenshot(path)

    def end_process(self):
        pass

    def persistence_notebook(self):
        for i in range(self.__duration_hour * 6):
            time.sleep(10 * 60)
            self.periodic_process()
        self.end_process()
    
    def start(self):
        time.sleep(10)
        self.save_screenshot()

        print('start unlock 90 min')
        threading.Thread(target=self.persistence_notebook).start()

