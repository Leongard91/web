from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException

driver = webdriver.Chrome(executable_path=r'C:\Users\Саша\Desktop\web\Testing\lecture7\selenium\chromedriver.exe')
print("Current session is {}".format(driver.session_id))

try:
    driver.get("https://www.google.com/")
except Exception as e:
    print(e.message)