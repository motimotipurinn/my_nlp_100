import pandas as pd

data=pd.read_table('name.txt',header=None,sep='\t',names=['name','sex','number','year'])
data.sort_values(by='number',ascending=False,inplace=True)
print(data.head())

#$ cat ./name.txt | sort -rnk 3 |head -n 10