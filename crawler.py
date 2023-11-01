from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


UFRPE_PATH = "https://www.ufrpe.br/br/lista-de-noticias"

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(UFRPE_PATH)

last_news = driver.find_element(By.CLASS_NAME, "views-row-1")
last_news_title = last_news.find_element(By.CLASS_NAME, "titulo_conteudo")
last_news_title.click()

news_title= driver.find_element(By.CLASS_NAME, "page-header")
news_body = driver.find_element(By.CLASS_NAME, "field-items")
print(news_body.text)


driver.close()
