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
  l1_ratio = trial.suggest_uniform('l1_ratio', 0, 1)
  C = trial.suggest_loguniform('C', 1e-4, 1e4)
  lg = LogisticRegression(random_state=123, 
                          max_iter=10000, 
                          penalty='elasticnet', 
                          solver='saga', 
                          l1_ratio=l1_ratio, 
                          C=C)
  lg.fit(X_train, train['CATEGORY'])
  valid_pred = score_lg(lg, X_valid)
  valid_accuracy = accuracy_score(valid['CATEGORY'], valid_pred[1])    
  return valid_accuracy 


study = optuna.create_study(direction='maximize')
study.optimize(objective_lg, timeout=3600)

# 結果の表示
print('Best trial:')
trial = study.best_trial
print('  Value: {:.3f}'.format(trial.value))
print('  Params: ')
for key, value in trial.params.items():
  print('    {}: {}'.format(key, value))
l1_ratio = trial.params['l1_ratio']
C = trial.params['C']

# モデルの学習
lg = LogisticRegression(random_state=123, 
                        max_iter=10000, 
                        penalty='elasticnet', 
                        solver='saga', 
                        l1_ratio=l1_ratio, 
                        C=C)
lg.fit(X_train, train['CATEGORY'])

# 予測値の取得
train_pred = score_lg(lg, X_train)
valid_pred = score_lg(lg, X_valid)
test_pred = score_lg(lg, X_test)

# 正解率の算出
train_accuracy = accuracy_score(train['CATEGORY'], train_pred[1]) 
valid_accuracy = accuracy_score(valid['CATEGORY'], valid_pred[1]) 
test_accuracy = accuracy_score(test['CATEGORY'], test_pred[1]) 

print(f'正解率（学習データ）：{train_accuracy:.3f}')
print(f'正解率（検証データ）：{valid_accuracy:.3f}')
print(f'正解率（評価データ）：{test_accuracy:.3f}')