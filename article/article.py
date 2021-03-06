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
    'merger', 'acquisition', 'acquires', 'buys', 'purchase'
    ]
with open('articles.txt', 'wt+') as file:
    for region in regions:
        r = requests.get('https://www2.staffingindustry.com/{}/Editorial/Daily-News'.format(region))
        dom = BeautifulSoup(r.text, 'html.parser')
        articles = dom.find_all(class_='content-view-line class-news-item')
        file.write('{} section \n\n'.format(mapping[region]))
        for article in articles:
            link = article.a['href']
            article_r = requests.get(BASE_URL + link)
            article_dom = BeautifulSoup(article_r.text, 'html.parser')
            article_title = article_dom.find(id='site-main-content').header.h1.string
            print('Capturing: {}'.format(article_title))
            article_date = article_dom.find(id='site-main-content').find_all('div')[2].string
            article_text = article_dom.find(id='site-main-content').find_all('p')
            file.write(article_title + '\n\n')
            file.write(article_date + '\n\n')
            for p in article_text:
                s = focus_text(p.text, focus_words)
                file.write(s + '\n\n')
            file.write('\n\n [END OF ARTICLE] \n\n')

# article: <div class="content-view-line class-news-item">
# URL by regions
# {base}/{region}/Editorial/Daily-News/
#   Americas: site
#   EMEA    : eng
#   APAC    : row

#
