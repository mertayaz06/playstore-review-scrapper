from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.get("https://play.google.com/store/apps/details?id=org.iggymedia.periodtracker&hl=en&gl=US&pli=1")

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz[2]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/c-wiz[6]/section/div/div[2]/div[5]/div/div/button')))

driver.execute_script("arguments[0].click();", element)
time.sleep(5)

comments = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]')
scrollable_div = comments.find_element(By.CLASS_NAME, "fysCi.Vk3ZVd")
reviews = []
stars_list = []
id_list = []
id = 1
last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

for i in range(10):
    comment = comments.find_elements(By.CLASS_NAME, "h3YV2d")
    stars = comments.find_elements(By.CLASS_NAME, "iXRFPc")

    for text in comment:
        if text.text != "":
            reviews.append(text.text)
            id_list.append(id)
            id += 1
        else:
            reviews.append("No comments, just rated")
            id_list.append(id)
            id += 1

    for star in stars:
        label = star.get_attribute("aria-label")
        label = label.split(" ")[1]
        stars_list.append(label)


    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    if new_height == last_height:
        print("Further comments could not be uploaded.")
        break
    last_height = new_height

df = pd.DataFrame({'ID': id_list, 'Star': stars_list, 'Review': reviews})
df.to_csv('./content/reviews.csv', index=False)
print("\n✔ The reviews.csv file was saved in the ./content folder.")

driver.quit()