import pandas as pd

data=pd.read_table('name.txt',header=None,sep='\t',names=['name','sex','number','year'])
print(data['name'].value_counts())

#$ cut -f 1 ./name.txt | sort | uniq | wc -l