def n_gram(n,str):
    return list(zip(*[str[i:]for i in range(n)]))

str="I am an NLPer"
print(n_gram(2,str.split()))
print(n_gram(2,str))