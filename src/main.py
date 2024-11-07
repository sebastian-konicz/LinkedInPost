import os
import sys

# Dodaje ścieżkę głównego katalogu repozytorium
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import LINKEDIN_ACCESS_TOKEN
from src.linkedin_client import LinkedInClient
from medium_scraper import medium_articles, freedium_article
from openai_api import article_summary
from openai_api_images import article_image

def main():
    access_token = LINKEDIN_ACCESS_TOKEN
    client = LinkedInClient(access_token)

    # medium scraping for articles
    top_url = medium_articles()
    # scraping top article
    freedium_article(top_url)
    # running ai summary script
    article_summary()
    # running ai image creating script
    article_image()

    with open('post_text.txt', 'r', encoding='utf-8') as file:
        post_text = file.read()

    # postin article with photo on LinkedIn
    client.create_post(post_text, "post_image.png")

if __name__ == "__main__":
    main()