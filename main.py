from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://orteil.dashnet.org/cookieclicker/")
time.sleep(3)

lang = driver.find_element(By.ID, value="langSelect-PT-BR")
lang.click()

time.sleep(5)
timeout = time.time() + 60 * 5
timeout_start = time.time() + 5

big_cookie = driver.find_element(By.ID, value="bigCookie")
now = datetime.now()


def buy_most_expensive_one(upgrade, sec):
    global timeout_start
    cookies_count = driver.find_element(By.ID, value="cookies")
    cookies_str = cookies_count.text.split("\n")
    if cookies_str[0] == "1 cookie":
        cookies = cookies_str[0].replace("cookie", "").strip()
    else:
        cookies = cookies_str[0].replace("cookies", "").strip()

    cookies_count_float = float(cookies.replace(",", ""))
    timeout_end = time.time()
    if timeout_end >= timeout_start:
        timeout_start = timeout_end + sec
        if upgrade == "products":
            products = driver.find_elements(By.CSS_SELECTOR, value=f"#{upgrade} .product.unlocked.enabled")
        elif upgrade == "upgrades":
            products = driver.find_elements(By.CSS_SELECTOR, value=f"#{upgrade} .crate.upgrade.enabled")
        else:
            products = None
        if products is not None:
            for i in range(len(products)):
                if len(products) == 1:
                    products[0].click()
                    continue
                price = products[i].find_element(By.CLASS_NAME, value="price")
                last_product = products[i - 1] if i > 0 else None
                if last_product is not None:
                    last_price = last_product.find_element(By.CLASS_NAME, "price")
                    most_expansive = products[i] if float(price.text.replace(",", "")) > float(last_price.text.replace(",", "")) else last_product

                    if float(most_expansive.text.split("\n")[1].replace(",", "")) <= cookies_count_float:
                        most_expansive.click()


while True:
    buy_most_expensive_one("upgrades", 1)
    buy_most_expensive_one("products", 5)

    if time.time() >= timeout:
        break

    big_cookie.click()

