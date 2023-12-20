from selenium import webdriver
from selenium.webdriver.common.by import By
import json

def driversetup():
    options = webdriver.ChromeOptions()
    #run Selenium in headless mode
    options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    #overcome limited resource problems
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("lang=en")
    #open Browser in maximized mode
    options.add_argument("start-maximized")
    #disable infobars
    # options.add_argument("disable-infobars")
    #disable extension
    # options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    # options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options, )

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

    return driver

driver = driversetup()


def get_element_by_classname(url, driver, byClassName):
    driver.get(url)

    title_elements = driver.find_elements(By.CLASS_NAME, byClassName)
    p_elements = driver.find_elements(By.TAG_NAME, 'p')
    image_elements = driver.find_elements(By.CLASS_NAME, 'ratiobox_content')

    result = []
    
    for index, (title_element, p_element, image_element) in enumerate(zip(title_elements, p_elements, image_elements), start=1):
        title_text = title_element.text
        p_text = p_element.text
        
        style_attribute = image_element.get_attribute("style")
        if style_attribute:
            url_start = style_attribute.find("url(")
            url_end = style_attribute.find(")")
            if url_start != -1 and url_end != -1:
                image_url = style_attribute[url_start + 5: url_end - 1]
            else:
                image_url = None
        else:
            image_url = None

        element_info = {
            # "no": index,
            "title": title_text,
            "desc": p_text,
            "image_url": image_url
        }
        
        result.append(element_info)

    driver.quit()

    return json.dumps(result[:3], indent=4)


# driver = driversetup()
# # populor news
# # url = 'https://indeks.kompas.com/terpopuler'
# url = 'https://www.detik.com/tag/gen-z'
# # url = 'https://edukasi.kompas.com/'
# # byClassName = 'article__link'
# byClassName = "title"

# selected_element_text = get_element_by_classname(url, driver, byClassName)

# print(selected_element_text)