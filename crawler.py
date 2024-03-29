from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import requests

SEND_EMAIL_URL = "http://localhost:8800/email/send"

UFRPE_PATH = "https://www.ufrpe.br/br/comunicados-home"
LAST_NEWS_FILE = "last_news.txt"

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(UFRPE_PATH)

def green_message(message):
    return f"\033[1;32m{message}\033[0m"

def red_message(message):
    return f"\033[1;31m{message}\033[0m"

def get_url():
    return driver.current_url


def get_last_news_title():
    last_news = driver.find_element(By.CLASS_NAME, "views-row-first")
    last_news_title = last_news.find_element(By.CLASS_NAME, "titulo_conteudo")
    return last_news_title

def read_news_file():
    with open(LAST_NEWS_FILE, "r") as file:
        return file.read()

def write_news_file(title):
    with open(LAST_NEWS_FILE, "w") as file:
        file.write(title)

def replace_breaklines(text):
    text_whithout_breaklines = text.replace("\n", " ")
    return text_whithout_breaklines

def replace_unwanted_tags(text):
    text_replaced = text.replace("\xa0", " ")
    return text_replaced


def get_links():
    try:
        files_section = driver.find_element(By.CLASS_NAME, "field-name-field-documento")
    except:
        return []
    news_files = files_section.find_elements(By.TAG_NAME, "a")
    pdfs_content = []

    for file in news_files:
        file_name = file.text
        file_url = file.get_attribute("href")
        pdfs_content.append({
            "name": file_name,
            "url": file_url
        })
    return pdfs_content

def get_images():
    try:
        content = driver.find_element(By.CLASS_NAME, "region-content")
    except:
        return []
    
    images = content.find_elements(By.TAG_NAME, "img")
    icons_path = "file/icons"
    images_src = []

    for image in images:
        image_src = image.get_attribute("src")
        
        if icons_path in image_src:
            continue

        images_src.append(image_src)

    return images_src

def get_body():

    news_body = driver.find_element(By.CSS_SELECTOR, "div[property='content:encoded']").get_attribute("innerHTML")
    soup = BeautifulSoup(news_body, 'html.parser')

    for img_tag in soup.find_all('img'):
        img_tag.decompose()

    news_body = replace_unwanted_tags(replace_breaklines(str(soup)))

    return news_body

def get_title():
    news_title= driver.find_element(By.CLASS_NAME, "page-header").text
    return news_title

def get_news_content():

    get_last_news_title().click()
    
    news = {
        "title": get_title(),
        "body": get_body(),
        "url": get_url(),
        "images": get_images(),
        "files": get_links()
    }

    return news

def send_email(content):
    try:
        response = requests.post(SEND_EMAIL_URL, json=content)
        if response.status_code == 200:
            print(green_message("\nNotícia enviada para a API com sucesso! "), "\n\n")
        else:
            print(red_message("\n\nErro na solicitação POST: ", response.status_code), "\n\n")
    except:
        print(red_message("\n\nFalha solicitação POST "), "\n\n")
        return


if __name__ == "__main__":
    last_news_title = get_last_news_title().text
    title_file = read_news_file()

    if last_news_title != title_file:
        content = get_news_content()
        write_news_file(last_news_title)
        print(green_message("\n\nNova notícia disponível: "), last_news_title,)
        # print(content)
        send_email(content)
    else:
        print(red_message("\n\nSem novas notícias"), "\n\n")

    driver.close()
