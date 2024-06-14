from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def open_page(driver_exe: str, url: str, detach: bool = True) -> webdriver.Chrome:
    s = Service(driver_exe)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', detach)
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(url)

    return driver
