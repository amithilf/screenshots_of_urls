from selenium import webdriver
import time
from selenium.common.exceptions import InvalidArgumentException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

def take_screenshots(file):
    images = [] #saving Images from file as base64 strings
    f = open(file, "r")
    urls_array = f.readlines()
    for i in urls_array:
        
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options) #driver_manager will not install new Chromedriver if it is already exists. 
        set_viewport_size(driver, 1920, 1080)
        try:
            driver.get(i) #accessing each URL from file
            time.sleep(3) #waiting for page to fully load
            x = driver.get_screenshot_as_base64()
            images.append(x)
            driver.close()
        except WebDriverException: #Selenium will check for common exceptions including ScreenshotException
            images.append("This page is no longer available")
            driver.close()
    return images, urls_array


if __name__ == '__main__':
    print('Enter your TXT file path:')
    txt_file = input()
    while True: #validating that a correct path was entered. 
        try:
            screenshots, urls = take_screenshots(txt_file)
        except FileNotFoundError:
            print('Please enter right path.')
            txt_file = input()
            continue
        break
    count = 0
    f = open('results.html','w')
    f.write("<html>\n")
    for i in screenshots:
        f.write('<h1>' + urls[count] + '</h1>')
        f.write("<h1>================</h1>")
        if i  == "This page is no longer available":
            f.write("<h1>" + i + "</h1>")
        else:
            f.write("<img src=data:image/png;base64," + i +">\n")
        count += 1
    f.write("</html>\n")
    f.close()


