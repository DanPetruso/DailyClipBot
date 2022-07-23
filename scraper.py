from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import os
from os import listdir
import time

def download_clip():
    # opens top clips of the day
    url_main = 'https://www.twitch.tv/directory/game/Super%20Smash%20Bros.%20Melee/clips?range=24hr'

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) #just gets rid of annoying debug message

    twitch_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    twitch_driver.get(url_main)
    twitch_driver.implicitly_wait(30)

    # clicks on the first clip in the list of clips
    # using selenium to click coordinates rather than elements since finding elements on twitch page wasn't working out
    zero_elem = twitch_driver.find_element(By.ID, 'root')
    x_body_offset = zero_elem.location["x"]
    y_body_offset = zero_elem.location["y"]
    x = 250
    y = 310
    actions = ActionChains(twitch_driver)
    actions.move_to_element_with_offset(twitch_driver.find_element(By.ID, 'root'), -x_body_offset, -y_body_offset).click()
    actions.move_by_offset( x, y ).click().perform()

    clip_url = twitch_driver.current_url
    twitch_driver.quit()

    # delete old clips to keep things clean
    dir = os.getcwd()
    for file_name in listdir(dir):
        if file_name.endswith('.mp4'):
            os.remove(dir + "\\" + file_name)
    print("old clips deleted")

    # change download path
    prefs = {'download.default_directory' : dir}
    options.add_experimental_option('prefs', prefs)

    # now going to clipsey to download clip
    clip_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    clip_driver.get("https://clipsey.com/")
    clip_driver.implicitly_wait(30)

    textbox = clip_driver.find_element(By.CLASS_NAME, "clip-url-input")
    textbox.send_keys(clip_url)

    get_dl_button = clip_driver.find_element(By.CLASS_NAME, "get-download-link-button")
    get_dl_button.click()

    clip_driver.implicitly_wait(30)

    clip_title = clip_driver.find_element(By.TAG_NAME, "h3")
    clip_channel = clip_driver.find_element(By.CLASS_NAME, "clip-broadcaster")

    dl_button = clip_driver.find_element(By.CLASS_NAME, "download-clip-button")
    dl_button.click()

    time.sleep(3)

    print('Clip downloaded:', clip_title.text, "-", clip_channel.text)

    return (clip_title.text, clip_channel.text)

if __name__ == '__main__':
    download_clip()