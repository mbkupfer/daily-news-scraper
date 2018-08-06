import requests
from bs4 import BeautifulSoup

base = 'https://www2.staffingindustry.com'


regions = ['site', 'eng', 'row']
for region in regions:
    r = requests.get('https://www2.staffingindustry.com/{}/Editorial/Daily-News'.format(region))
    dom = BeautifulSoup(r.text, 'html.parser')
    articles = dom.find_all(class_='content-view-line class-news-item')
    for article in articles:
        link = article.a['href']
        r = requests.get(base + link)
        print
        print(r.request.url, r.status_code)

# article: <div class="content-view-line class-news-item">
# URL by regions
# {base}/{region}/Editorial/Daily-News/
#   Americas: site
#   EMEA    : eng
#   APAC    : row

#
