def html_to_factors_nytimes(url):
    """
    Given a url from nytimes, this function returns a dictionary which contains the name of the author, 
    number of links on the website, the headline and the body.
    """
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get(url)
    if response.status_code == 200:
        page_data_soup = BeautifulSoup(response.content,'lxml')
        author_name = page_data_soup.find('span', class_='byline-author').text
        links = [link.get('href') for link in page_data_soup.find_all('a', href=True)]
        headline = page_data_soup.find('h1', itemprop="headline").text
        len_headline = len(headline)
        body = ''
        for tag in page_data_soup.find_all('p', class_='story-body-text story-content'):
            body += tag.text
        dict_solution = {'author_name':author_name, "links":links, "headline":headline,"body":body}
        return dict_solution

def html_to_factors_21cent(url):
    """
    Given a url from 21cent , this function returns a dictionary which contains the name of the author, 
    number of links on the website, the headline and the body.
    """
    import requests
    from bs4 import BeautifulSoup
    
    response = requests.get(url)
    if response.status_code == 200:
        page_data_soup = BeautifulSoup(response.content,'lxml')  
        author_name = page_data_soup.find('a', rel='author').text
        links = [link.get('href') for link in page_data_soup.find_all('a', href=True)]
        headline = page_data_soup.find('h1', class_="entry-title").text
        body = ''
        for tag in page_data_soup.find_all('p'):
            body += tag.text
        dict_solution = {'author_name':author_name, "links":links, "headline":headline,"body":body}
        return dict_solution