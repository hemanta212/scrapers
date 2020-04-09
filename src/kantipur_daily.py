from bs4 import BeautifulSoup as BS
import requests
from common import get_soup


def kantipur_daily_extractor():
    news_list = []
    url = 'https://www.kantipurdaily.com/news'
    soup = get_soup(url)

    for article in soup.find_all('article', class_='normal'):
        title = article.h2.a.text
        #author = article.find('div', class_='author').text
        summary = article.find('p').text
        image = article.find('div', class_="image").figure.a.img["data-src"]
        img = image.replace("-lowquality", "")
        small_img = img.replace("lowquality", "")
        big_img = small_img.replace("300x0", "1000x0")
        date_ore = article.h2.a['href']
        contaminated_list = date_ore.split('/')
        pure_date_list = [contaminated_list[2],
                          contaminated_list[3], contaminated_list[4]]
        date = "/".join(pure_date_list)
        link = "https://kantipurdaily.com" + date_ore
        news_dict = {
            'title': title,
            'nep_date': date,
            'source': 'ekantipur',
            'summary': summary,
            'news_link': link,
            'image_link': big_img,
        }
        news_list.append(news_dict)

    return news_list


if __name__ == "__main__":
    news = kantipur_daily_extractor()
    print(len(news))
