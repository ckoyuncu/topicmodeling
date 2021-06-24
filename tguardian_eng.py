import requests
from datetime import timedelta
import datetime
import pandas as pd

all_data = []

MY_API_KEY = 'c1ed206d-9ca3-4a87-ae13-0c1cf888b776'
API_ENDPOINT = 'http://content.guardianapis.com/search'

#dictionary which contains all parameters
my_params = {
    'from-date': "",
    'to-date': "",
    'order-by': "newest",
    'show-fields': 'all',
    'page-size': 200,
    'api-key': MY_API_KEY
}


def dataParse(data):
    for d in data:
        for key, value in d['fields'].items():
            d[key] = value
        d.pop('fields')
        all_data.append(d)


def search(query, start, end):
    """
    Function that includes the query search. Includes 3 parameters: query, start date, and end date
    """
    a, b, c = start.split('-')
    d, e, f = end.split('-')
    start_date = datetime.date(int(a), int(b), int(c))
    end_date = datetime.date(int(d), int(e), int(f))
    dayrange = range((end_date - start_date).days + 1)
    for daycount in dayrange:
        dt = start_date + timedelta(days=daycount)
        datestr = dt.strftime('%Y-%m-%d')
        print("Downloading", datestr)
        all_results = []
        my_params['q'] = query
        my_params['from-date'] = datestr
        my_params['to-date'] = datestr
        current_page = 1
        total_pages = 1
        while current_page <= total_pages:
            print("...page", current_page)
            my_params['page'] = current_page
            resp = requests.get(API_ENDPOINT, my_params)
            data = resp.json()
            all_results.extend(data['response']['results'])
            current_page += 1
            total_pages = data['response']['pages']
        dataParse(all_results)


if __name__ == '__main__':
    word = input('\nPlease enter search term: ')
    begin = input('\nStarting date(i.e:2019-3-15): ')
    end = input('\nEnd date(i.e:2019-3-15): ')
    search(word, begin, end)
    df = pd.DataFrame(all_data)
    df.to_excel(word.split()[0] + str(datetime.date.today()) + '.xlsx')
