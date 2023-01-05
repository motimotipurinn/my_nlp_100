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
from tqdm import tqdm
import optuna
import xgboost as xgb



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

def objective_lg(trial):
    l1_ratio=trial.suggest_uniform('l1_ratio',0,1)
    C=trial.suggest_loguniform('C',1e-4,1e4)
    lg=LogisticRegression(
        random_state=123,
        max_iter=10000,
        penalty='elasticnet',
        solver='saga',
        l1_ratio=l1_ratio,
        C=C,
    )
    lg.fit(X_train,train['CATEGORY'])
    valid_pred=score_lg(lg,X_train)
    valid_accuracy = accuracy_score(valid['CATEGORY'], valid_pred[1])
    return valid_accuracy


params={'objective': 'multi:softmax', 
        'num_class': 4,
        'eval_metric': 'mlogloss',
        'colsample_bytree': 1.0, 
        'colsample_bylevel': 0.5,
        'min_child_weight': 1,
        'subsample': 0.9, 
        'eta': 0.1, 
        'max_depth': 5,
        'gamma': 0.0,
        'alpha': 0.0,
        'lambda': 1.0,
        'num_round': 1000,
        'early_stopping_rounds': 50,
        'verbosity': 0
        }

# XGBoost用にフォーマット変換
category_dict = {'b': 0, 'e': 1, 't':2, 'm':3}
y_train = train['CATEGORY'].map(lambda x: category_dict[x])
y_valid = valid['CATEGORY'].map(lambda x: category_dict[x])
y_test = test['CATEGORY'].map(lambda x: category_dict[x])
dtrain = xgb.DMatrix(X_train, label=y_train)
dvalid = xgb.DMatrix(X_valid, label=y_valid)
dtest = xgb.DMatrix(X_test, label=y_test)

# モデルの学習
num_round = params.pop('num_round')
early_stopping_rounds = params.pop('early_stopping_rounds')
watchlist = [(dtrain, 'train'), (dvalid, 'eval')]
model = xgb.train(params, dtrain, num_round, evals=watchlist, early_stopping_rounds=early_stopping_rounds)

train_pred = model.predict(dtrain, ntree_limit=model.best_ntree_limit)
valid_pred = model.predict(dvalid, ntree_limit=model.best_ntree_limit)
test_pred = model.predict(dtest, ntree_limit=model.best_ntree_limit)

# 正解率の算出
train_accuracy = accuracy_score(y_train, train_pred) 
valid_accuracy = accuracy_score(y_valid, valid_pred) 
test_accuracy = accuracy_score(y_test, test_pred) 

print(f'正解率（学習データ）：{train_accuracy:.3f}')
print(f'正解率（検証データ）：{valid_accuracy:.3f}')
print(f'正解率（評価データ）：{test_accuracy:.3f}')