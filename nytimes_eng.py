from pynytimes import NYTAPI
from bs4 import BeautifulSoup
import urllib
import datetime
import pandas as pd
import time

API_KEY = '1HXamLhbfLrsj4BUYmKZUGnZV2QLwAtR'

nyt = NYTAPI(API_KEY, https=False)

# top_stories = nyt.top_stories()
#
# # Get all the top stories from a specific category
# top_science_stories = nyt.top_stories(section = "science")

# data = nyt.archive_metadata(
#     date = datetime.datetime(2019, 10, 1)
# )

def content(url):
    try:
        result = ''
        site = urllib.request.urlopen(url)
        content = site.read()
        soup = BeautifulSoup(content, 'lxml')
        table = soup.findAll('p')
        for line in table:
            result += line.text
            result += ' '
        return result
    except:
        return ''
    


def search(query, begin, end):
    a, b, c = begin.split(',')
    x, y, z = end.split(',')
    articles = nyt.article_search(
        query = query,
        results = 99,
        dates = {
            "begin": datetime.datetime(int(a), int(b), int(c)),
            "end": datetime.datetime(int(x), int(y), int(z))
        },
        # options = {
        #     "sort": "oldest",
        #     "sources": [
        #         "New York Times",
        #         "AP",
        #         "Reuters",
        #         "International Herald Tribune"
        #     ],
        #     "news_desk": [
        #         "Politics"
        #     ],
        #     "type_of_material": [
        #         "News Analysis"
        #     ]
        # }
    )
    for art in articles:
        cont = content(art['web_url'])
        art['content'] = cont
        print(art['web_url'])
        time.sleep(1)
    return articles


if __name__ == '__main__':
    while True:
        word = input('\nPlease enter search term: ')
        begin = input('\nStarting date(i.e:2019,3,15): ')
        end = input('\nEnd date(i.e:2019,3,15): ')
        articles = search(word, begin, end)
        if articles:
            df = pd.DataFrame(articles)
            filename = word.split()[0] + ' ' + str(datetime.datetime.now().date()) + '.xlsx'
            df.to_excel(filename)
            print(f'\nResults were saved under {filename}.')
        else:
            print('\nNo results were found...\n')
