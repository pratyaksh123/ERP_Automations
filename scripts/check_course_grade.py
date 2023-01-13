from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import asyncio

async def check_grade(driver):
    driver.get("http://220.158.144.41:8080/ERP_IITJ/studentPerformance.do")
    try:
        table = driver.find_elements(By.TAG_NAME, 'table')[9]
        row = table.find_elements(By.TAG_NAME, 'tr')[5]
        col = row.find_elements(By.TAG_NAME, 'td')[4]
        if col.text != "I":
            return "BTP grade updated to {col.text}"
            # send email if you want using ses
        else:
            return "BTP grade not updated yet"
    except NoSuchElementException as e:
        print("Course not found", e)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    check_grade()