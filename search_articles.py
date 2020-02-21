import re

from nltk.corpus import stopwords

import pymorphy2
from google.oauth2 import service_account
project_id = 'arctic-task-238719'
private_key='arctic-task-238719-e6a1c5fe056b.json'
import json
from google.cloud import bigquery
credentials = service_account.Credentials.from_service_account_file('./arctic-task-238719-e6a1c5fe056b.json')
from pandas.io import gbq
stops = set(stopwords.words("english")) | set(stopwords.words("russian"))
import pandas as pd
morph=pymorphy2.MorphAnalyzer()

def search(word='',mode='title'):
    word = re.sub("[^а-яА-Яa-zA-Z0-9]", " ", word)
    words = word.lower().split()
    words = [w for w in words if not w in stops]
    if words=='':
        return "некорректный ввод"

    if mode=='author':
        Query = 'SELECT * FROM dataset.search_rsl_ru WHERE AUTHOR LIKE \''
        for word in words:
            Query+='%{}'.format(word)
        Query += '%\''
        df = gbq.read_gbq(Query, project_id, credentials=credentials)

    if mode=='title':
        words = [morph.parse(w)[0].normal_form for w in words]
        Query = 'SELECT * FROM dataset.search_rsl_ru WHERE TITLE LIKE \''
        for word in words:
            Query+='%{}'.format(word)
        Query += '%\''
        df = gbq.read_gbq(Query, project_id, credentials=credentials)

    if mode=='kws':
        words = [morph.parse(w)[0].normal_form for w in words]
        Query = 'SELECT * FROM dataset.search_rsl_ru WHERE KEYWORDS LIKE \''
        for word in words:
            Query+='%{}'.format(word)
        Query +='%\''
        df = gbq.read_gbq(Query, project_id, credentials=credentials)
    
    return df.values.tolist()


