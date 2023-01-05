import pandas as pd

def output(N,data):
    print(data.head(N))

data=pd.read_table('name.txt',header=None,sep='\t',names=['name','sex','number','year'])
N=int(input())
output(N,data)

#$ head -n 7 ./name.txt 