import requests.exceptions
from pynytimes import NYTAPI
from bs4 import BeautifulSoup
import urllib
import datetime
import pandas as pd
import time

API_KEY = '1HXamLhbfLrsj4BUYmKZUGnZV2QLwAtR'

nyt = NYTAPI(API_KEY, https=False)  

def content(url):
    """
    Uses web crawling to acquire the content through the URLs obtained by the NYT API.
    """
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
    """
    Function that includes the query search. Includes 3 parameters: query, start date, and end date
    """
    a, b, c = begin.split(',')  
    x, y, z = end.split(',')  
    start_date = datetime.datetime(int(a), int(b), int(c))  
    end_date = datetime.datetime(int(x), int(y), int(z))
    dayrange = range((end_date - start_date).days + 1)
    all_data = []  
    for daycount in dayrange:
        dt = start_date + datetime.timedelta(days=daycount)
        #datestr = dt.strftime('%Y-%m-%d')
        print("Downloading", str(dt))
        try:  
            articles: list = nyt.article_search(  
                query=query,
                results=99,
                dates={
                    "begin": dt,
                    "end": dt
                },
                #options={'page': str(page)}
            )
            if articles:  
                print("content : ", len(articles))
                for art in articles:  
                    cont = content(art['web_url'])
                    art['content'] = cont  
                    print(art['web_url'])
                    time.sleep(1)
                all_data.extend(articles)  
                time.sleep(6)  
        except requests.exceptions.HTTPError:  
            pass
    print("Scraping...")
    
    return all_data


if __name__ == '__main__':
    # while True:
    word = input('\nPlease enter search term: ')
    begin = input('\nStart date(i.e:2019,3,15): ')
    end = input('\nEnd date(i.e:2019,3,15): ')
    articles = search(word, begin, end)
    if articles:
        df = pd.DataFrame(articles)  
        filename = word.split()[0] + ' ' + str(datetime.datetime.now().date()) + '..csv'
        df.to_excel(filename)  
        print(f'\nResults were saved under {filename}.')
    else:
        print('\nNo results were found...\n')
