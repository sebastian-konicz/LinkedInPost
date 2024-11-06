import requests
from bs4 import BeautifulSoup

# url data
freedium = 'https://freedium.cfd/'
url = 'https://generativeai.pub/the-first-fully-ai-generated-video-game-is-here-e52e4bf78d2d'
full_url = freedium + url

# scraping settings
response = requests.get(full_url)
page = response.content
soup = BeautifulSoup(page, 'html.parser')

# scraped elements
title = soup.find('h1').text

article_body = soup.find("div", class_="main-content").get_text(separator=" ")

# full text for prompt
full_text = f"TITLE: {title}\n" + f"ARTICLE BODY: {article_body}" + f"ARTICLE LINK: {url}"

# saving file
with open('article_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"{full_text}")