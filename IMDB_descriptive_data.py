#!/usr/bin/env python
# coding: utf-8

# # ETL ( Extraction, Transformation, Loading) part

# # Extraction

# In[2]:


import pandas as pd

pd.set_option('display.max_colwidth', None)


import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Find the total number of pages
num_pages = 10

# Loop through each page and extract movie information
for i in range(1, num_pages+1):
    page_url = f'{url}?page={i}'
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    


# In[3]:


# Find all the movie items on the page
movie_items = soup.find_all('div', {'class': 'lister-item-content'})
data = []
# Loop through each movie item and extract the required information
for item in movie_items:
    total = {}
    total['title'] = item.h3.a.text
    total['year'] = item.find('span', {'class': 'lister-item-year'}).text.strip('()')
    total['rating'] = item.find('div', {'class': 'inline-block ratings-imdb-rating'}).text.strip()
    total['runtime'] = item.find('span', {'class': 'runtime'}).text         
    total['description'] = item.find_all('p')[1].text.strip()
    total['genre'] = item.find('span', {'class': 'genre'}).text.strip()

    data.append(total)
        


# In[4]:


data


# ## Transformation

# In[5]:


imdb = pd.DataFrame(data)
imdb


# In[6]:


imdb['year'] = imdb['year'].str.replace('[^a-zA-Z0-9\w\s]', '', regex=True)


# In[7]:


import re

imdb['year'] = imdb['year'].apply(lambda x: re.findall('\d+', str(x))[0]).astype(int)


# In[8]:


imdb['runtime_in_min'] = imdb['runtime'].apply(lambda x: re.findall('\d+', str(x))[0]).astype(float)


# In[9]:


imdb['rating'] = imdb['rating'].astype(float)


# In[10]:


imdb['year'] = imdb['year'].astype(int)


# In[11]:


imdb['rating'] = imdb['rating'].astype(float)


# In[13]:


unique_values = imdb['year'].unique()
unique_values


# In[14]:


imdb.info()


# In[15]:


imdb.head()


# In[16]:


imdb = imdb.drop('runtime', axis=1)
imdb.head()


# In[17]:


imdb


# # Loading 

# In[18]:


IMDB_descriptive_data = imdb


# In[19]:


output_file = r'C:\Users\ashut\Downloads\IMDB_descriptive_data.csv'

# write the dataframe to a CSV file at the desired location
IMDB_descriptive_data.to_csv(output_file, index=False)


# In[20]:


file_path = r'C:\Users\ashut\Downloads\IMDB_descriptive_data.json'
IMDB_descriptive_data.to_json(file_path, orient='records')


# In[ ]:




