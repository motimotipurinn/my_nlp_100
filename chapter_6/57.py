import string
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt 
from sklearn.metrics import precision_score ,recall_score,f1_score



def preprocessing(text):
    table=str.maketrans(string.punctuation,' '*len(string.punctuation))
    text=text.translate(table)
    text=text.lower()
    text=re.sub('[0-9]+', '0', text)
    return text

def score_lg(lg,X):
    return [np.max(lg.predict_proba(X),axis=1),lg.predict(X)]

df=pd.read_csv('./newsCorpora_re.csv',header=None,sep='\t',names=['ID', 'TITLE', 'URL', 'PUBLISHER', 'CATEGORY', 'STORY', 'HOSTNAME', 'TIMESTAMP'])
df = df.loc[df['PUBLISHER'].isin(['Reuters', 'Huffington Post', 'Businessweek', 'Contactmusic.com', 'Daily Mail']), ['TITLE', 'CATEGORY']]
train,valid_test=train_test_split(df,test_size=0.2,shuffle=True,random_state=123,stratify=df['CATEGORY'])
valid,test=train_test_split(valid_test,test_size=0.5,shuffle=True,random_state=123,stratify=valid_test['CATEGORY'])
df=pd.concat([train,valid,test],axis=0)
df.reset_index(drop=True,inplace=True)
df['TITLE']=df['TITLE'].map(lambda x:preprocessing(x))

train_valid=df[:len(train)+len(valid)]
test=df[len(train)+len(valid):]
vec_tfidf=TfidfVectorizer(min_df=10,ngram_range=(1,2))
X_train_valid=vec_tfidf.fit_transform(train_valid['TITLE'])
X_test=vec_tfidf.transform(test['TITLE'])

X_train_valid=pd.DataFrame(X_train_valid.toarray(),columns=vec_tfidf.get_feature_names_out())
X_test=pd.DataFrame(X_test.toarray(),columns=vec_tfidf.get_feature_names_out())
X_train=X_train_valid[:len(train)]
X_valid=X_train_valid[len(train):]

lg=LogisticRegression(random_state=123,max_iter=10000)
lg.fit(X_train,train['CATEGORY'])
train_pred=score_lg(lg,X_train)
test_pred=score_lg(lg,X_test)

features=X_train.columns.values
index=[i for i in range(1,11)]
for c,coef in zip(lg.classes_,lg.coef_):
    print(f'[????????????]{c}')
    best10=pd.DataFrame(features[np.argsort(coef)[::-1][:10]],columns=['???????????????'],index=index).T
    worst10=pd.DataFrame(features[np.argsort(coef)[:10]],columns=['???????????????'],index=index).T
    print(pd.concat([best10,worst10],axis=0))
    print('\n')