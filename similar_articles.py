from keyphrase_extraction import keyword_extraction
from annotation import TextRank
import re
import pickle
from sklearn.neighbors import NearestNeighbors

def treatment_text(review):
    try:
        review_text = re.sub("[^а-яА-Яa-zA-Z0-9]", " ", review)
        words = review_text.lower().split()
        words = [w for w in words if not w in stops]
        words = [morph.parse(w)[0].normal_form for w in words]
        words = [stemmer.stem(w) for w in words]
        words = [w for w in words if not w in stops]
        return(' '.join(words))
    except:
        return review

with open('vectorizer.pickle', 'rb') as f:
    vectorizer = pickle.load(f)

with open('knn.pickle', 'rb') as f:
    neigh = pickle.load(f)

with open('dataset.pickle', 'rb') as f:
    df = pickle.load(f)

ann_extr = TextRank()

def create_description(text,str_kws,str_ann):
    if str_ann=='' or str_ann=='\n':
        str_ann = ann_extr.extract(text)
    if str_kws=='' or str_kws=='\n':
        str_kws = keyword_extraction(text)
    return [text,str_kws,str_ann]


# with open('vectorizer.pickle', 'rb') as f:
#     vectorizer = pickle.load(f)

# with open('knn.pickle', 'rb') as f:
#     neigh = pickle.load(f)
def find_similar(text,kws,ann):
    s = kws+ann
    s = treatment_text(s)
    s = vectorizer.transform([s])
    s = s.toarray()
    result = neigh.kneighbors(s)[1][0]
    r =[]
    for i in result:
        r.append(df.loc[i][['author','title','keywords']].values.tolist())
    return r

from google.oauth2 import service_account
project_id = 'arctic-task-238719'
private_key='arctic-task-238719-e6a1c5fe056b.json'
import json
from google.cloud import bigquery
credentials = service_account.Credentials.from_service_account_file('./arctic-task-238719-e6a1c5fe056b.json')
from pandas.io import gbq
from sklearn.feature_extraction.text import TfidfVectorizer

def similar_articles_from_user_library(username,text,kws,ann):
    try:
        Query = 'SELECT * FROM dataset.'+username
        df = gbq.read_gbq(Query, project_id, credentials=credentials)
        df['title_kws'] = df['title']+df['keywords']
        df['title_kws'] = df['title_kws'].apply(treatment_text)
        x = df['title_kws'].values.tolist()
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(x)
        neigh = NearestNeighbors(n_neighbors=5).fit(X)
        s = treatment_text(kws+ann)
        s = vectorizer.transform([s]).toarray()
        result = neigh.kneighbors(s)[1][0]
        r =[]
        for i in result:
            r.append(df.loc[i][['authors','title','keywords']].values.tolist())
        return r
    except TransportError:
        return False
    except:
        return -1

    
# find_similar('колебание коэффициент демпфирования модуль упругость установка','','')

# with open ('./spiderman.txt',encoding='utf-8') as f:
#     reader=f.read()
#     text=''
#     for i in reader:
#         text+=i
#
# x=create_description(text,'','')
# print(x[1])
# print(x[2])


# from rake import RAKE
# r = RAKE()
# keywords = r.keywords_extract(text)
# keywords = ', '.join(keywords).capitalize()
# print('**'*2,keywords)