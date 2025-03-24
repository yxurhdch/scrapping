from pprint import pprint
import json
import requests
import bs4
from fake_headers import Headers
from datetime import datetime

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            # Получаем текущую дату и время
            current_time = datetime.now()

            # Выполняем функцию и сохраняем результат
            result = old_function(*args, **kwargs)

            # Формируем строку для записи в лог
            log_entry = f"Функция: {old_function} была вызвана в {current_time}"
            log_entry += f" c аргументами {args=}, {kwargs=}"
            log_entry += f" c результатом {result}\n"

            with open(path, 'a', encoding='utf-8') as f:
                f.write(log_entry)

            return result
        return new_function
    return __logger


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
parsed_data = []

@logger('site_parser.log')
def find_keyword(text, keywords):
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True


@logger('site_parser.log')
def process_article(article):
    article_link = 'https://habr.com' + article.find('a', class_='tm-title__link')['href']

    article_response = requests.get(article_link)
    article_soup = bs4.BeautifulSoup(article_response.text, features='lxml')

    article_title = article_soup.find('h1').text
    div_time = article_soup.find('div', class_='tm-article-snippet__meta')
    article_time = div_time.find('time')['datetime']
    article_text = article_soup.find('div', class_='tm-article-body').text

    return {
        'time': article_time,
        'title': article_title,
        'link': article_link,
        'text': article_text
    }


response = requests.get('https://habr.com/ru/articles/',
                             headers=Headers(browser='chrome', os='win').generate())

soup = bs4.BeautifulSoup(response.text, features='lxml')
articles_list = soup.find_all('article', class_='tm-articles-list__item')

for article in articles_list:
    article_data = process_article(article)

    if find_keyword(article_data['title'], KEYWORDS) or find_keyword(article_data['text'], KEYWORDS):
        parsed_data.append({
            'time': article_data['time'],
            'title': article_data['title'],
            'link': article_data['link']
        })

if __name__ == '__main__':
    with open('article.json', 'w', encoding="utf-8") as file:
        json.dump(parsed_data, file, ensure_ascii=False, indent=4)
    print("Парсинг завершен. Результаты сохранены в article.json")
    print(f"Логи сохранены в site_parser.log")