import pandas as pd

def split_file(N,data):
    tmp=data.reset_index(drop=False)
    data_cut=pd.qcut(tmp.index,N,labels=[i for i in range(N)])
    data_cut=pd.concat([data,pd.Series(data_cut,name='sp')],axis=1)
    return data_cut

data=pd.read_table('name.txt',header=None,sep='\t',names=['name','sex','number','year'])
N=int(input())
data_cut=split_file(N,data)
print(data_cut['sp'].value_counts())
print(data_cut.head())

#$ split -l 200 -d ./names.txt sp