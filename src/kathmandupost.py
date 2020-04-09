from datetime import datetime
from bs4 import BeautifulSoup as BS
import requests
from common import get_soup

url = 'https://kathmandupost.ekantipur.com'
soup = get_soup(url)

def kathmandu_post_extractor():
    url = 'https://kathmandupost.ekantipur.com'
    soup = get_soup(url)
    more_news_section = soup.find('div', class_='block--morenews')
    news_list = more_news_section.find_all('article', class_="article-image")
    main_list = []

    for news in news_list:
        post_link = news.a['href']
        default_link = "https://kathmandupost.ekantipur.com"
        full_link = default_link + post_link
        title = news.contents[1].h3.text
        image_div = news.find('div', class_='image')
        try:
            image_link = image_div.figure.a.img['data-src']
        except:
            image_link = "img not available"
        date_url = news.a['href']
        date = get_date(date_url)

        summary = news.p.text
        news_dict = {
            "image_link": image_link,
            "title": title,
            "nep_date": date,
            "source": "ekantipur",
            "news_link": full_link,
            "summary": summary,
        }
        main_list.append(news_dict)
        last_list = featured_news(soup) + main_list

    return last_list


def featured_news(soup):
    featured_news = []
    featured_section = soup.find('div', class_='row order')
    sticky_news = featured_section.find_all('article', class_="article-image")

    for news in sticky_news:
        img_div = news.find('div', class_='image')
        try:
            img_link = img_div.figure.img['data-src']
        except:
            img_link = "img not available"
        default_link = "https://kathmandupost.ekantipur.com"
        post_link = news.h3.a['href']
        full_link = default_link + post_link
        title = news.h3.a.text
        date_url = news.h3.a['href']
        date = get_date(date_url)

        summary = news.p.text
        if len(summary) >= 1001:
            summary = summary[:1000]
        news_dict = {
            "title": title,
            "source": "ekantipur",
            "news_link": full_link,
            'nep_date': date,
            "summary": summary,
            "image_link": img_link,
        }
        featured_news.append(news_dict)
    return featured_news


def get_date(url_string):
    date = url_string.split('/')
    year_index = date.index(str(datetime.now().year))
    try:
        date_list = date[year_index: year_index + 3]
        full_date = "-".join(date_list)
    except IndexError:
        full_date = 'error'
    return full_date

if __name__ == "__main__":
    news = kathmandu_post_extractor()
    print(len(news))
