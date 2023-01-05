import pandas as pd

def output(N,data):
    print(data.tail(N))

data=pd.read_table('name.txt',header=None,sep='\t',names=['name','sex','number','year'])
N=int(input())
output(N,data)

#$ tail -n 7 ./name.txt 