
# coding: utf-8

# In[2]:


import pandas as pd
from datetime import datetime
import requests
import time
import bs4
import re
import json
from apscheduler.schedulers.blocking import BlockingScheduler
import logging


# In[3]:


base_url='https://стопкоронавирус.рф/'


# In[4]:


filename='logfile.log'
def log(msg):
    logging.basicConfig(format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        filename=filename)
    logging.warning(msg)


# In[5]:


def get_session(url):
    url = url
    s = requests.session()
    r = s.get(url)
    return(r)


# In[6]:


def get_data(base_url):
    currtime = time.localtime()
    date=time.strftime('%Y-%m-%d',currtime)
    r = get_session(base_url)
    soup = bs4.BeautifulSoup(r.text,'html.parser')
    date_note=soup.find_all('div',attrs={'class':'cv-banner__description'})
    date_text=date_note[0].string
    reg_table = soup.find_all('div', attrs={'class':'d-map__list'})
    res=pd.DataFrame(columns=['date','name','sick','healed','died','date_text'])
    for tr in reg_table[0].find('table'):
        tmp=dict()
        name=tr.find('th').string
        sick=tr.find_all('td')[0].get_text(' ')
        healed=tr.find_all('td')[1].get_text(' ')
        died=tr.find_all('td')[2].get_text(' ')
        tmp['name']=name
        tmp['sick']=sick
        tmp['healed']=healed
        tmp['died']=died
        tmp['date_text']=date_text
        tmp['date']=date
        res=res.append(tmp,ignore_index=True)
    return res
    


# In[9]:


def job():
    try:
        currtime = time.localtime()
        date=time.strftime('%Y-%m-%d',currtime)
        res=get_data(base_url)
        res.to_csv('stopkv_data%s.csv'%date,index=False)
        data=pd.read_csv('stopkv_data.csv')
        data=data.append(res, sort=False)
        log(data.shape)
        data.to_csv('stopkv_data.csv',index=False)
    except IOError as e:
        log('%s error '%(e))


# In[ ]:


job()
scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', hours=24, misfire_grace_time=4)
scheduler.start()


# In[221]:


#res.to_csv('stopkv_data%s.csv'%date,index=False)

