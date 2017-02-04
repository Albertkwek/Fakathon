def html_to_factors_general(url):
    """
    Given a general website, this function returns a dictionary which the links on the website, the headline,
    the body and the url.
    
    """
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            page_data_soup = BeautifulSoup(response.content,'lxml')
            links = [link.get('href') for link in page_data_soup.find_all('a', href=True)]
            headline = page_data_soup.find('h1').text
            body = ''
            for tag in page_data_soup.find_all('p'):
                body += " "*(len(body)!=0) + tag.text
            dict_solution = {"links":links, "headline":headline,"body":body}
            return dict_solution
        except:
            return None
    
def html_to_factors_nytimes(url):
    """
    Given a url from nytimes, this function returns a dictionary which contains the name of the author, 
    number of links on the website, the headline and the body.
    """
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            page_data_soup = BeautifulSoup(response.content,'lxml')
            author_name = page_data_soup.find('span', class_='byline-author').text
            links = [link.get('href') for link in page_data_soup.find_all('a', href=True)]
            headline = page_data_soup.find('h1', itemprop="headline").text
            body = ''
            for tag in page_data_soup.find_all('p', class_='story-body-text story-content'):
                body += " "*(len(body)!=0) + tag.text
            dict_solution = {'author_name':author_name, "links":links, "headline":headline,"body":body, "url":url}
            return dict_solution
        except:
            return None

def html_to_factors_21cent(url):
    """
    Given a url from 21cent , this function returns a dictionary which contains the name of the author, 
    number of links on the website, the headline and the body.
    """
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            page_data_soup = BeautifulSoup(response.content,'lxml')  
            author_name = page_data_soup.find('a', rel='author').text
            links = [link.get('href') for link in page_data_soup.find_all('a', href=True)]
            headline = page_data_soup.find('h1', class_="entry-title").text
            body = ''
            for tag in page_data_soup.find_all('p'):
                body += " "*(len(body)!=0) + tag.text
            dict_solution = {'author_name':author_name, "links":links, "headline":headline,"body":body, "url":url}
            return dict_solution
        except:
            return None


def html_to_factors_infowars(url):
    """
    Given a url from InfoWars , this function returns a dictionary which contains the name of the author, 
    number of links on the website, the headline and the body.
    """
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            page_data_soup = BeautifulSoup(response.content,'lxml')
            author_name = page_data_soup.find('span', class_="author").find('a').text
            links = [link.get('href') for link in page_data_soup.find_all('a', href=True)]
            headline = page_data_soup.find('h1', class_="entry-title").text
            body = ''
            for tag in page_data_soup.find('article').find_all('p'):
                body += " "*(len(body)!=0) + tag.text
            dict_solution = {'author_name':author_name, "links":links, "headline":headline,"body":body}
            return dict_solution
        except:
            return None

def scrap_RNRN_web():
    """
    This function takes down all the web urls from RNRN
    and return them as a list
    """
    url = "http://realnewsrightnow.com/"
    import requests
    from bs4 import BeautifulSoup

    rnrn_url = []

    response = requests.get(url)
    if response.status_code == 200:
        page_data_soup = BeautifulSoup(response.content,'lxml')
        cat_avoid = {'Home','About'}
        for tag in page_data_soup.find('ul', id="menu-main-navigation-1").find_all('li'):
            if tag.text not in cat_avoid:
                category_link = tag.find('a').get('href')
                newresponse = requests.get(category_link)
                if newresponse.status_code == 200:
                    new_page_data_soup = BeautifulSoup(newresponse.content,'lxml')
                    rnrn_url.extend([item.find('a').get('href') for item in new_page_data_soup.find_all(['h3','h5'],itemprop = "headline")])

def scrap_21_cent_web():
    """
    This function takes down all the web urls from cent21
    and return them as a list
    """
    url = "http://21stcenturywire.com/"
    import requests
    from bs4 import BeautifulSoup

    cent21_url = []

    response = requests.get(url)
    if response.status_code == 200:
        page_data_soup = BeautifulSoup(response.content,'lxml')
        parent = page_data_soup.find('ul', id="menu-main")
        for child in parent.find_all('li', id=lambda x:x and x.startswith('menu-item-')):
            category_link = child.find('a')['href']
            newresponse = requests.get(category_link)
            if newresponse.status_code == 200:
                new_page_data_soup = BeautifulSoup(newresponse.content,'lxml')
                cent21_url.extend([item.find('a').get('href') for item in new_page_data_soup.find_all('h2', class_="entry-title")])
    return cent21_url

def scrap_infowars_web():
    """
    This function takes down all the web urls from InfoWars
    and return them as a list
    """
    url = "http://www.infowars.com/"
    import requests
    from bs4 import BeautifulSoup

    infowars_url = []

    response = requests.get(url)
    if response.status_code == 200:
        page_data_soup = BeautifulSoup(response.content,'lxml')
        for tag in page_data_soup.find('li', id="menu-item-216953").find_all('li'):
            category_link = tag.find('a').get('href')
            newresponse = requests.get(category_link)
            if newresponse.status_code == 200:
                new_page_data_soup = BeautifulSoup(newresponse.content,'lxml')
                infowars_url.extend([div.find('h3').find('a').get('href') for div in new_page_data_soup.find_all('div', class_="article pure-u-xs-1-1 pure-u-sm-1-2 pure-u-lg-1-2 pure-u-xl-1-2 ")])
                    
    return infowars_url