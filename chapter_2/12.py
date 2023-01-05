import pandas as pd

data=pd.read_table('name.txt',header=None,sep='\t',names=['name','sex','number','year'])
col1=data['name']
col1.to_csv('./col1.txt',index=False)
print(col1.head())
col2=data['sex']
col2.to_csv('./col2.txt',index=False)
print(col2.head())

#cut -f 1 ./name.txt > col1_chk.txt
#cut -f 1 ./name.txt > col2_chk.txt