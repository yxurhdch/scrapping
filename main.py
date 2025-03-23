from pprint import pprint
import json
import requests
import bs4
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
parsed_data = []

def find_keyword(text, keywords):
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True


response = requests.get('https://habr.com/ru/articles/',
                             headers=Headers(browser='chrome', os='win').generate())

soup = bs4.BeautifulSoup(response.text, features='lxml')
articles_list = soup.find_all('article', class_='tm-articles-list__item')

for article in articles_list:
    article_link = 'https://habr.com' + article.find('a', class_='tm-title__link')['href']

    article_response = requests.get(article_link)
    article_soup = bs4.BeautifulSoup(article_response.text, features='lxml')

    article_title = article_soup.find('h1').text
    div_time = article_soup.find('div', class_='tm-article-snippet__meta')
    article_time = div_time.find('time')['datetime']
    article_text = article_soup.find('div', class_='tm-article-body').text


    if find_keyword(article_title, KEYWORDS) or find_keyword(article_text, KEYWORDS):
        parsed_data.append({
            'time': article_time,
            'title': article_title,
            'link': article_link
        })


if __name__ == '__main__':
    with open('article.json', 'w', encoding="utf-8") as file:
        json.dump(parsed_data, file, ensure_ascii=False, indent=4)