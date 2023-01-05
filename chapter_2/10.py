#$ wc name.txt -l
import pandas as pd

data=pd.read_table('name.txt',header=None,sep='\t',names=['name','sex','number','year'])
print(len(data))