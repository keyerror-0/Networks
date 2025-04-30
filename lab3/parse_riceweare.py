import time
import csv
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




parser = argparse.ArgumentParser(description= 'Choose category to parse')
parser.add_argument('-c', "--category", default= 'all', type= str)
category = parser.parse_args().category


def pagination_process(driver: webdriver.Chrome):
    try:
        driver.execute_script ("window.scrollTo(0,document.body.scrollHeight);")
        pagination_block = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                        (By.CLASS_NAME, "js-store-load-more-btn")))
        driver.execute_script("arguments[0].click()", pagination_block)
        return True
    except:
        return False

def init_driver():

    options = Options()
    options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    return webdriver.Chrome(options=options)

def move_to_categories(driver: webdriver.Chrome):

    WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.LINK_TEXT, "каталог"))
    )

    driver.find_element(By.LINK_TEXT, "каталог").click()

def show_available_categories(driver: webdriver.Chrome):
    WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "js-store-parts-switcher"))
    )

    categories = driver.find_elements(By.CLASS_NAME, "js-store-parts-switcher")
    
    # for category in categories:    
    #     print(category.text)
    
    return categories

def choose_category_to_parse(driver: webdriver.Chrome, categories, category = 'all'):

    # print("what category to parse?")
    user_category = category

    for category in categories:    
        if(category.text == user_category):
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(category)
                )
            category.click()

def process_popup(driver: webdriver, popup):
    close_buttons = popup.find_elements(By.CSS_SELECTOR, "button.t-popup__block-close-button")
    
    if close_buttons and close_buttons[0].is_displayed() and close_buttons[0].is_enabled():
        try:
            close_buttons[0].click()
        except:
            driver.execute_script("arguments[0].click();", close_buttons[0])

def parse_category(driver: webdriver):
    
    WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "t-item"))
    )

    while(pagination_process(driver) == True):
        time.sleep(0.2)

    with open('res.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'price', 'old_price', 'currency', 'href']
        writer = csv.DictWriter(csvfile, fieldnames= fieldnames)
        time.sleep(2)
        elems = driver.find_elements(By.CLASS_NAME, "t-item [href]")
        for elem in elems:
            try:
                popup_elements = driver.find_elements(By.CSS_SELECTOR, "div.t-popup.t-popup_show")

                if popup_elements and popup_elements[0].is_displayed():
                    process_popup(driver, popup_elements[0])

                WebDriverWait(driver, 20).until(
                EC.visibility_of(elem)
                )
                name = elem.find_element(By.CLASS_NAME, "t-name")
                price = elem.find_element(By.CLASS_NAME, "t-store__card__price-value")
                old_price = elem.find_element(By.CLASS_NAME, "js-store-prod-price-old-val")
                currency = elem.find_element(By.CLASS_NAME, "t-store__card__price-currency")
                href = elem.get_attribute("href")
            except:
                old_price = None
            writer.writerow({'name': name.text, 'price': price.text, 'old_price': old_price.text, 'currency': currency.text, 'href': href})

def main():
    driver = init_driver()
    driver.get("https://ricewear.com")
    move_to_categories(driver)
    categories = show_available_categories(driver)
    choose_category_to_parse(driver, categories, category=category)
    parse_category(driver)

main()