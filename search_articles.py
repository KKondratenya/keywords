import re

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
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

stemmer=SnowballStemmer('russian')

def search_user_library(username,q='',mode='title'):
    try:
        q = re.sub("[^а-яА-Яa-zA-Z0-9]", " ", q)
        q = q.lower()
        words=q.split()
        words = [w for w in words if not w in stops]
        words = [stemmer.stem(w) for w in words]
        if words=='':
            return "некорректный ввод"

        if mode=='author':
            Query = 'SELECT * FROM dataset.'+username+' WHERE AUTHORS LIKE \''
            for word in words:
                Query+='%{}'.format(word)
            Query += '%\''
            print(Query)
            df = gbq.read_gbq(Query, project_id, credentials=credentials)
            print(df.values.tolist())
            if df.values.tolist()==[]:
                Query = 'SELECT * FROM dataset.'+username+' WHERE AUTHORS LIKE \'%{}%\''.format(q)
                print(Query)
                df = gbq.read_gbq(Query, project_id, credentials=credentials)

        if mode=='title':
    #         words = [morph.parse(w)[0].normal_form for w in words]
            Query = 'SELECT * FROM dataset.'+username+' WHERE TITLE LIKE \''
            for word in words:
                Query+='%{}'.format(word)
            Query += '%\''
            print(Query)
            df = gbq.read_gbq(Query, project_id, credentials=credentials)
            print(df.values.tolist())
            if df.values.tolist()==[]:
                Query = 'SELECT * FROM dataset.'+username+' WHERE TITLE LIKE \'%{}%\''.format(q)
                print(Query)
                df = gbq.read_gbq(Query, project_id, credentials=credentials)

        if mode=='kws':
    #         words = [morph.parse(w)[0].normal_form for w in words]
            Query = 'SELECT * FROM dataset.'+username+' WHERE KEYWORDS LIKE \''
            for word in words:
                Query+='%{}'.format(word)
            Query += '%\''
            print(Query)
            df = gbq.read_gbq(Query, project_id, credentials=credentials)
            print(df.values.tolist())
            if df.values.tolist()==[]:
                Query = 'SELECT * FROM dataset.'+username+' WHERE KEYWORDS LIKE \'%{}%\''.format(q)
                print(Query)
                df = gbq.read_gbq(Query, project_id, credentials=credentials)
        result = df.values.tolist()
        if result==[]:
            return result
        else:
            return result
    except TransportError:
        return False
    except:
        return -1


stemmer=SnowballStemmer('russian')

def search(q='',mode='title'):
    print(mode)
    try:
        q = re.sub("[^а-яА-Яa-zA-Z0-9]", " ", q)
        q = q.lower()
        words=q.split()
        words = [w for w in words if not w in stops]
        words = [stemmer.stem(w) for w in words]
        if words=='':
            return "некорректный ввод"

        if mode=='author':
            Query = 'SELECT * FROM dataset.search_rsl_ru WHERE AUTHORS LIKE \''
            for word in words:
                Query+='%{}'.format(word)
            Query += '%\''
            print(Query)
            df = gbq.read_gbq(Query, project_id, credentials=credentials)
            print(df.values.tolist())
            if df.values.tolist()==[]:
                Query = 'SELECT * FROM dataset.search_rsl_ru WHERE AUTHORS LIKE \'%{}%\''.format(q)
                print(Query)
                df = gbq.read_gbq(Query, project_id, credentials=credentials)

        if mode=='title':
    #         words = [morph.parse(w)[0].normal_form for w in words]
            Query = 'SELECT * FROM dataset.search_rsl_ru WHERE TITLE LIKE \''
            for word in words:
                Query+='%{}'.format(word)
            Query += '%\''
            print(Query)
            df = gbq.read_gbq(Query, project_id, credentials=credentials)
            print(df.values.tolist())
            if df.values.tolist()==[]:
                Query = 'SELECT * FROM dataset.search_rsl_ru WHERE TITLE LIKE \'%{}%\''.format(q)
                print(Query)
                df = gbq.read_gbq(Query, project_id, credentials=credentials)

        if mode=='kws':
    #         words = [morph.parse(w)[0].normal_form for w in words]
            Query = 'SELECT * FROM dataset.search_rsl_ru WHERE KEYWORDS LIKE \''
            for word in words:
                Query+='%{}'.format(word)
            Query += '%\''
            print(Query)
            df = gbq.read_gbq(Query, project_id, credentials=credentials)
            print(df.values.tolist())
            if df.values.tolist()==[]:
                Query = 'SELECT * FROM dataset.search_rsl_ru WHERE KEYWORDS LIKE \'%{}%\''.format(q)
                print(Query)
                df = gbq.read_gbq(Query, project_id, credentials=credentials)
        result = df.values.tolist()
        if result==[]:
            return []
        else:
            return result
    except TransportError:
        return False
    except:
        return -1

# search(mode='kws',q='колебания механических')

# search_user_library(username='kirill',mode='title',word='физика ')

# search_user_library(username='kirill',mode='title',word='физика ')