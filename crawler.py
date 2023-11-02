from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

UFRPE_PATH = "https://www.ufrpe.br/br/lista-de-noticias"
LAST_NEWS_FILE = "last_news.txt"

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(UFRPE_PATH)

def green_message(message):
    return f"\033[1;32m{message}\033[0m"

def red_message(message):
    return f"\033[1;31m{message}\033[0m"

def get_last_news_title():
    last_news = driver.find_element(By.CLASS_NAME, "views-row-1")
    last_news_title = last_news.find_element(By.CLASS_NAME, "titulo_conteudo")
    return last_news_title

def read_news_file():
    with open(LAST_NEWS_FILE, "r") as file:
        return file.read()

def write_news_file(title):
    with open(LAST_NEWS_FILE, "w") as file:
        file.write(title)

def replace_break_lines(text):
    text_replaced = text.replace("\n", "<br>")
    return text_replaced

def get_news_content():
    get_last_news_title().click()
    news_title= driver.find_element(By.CLASS_NAME, "page-header")
    news_body = driver.find_element(By.CLASS_NAME, "field-items")
    news_url = driver.current_url
    return {
        "title": news_title.text,
        "body": replace_break_lines(news_body.text),
        "url": news_url
    }

last_news_title = get_last_news_title().text
title_file = read_news_file()

if last_news_title == title_file:
    content = get_news_content()
    write_news_file(last_news_title)
    print(content)
    print(green_message("\n\nNova notícia disponível: "), last_news_title, "\n\n")
else:
    print(red_message("\n\nSem novas notícias"), "\n\n")

driver.close()
