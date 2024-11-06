import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import os

urls = {
    # 'Towards Data Science': 'https://towardsdatascience.com/archive/{0}/{1:02d}/{2:02d}',
    'Generative AI': 'https://generativeai.pub/archive/{0}/{1:02d}/{2:02d}',
}

def is_leap(year):
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True


def convert_day(day, year):
    month_days = [31, 29 if is_leap(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    m = 0
    d = 0
    while day > 0:
        d = day
        day -= month_days[m]
        m += 1
    return (m, d)


def get_claps(claps_str):
    if (claps_str is None) or (claps_str == '') or (claps_str.split is None):
        return 0
    split = claps_str.split('K')
    claps = float(split[0])
    claps = int(claps * 1000) if len(split) == 2 else int(claps)
    return claps


def get_img(img_url, dest_folder, dest_filename):
    ext = img_url.split('.')[-1]
    if len(ext) > 4:
        ext = 'jpg'
    dest_filename = f'{dest_filename}.{ext}'
    with open(f'{dest_folder}/{dest_filename}', 'wb') as f:
        f.write(requests.get(img_url, allow_redirects=False).content)
    return dest_filename

year = 2019
selected_days = random.sample([i for i in range(1, 367 if is_leap(year) else 366)], 50)
img_dir = 'images'
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

data = []
article_id = 0
i = 0
n = len(selected_days)

# for d in selected_days:
d = 311
year = 2024
month, day = convert_day(d, year)
date = '{0}-{1:02d}-{2:02d}'.format(year, month, day)
print(f'{i} / {n} ; {date}')
for publication, url in urls.items():
    response = requests.get(url.format(year, month, day), allow_redirects=True)
    # if not response.url.startswith(url.format(year, month, day)):
    #     continue
    # print(response.content)
    page = response.content
    soup = BeautifulSoup(page, 'html.parser')
    # print(soup)
    articles = soup.find_all("div",
                             class_="postArticle postArticle--short js-postArticle js-trackPostPresentation js-trackPostScrolls")
    # print(articles)
    for article in articles:
        title = article.find("h3", class_="graf--title")
        if title is None:
            continue
        title = title.contents[0]
        article_id += 1
        subtitle = article.find("h4", class_="graf--subtitle")
        subtitle = subtitle.contents[0] if subtitle is not None else ''
        image = article.find("img", class_="graf-image")
        image = '' if image is None else get_img(image['src'], 'images', f'{article_id}')
        article_url = article.find_all("a")[3]['href'].split('?')[0]
        claps = get_claps(article.find_all("button")[1].contents[0])
        reading_time = article.find("span", class_="readingTime")
        reading_time = 0 if reading_time is None else int(reading_time['title'].split(' ')[0])
        responses = article.find_all("a")
        if len(responses) == 7:
            responses = responses[6].contents[0].split(' ')
            if len(responses) == 0:
                responses = 0
            else:
                responses = responses[0]
        else:
            responses = 0

        story_page = requests.get(article_url)
        story_soup = BeautifulSoup(story_page.text, 'html.parser')

        sections = story_soup.find_all('section')

        story_paragraphs = []
        section_titles = []

        for section in sections:
            paragraphs = section.find_all('p')
            for paragraph in paragraphs:
                story_paragraphs.append(paragraph.text)

            subs = section.find_all('h1')
            for sub in subs:
                section_titles.append(sub.text)

        number_sections = len(section_titles)
        number_paragraphs = len(story_paragraphs)


        data.append(
            [article_id, article_url, title, subtitle, image, claps, responses, reading_time, publication, date, section_titles, story_paragraphs])



medium_df = pd.DataFrame(data, columns=['id', 'url', 'title', 'subtitle', 'image', 'claps', 'responses', 'reading_time',
                                        'publication', 'date', 'section_titles', 'story_paragraphs'])

medium_df.to_csv('medium_data.csv', index=False)