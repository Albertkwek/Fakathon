#!/usr/bin/python3

import sys
    
if len(sys.argv) != 4:  # the program name and the datafile
# stop the program and print an error message
    sys.exit("usage: get_nyt_data.py month year N")

month = int(sys.argv[1])
year = int(sys.argv[2])
N = int(sys.argv[3])

from nytimesarchive import ArchiveAPI
import requests
from bs4 import BeautifulSoup

def get_nyt_urls(month,year,sections=['Sports','Technology','Health','U.S.','World','Science','Business Day','Job Market']):
    api = ArchiveAPI('1c69c544ee10436f89f54e8041ddcbed')
    print("Querying data...")
    r = api.query(year,month)
    
    N = len(r['response']['docs'])

    urls = [r['response']['docs'][x]['web_url'] for x in range(0,N) if r['response']['docs'][x]['section_name'] in sections]
    #section = [r['response']['docs'][x]['section_name'] for x in range(0,N) if r['response']['docs'][x]['section_name'] in sections]
    
    print(len(urls),"documents queried.")
    
    return urls

def html_to_factors_nytimes(url):
    """
    Given a url from nytimes, this function returns a dictionary which contains the name of the author, 
    number of links on the website, the headline and the body.
    """
    #print("Fetching data from", url)
    response = requests.get(url)
    if response.status_code == 200:
        try:
            page_data_soup = BeautifulSoup(response.content,'lxml')
            author_name = page_data_soup.find('span', class_='byline-author').text
            links = [link.get('href') for link in page_data_soup.find_all('a', href=True)]
            headline = page_data_soup.find('h1', itemprop="headline").text
            len_headline = len(headline)
            body = ''
            for tag in page_data_soup.find_all('p', class_='story-body-text story-content'):
                body += " "*(len(body)!=0) + tag.text
            dict_solution = {'author_name':author_name, "links":links, "headline":headline,"body":body, "url":url}
            return dict_solution
        except:
            return None        

urls = get_nyt_urls(month,year)

if N==0: N=len(urls)

data = []

for x in range(0,N):
    print(x, "Fetching data from", urls[x])
    data.append(html_to_factors_nytimes(urls[x]))
    
import pickle

fileName = 'nyt-'+str(month)+'-'+str(year)+'.pkl'
with open(fileName, 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
print("Saved data to "+fileName)