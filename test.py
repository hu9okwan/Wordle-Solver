# function that checks which unpicked letter has most remaining and pick a word that matches such

# function that looks at each position with most common unpicked letter and suggests a word 


#importing webdriver from selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import collections
import random
import os
import string


options = webdriver.ChromeOptions()
username = os.environ['USERPROFILE']
USER_PROFILE_PATH = "--user-data-dir=" + username + "\\AppData\\Local\\Google\\Chrome\\User Data"
options.add_argument(USER_PROFILE_PATH)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options, executable_path = './selenium/chromedriver.exe')

url = "https://www.nytimes.com/games/wordle/index.html"
driver.get(url)







# def check_already_won():
#     # Checks if the game was already played/solved 
#     share_button_elem = driver.execute_script(" return document.querySelector('body > game-app').shadowRoot.querySelector('#game > game-modal > game-stats').shadowRoot.querySelector('#share-button') ")
#     if share_button_elem:
#         return True
#     return False

# print(check_already_won())

# element = driver.find_element_by_xpath("//*[@id='game']/game-modal/game-stats//div/div[3]/div[2]")

# if driver.find_elements(By.XPATH, "//*[@id='game']/game-modal/game-stats//div/div[3]/div[2]") == []:
#     print("yap")   # that element is not exist



#instructions 
# document.querySelector("body > game-app").shadowRoot.querySelector("#game > game-modal > game-help").shadowRoot.querySelector("section > div")
#xpath= //*[@id="game"]/game-modal/game-help//section/div
#fullx= /html/body/game-app//game-theme-manager/div/game-modal/game-help//section/div

#game stats
# document.querySelector("body > game-app").shadowRoot.querySelector("#game > game-modal > game-stats")
# //*[@id="game"]/game-modal/game-stats
# /html/body/game-app//game-theme-manager/div/game-modal/game-stats

def expand_shadow_element(element):
    shadow_root = driver.execute_script("return document.querySelector('body > game-app').shadowRoot", element)
    return shadow_root


try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body > game-app"))
    )
except TimeoutException:
    print("Timed out. Page took too long to load")
    exit

print("Document is ready")

# game_app_elem = driver.find_element_by_css_selector("body > game-app")
# shadow_root1 = expand_shadow_element(game_app_elem)

# game_stats_elem = driver.find_element_by_css_selector('#game > game-modal > game-help')

time.sleep(2)
shadow_root1 = driver.execute_script('return document.querySelector("body > game-app").shadowRoot.querySelector("#game > game-modal > game-stats")')



print(shadow_root1)
# print(game_stats_elem)
