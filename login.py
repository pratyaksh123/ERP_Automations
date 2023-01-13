from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import time
import asyncio
from dotenv import load_dotenv
from scripts import check_course_grade
load_dotenv()

import os

username = os.environ.get("username")
password = os.environ.get("password")

import pytesseract

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--incognito")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280x1696")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-dev-tools")
options.add_argument("--no-zygote")
options.add_argument("--remote-debugging-port=9222")

async def main():
    path   = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(path, options=options)

    driver.get('http://220.158.144.41:8080/ERP_IITJ/')
    # login to form
    driver.find_element(By.NAME, 'userid').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)

    # find captcha
    captcha = driver.find_element(By.CLASS_NAME, 
        'captchaimage')
    captcha_image = captcha.screenshot_as_png
    with open('image.png', 'wb') as f:
        f.write(captcha_image)
    captcha_result = pytesseract.image_to_string(Image.open('image.png'))
    driver.find_element(By.NAME, "capResp").send_keys(captcha_result)

    results = await check_course_grade.check_grade(driver)
    print(results)
    driver.close()
    driver.quit()


if __name__ == '__main__':
    asyncio.run(main())
    # You can run this script using crontab as well.
    # run every 5 minutes
    # count = 0
    # while(True):
    #     print("Execution number", count)
    #     main()
    #     time.sleep(300)
    #     count += 1