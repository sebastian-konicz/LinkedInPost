import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# scraping for articles in the given day
def medium_articles():
    # date values
    date = datetime.today()
    delta = 1
    search_date = date - timedelta(days=delta)
    search_date_value = datetime.strftime(search_date, "%Y-%m-%d")
    day_of_week = date.weekday()

    day = f"{search_date.day:02}"
    month = f"{search_date.month:02}"
    year = search_date.year

    print('system date:', date)
    # print('day_of_week:', day_of_week)
    # print('day:', day)
    # print('month:', month)
    # print('year:', year)

    urls = {
        # 'Towards Data Science': 'https://towardsdatascience.com/archive/{0}/{1:02d}/{2:02d}',
        'Generative AI': f'https://generativeai.pub/archive/{year}/{month}/{day}',
    }

    def get_claps(claps_str):
        if (claps_str is None) or (claps_str == '') or (claps_str.split is None):
            return 0
        split = claps_str.split('K')
        claps = float(split[0])
        claps = int(claps * 1000) if len(split) == 2 else int(claps)
        return claps

    data = []
    article_id = 0

    # articles for a given day:
    print(f'publication date: {search_date_value}')
    for publication, url in urls.items():
        print(publication)

        response = requests.get(url.format(year, month, day), allow_redirects=True)
        # if not response.url.startswith(url.format(year, month, day)):
        #     continue
        # print(response.content)
        page = response.content
        soup = BeautifulSoup(page, 'html.parser')

        articles = soup.find_all("div", class_="postArticle postArticle--short js-postArticle js-trackPostPresentation js-trackPostScrolls")

        for article in articles:
            title = article.find("h3", class_="graf--title")
            if title is None:
                continue
            title = title.contents[0]

            article_id += 1

            subtitle = article.find("h4", class_="graf--subtitle")
            subtitle = subtitle.contents[0] if subtitle is not None else ''

            article_url = article.find_all("a")[3]['href'].split('?')[0]

            claps = get_claps(article.find_all("button")[1].contents[0])

            responses = article.find_all("a")
            if len(responses) == 7:
                responses = responses[6].contents[0].split(' ')
                if len(responses) == 0:
                    responses = 0
                else:
                    responses = responses[0]
            else:
                responses = 0

            data.append([article_id, title, article_url, claps, responses])

    medium_df = pd.DataFrame(data, columns=['id', 'title', 'url',  'claps', 'responses'])

    # Sortowanie po kolumnie 'claps' w kolejności malejącej
    df_sorted = medium_df.sort_values(by='claps', ascending=False)

    # top 'url' and 'title' dla najwyższej wartości 'claps'
    top_title = df_sorted.iloc[1]['title']
    top_url = df_sorted.iloc[1]['url']

    print(top_title)
    print(top_url)

    # saving data
    file_name = f'medium_data'
    # file_name = f'medium_data_{year}_{month}_{day}'

    medium_df.to_csv(f'{file_name}.csv', index=False)
    # medium_df.to_parquet(f'{file_name}.csv', engine='pyarrow', compression='gzip')

    return top_url

def freedium_article(top_url):
    # url data
    freedium = 'https://freedium.cfd/'
    url = top_url
    full_url = freedium + url

    # scraping settings
    response = requests.get(full_url)
    page = response.content
    soup = BeautifulSoup(page, 'html.parser')

    # scraped elements
    title = soup.find('h1').text

    article_body = soup.find("div", class_="main-content").get_text(separator=" ")

    # full text for prompt
    full_text = f"ARTICLE TITLE: {title}\n" + f"ARTICLE BODY: {article_body}" + f"ARTICLE LINK: {url}"

    # saving file
    print('article text has been saved')
    with open('article_text.txt', 'w', encoding='utf-8') as f:
        f.write(f"{full_text}")

if __name__ == "__main__":
    top_url = medium_articles()
    freedium_article(top_url)