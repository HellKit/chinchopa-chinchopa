# TODO: Парсер
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WorkshopSteam:
    def __init__(self):
        work_dir = os.path.abspath(__file__)
        driver_dir = os.path.join(work_dir, '..', 'chromedriver')
        self.driver = webdriver.Chrome(driver_dir)
        self._set_settings()

    def _set_settings(self):
        """Настройки окна хрома"""
        self.driver.set_window_size(width=1920, height=1080)

    def put_game_id(self, id_=730, link=None):
        """Подключение к серверу стим"""
        if link is None:
            self.driver.get(f'https://steamcommunity.com/market/search?appid={id_}')
        else:
            self.driver.get(link)

    def get_weapon_price(self):
        return self.driver.find_element_by_class_name('market_listing_price').text

    def click_on_button(self, css_='', class_=True):
        if class_:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, css_))
            )
        else:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, css_))
            )
        button.click()

    def get_names_of_weapons(self):
        weapons = self.driver.find_element_by_name('category_730_Weapon[]')
        return weapons.text.split('\n')

    def input_to_search_panel(self, id_, text):
        self.driver.find_element_by_id(id_).send_keys(text)

    def get_links_for_weapons(self, class_):
        return [link.get_attribute('href') for link in self.driver.find_elements_by_class_name(class_)]

    @staticmethod
    def get_game_name_and_id():
        games = ['CS:GO']
        links = ['730']
        games_with_id = {game: link for game, link in zip(games, links)}
        return games_with_id

    def get_element_text(self, css_='', id_=False):
        if id_:
            elements = [el.text for el in self.driver.find_elements_by_id(css_)]
        else:
            elements = [el.text for el in self.driver.find_elements_by_class_name(css_)]
        return elements
