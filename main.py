import bs4
import requests
from fake_useragent import UserAgent


def main():
    base_url = 'https://habr.com'
    url = base_url + '/ru/all/'

    all_articles = []

    keywords = ['дизайн', 'фото', 'web', 'python']

    ua = UserAgent()
    headers = {'UserAgent': ua.chrome}

    print_articles(all_articles)


def article_search(url, cls, headers, keywords):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    text = response.text

    soup = bs4.BeautifulSoup(text, features='html.parser')

    article = soup.find('article')
    try:
        preview = article.find(class_=cls).text
        if preview.lower().find(keywords) > -1:
            return True
    except AttributeError:
        pass


def preview_search(url, headers, keywords, all_articles):
    base_url = 'https://habr.com'
    url = base_url + '/ru/all/'
    response = requests.get(url, headers=headers)
    text = response.text

    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all("article")

    for article in articles:
        try:
            date = article.find(class_='tm-article-snippet__datetime-published').time.attrs['title'][:10]
            title = article.find(class_='tm-article-snippet__title-link').find('span').text
            link = base_url + article.find(class_='tm-article-snippet__title-link').artts['href']
            hubs = article.find_all(class_='tm-article-snippet__hubs-item')
            hubs = set(hub.text.strip('*').strip().lower() for hub in hubs)
            cls = 'article-formatted-body article-formatted-body article-formatted-body_version-1'
            preview = article.find(class_=cls).text
        except AttributeError:
            pass

        for keyword in keywords:
            if preview.lower().find(keyword) > -1 or title.lower().find(keyword) > -1 or keyword in hubs:
                news = [date, title, link]
                all_articles.append(news)
                break
            else:
                if article_search(url, cls, headers, keywords):
                    news = [date, title, link]
                    all_articles.append(news)
                    break
    return all_articles


def print_articles(all_articles):
    for article in all_articles:
        print(f'<{article[0]}> - <{article[1]}> - <{article[2]}>')
    return print(all_articles)


if __name__ == '__main__':
    main()
