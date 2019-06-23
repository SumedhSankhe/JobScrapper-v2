# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 18:07:22 2019

@author: sumedh
"""

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from tqdm import tqdm
from datetime import datetime


def log_error(e):
    print(e)


def create_url(website, title ='', location = ''):
    '''
    Attempts to format the url to get the right title and location
    '''
    
    website = website.lower()
    if website in ('indeed','monster'):
        if website == 'indeed':
            title = title.replace(' ','+')
            location = location.replace(',','%2C')
            location = location.replace(' ','+')
            url = 'https://www.indeed.com/jobs?q={}&l={}'.format(title, location)         
    else:
        log_error('Incorrect Website, Website not yet included') 
    
    return url

def get_url(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return BeautifulSoup(resp.content, 'html.parser')
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
        

def job_extract(div):
    '''
    Extracts the job title from the soup
    '''
    jobs = [j['title'] if j['title'] else 'Not Found' for j in div.find_all(name = 'a', attrs = {'data-tn-element':'jobTitle'})]
    return jobs[0]

def company_extract(div):
    '''
    Extracts company name from the soup
    '''
    comp = [d.text.strip() if d is not None else print('Fucked') for d in div.find_all(name = 'span', attrs = {'class':'company'})]
    return comp[0]


def extract_from_soup1(soup):
    jobs = []
    companies = []
    code = []
    for div in soup.find_all(name='div', attrs={'data-tn-component': 'organicJob'}):
        jobs.append(job_extract(div))
        companies.append(company_extract(div))
        code.append(div['data-jk'])
    
    df = pd.DataFrame({'Job_Id': code,
                       'Title': jobs,
                       'Company': companies})
    return df


def paiginate(**kwargs):
    ''' 
    Gets number of pages to paginate through
    '''
    url = create_url(kwargs['website'], kwargs['title'], kwargs['location'])
    soup = get_url(url)
    
    pg = soup.find(name = 'div', attrs = {'id':'searchCount'}).text.split(' ')[-2]
    pg = int(pg.replace(',',''))
    
    if kwargs['limit'] < pg:
        pg = kwargs['limit']
    
    df_list = []
    
    for r in tqdm(range(0,pg,10)):
        URL = url+'&start={}&limit={}'.format(pg,pg+10)
        new_soup = get_url(URL)
        df_list.append(extract_from_soup1(new_soup))
        sleep(0.03)
    
    df = pd.concat(df_list)
    df = df.drop_duplicates('Job_Id')
    path= 'D:\\Github\\JobScrapper-v2\\daily_data\\'
    fname = str(datetime.today().strftime('%Y-%m-%d'))
    fname = path+fname+'.csv'
    df.to_csv(fname, index = False)
    
    return print('Done')


paiginate(website = 'indeed', title = 'data scientist', location = 'boston', limit = 20)

