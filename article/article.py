import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www2.staffingindustry.com'


regions = ['site', 'eng', 'row']
mapping = {
    'site': 'Americas',
    'eng':  'EMEA',
    'row':  'APAC'
}

def focus_text(sentence, focus_words):
    """
    Returns a string with focus words capitalized

    :sentence(str): we will scan this and modify if words match
    :focus_words: an array of words to capitalize

    """
    sentence = sentence.lower()
    for w in focus_words:
        sentence = sentence.replace(w, w.upper())
    return sentence


focus_words = [
    'merger', 'merged',
     'acquisition', 'acquires', 'acquire', 'acquired', 'acquiring',
     'buys', 'purchase'
    ]

def scrape_daily_news():
    with open('articles.txt', 'wt+') as file:
        for region in regions:
            url = r'https://www2.staffingindustry.com/{}/Editorial/Daily-News/'.format(region)
            r = requests.get(url, allow_redirects=True)
            dom = BeautifulSoup(r.text, 'html.parser')
            articles = dom.find_all(class_='content-view-line class-news-item')
            file.write('{} section \n\n'.format(mapping[region]))
            for article in articles:
                link = article.a['href']
                article_r = requests.get(BASE_URL + link)
                article_dom = BeautifulSoup(article_r.text, 'html.parser')
                title = article_dom.find(id='site-main-content').header.h1.string
                print('Capturing: {}'.format(title))
                date = article_dom.find(id='site-main-content').find_all('div')[2].string
                text = article_dom.find(id='site-main-content').find_all('p')
                file.write(focus_text(title, focus_words) + '\n\n')
                file.write(date + '\n\n')
                file.write(article_r.url + '\n\n')
                for p in text:
                    s = focus_text(p.text, focus_words)
                    file.write(s + '\n\n')
                file.write('\n\n [END OF ARTICLE] \n\n')

if __name__ == '__main__':
    scrape_daily_news()
# article: <div class="content-view-line class-news-item">
# URL by regions
# {base}/{region}/Editorial/Daily-News/(offset)/{offset increments of 10}}
#   Americas: site
#   EMEA    : eng
#   APAC    : row

#
#https://www2.staffingindustry.com/Editorial/Daily-News/
