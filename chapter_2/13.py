import pandas as pd

col1=pd.read_table('col1.txt')
col2=pd.read_table('col2.txt')
col_merged=pd.concat([col1,col2],axis=1)
col_merged.to_csv('./col_merged.txt',sep='\t',index=False)
print(col_merged.head())

#$ paste ./col1.txt ./col2.txt | head -n 10