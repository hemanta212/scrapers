from bs4 import BeautifulSoup as BS
import requests
from common import get_soup


def extractor(category=None, section='gen'):
    if not category:
        category = [27] if section == 'intl' else [21,22,24,25,26,31]
    elif category:
        _resolve_category(category)
    all_news = []
    for category_no in category:
        url = f'http://nagariknews.nagariknetwork.com/category/{category_no}'
        print("Resolved url", url)
        soup = get_soup(url)
        news_list = _soup_extractor(soup)
        all_news += news_list
    print(f"Length of all {len(all_news)}")
    return all_news


def _soup_extractor(soup):

    # with codecs.open("ujyaalo_international_cache.csv", "w",
    #  encoding='utf-8', errors='ignore') as w:
    # with open("ujyaalo_international_cache.csv", 'w') as w:
    def _cover_news(soup, nep_date):
        cover_news_list = []
        cover_div = soup.find_all("div", class_='col-sm-3 part-ent')
        for news in cover_div:
            img = news.div.img['src']
            image = img.replace("media/cache/nagarik_thumbnail_460_300/", "")
            image_url = image.replace("media/cache/resolve/nagarik_thumbnail_460_300/", "")
            title = news.h3.a.text
            summary = news.p.text
            primary_url = "https://nagariknews.nagariknetwork.com"
            news_link = primary_url + news.h3.a['href']
            cover_news_dict = {
                'title': title,
                'summary': summary,
                'source': 'Nagarik news',
                'summary': summary,
                'news_link': news_link,
                'image_link': img,
                'nep_date': nep_date,
            }
            cover_news_list.append(cover_news_dict)
        print(f"Length of cover {len(cover_news_list)}")
        return cover_news_list


    news_articles = soup.find_all('div', class_='detail-on')
    main_news_list = []

    for news in news_articles:
        title = news.h3.a.text
        date, summary = news.p.text, news.find_all('p')[1].text
        link = "http://nagariknews.nagariknetwork.com" + news.h3.a['href']
        news_dict = {
            'title': title,
            'nep_date': date,
            'source': 'Nagarik news',
            'summary': summary,
            'news_link': link,
            'image_link': None
        }
        main_news_list.append(news_dict)

    nep_date = main_news_list[0]['nep_date']
    cover_news_list = _cover_news(soup, nep_date)
    print(f"Length of main {len(main_news_list)}")
    final_list = cover_news_list + main_news_list
    return final_list

def _resolve_category(category):
    if type(category) is str:
        _category = category.replace(',', ' ').replace('  ',' ')
        category = [int(i) for i in _category.split(' ')]
    else:
        try:
            category = list(category)
        except TypeError:
            category = [category]


if __name__ == '__main__':
    news = extractor()
    print(len(news))
