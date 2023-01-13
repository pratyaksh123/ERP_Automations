from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

async def check_course(driver):
    driver.get("http://220.158.144.41:8080/ERP_IITJ/registration.do")
    try:
        course = driver.find_element(By.XPATH, '//select[@name="F"]//option[@value="MSL7140"]')
        print("Courses Available! \n", course.text)
        Select(driver.find_element(By.XPATH, '//select[@name="F"]')).select_by_value("MSL7140")
        Select(driver.find_element(By.XPATH, '//select[@name="F_type"]')).select_by_value("OE")
        add_course = driver.find_elements(By.XPATH, '//input[@type="submit"]')
        for i in add_course:
            if i.get_attribute('value') == 'Add Course(s)':
                add_course = i
                break
        print(add_course.tag_name, add_course.get_attribute('value'))
        print(driver.current_url)
        add_course.click()
        print(driver.current_url)
        WebDriverWait(driver, 100)
        return "Course Registered!"
    except NoSuchElementException as e:
        print("Courses are full")


    driver.close()
    driver.quit()


if __name__ == '__main__':
    check_course()