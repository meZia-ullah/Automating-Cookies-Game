from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_driver_path = "D:/setups/chromedriver/chromedriver-win64/chromedriver.exe"
service = webdriver.chrome.service.Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

items = driver.find_elements(By.CSS_SELECTOR, "#store div")
items_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 10
five_min = time.time() + 60 * 5  # 5minutes

cookie = driver.find_element(By.ID, "cookie")

while True:
    cookie.click()
    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)
                print(item_prices)

        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = items_ids[n]

        my_money = driver.find_element(By.ID, "money").text
        if "," in my_money:
            my_money = my_money.replace(",", "")
        cookie_count = int(my_money)

        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID,to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 10

        # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID,"cps").text
        print(cookie_per_s)
        break
