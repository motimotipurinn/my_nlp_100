def n_gram(n,str):
    return list(zip(*[str[i:]for i in range(n)]))

str1="paraparaparadise"
str2="paragraph"
X=set(n_gram(2,str1))
Y=set(n_gram(2,str2))
print(X|Y)
print(X&Y)
print(X-Y)
print({('s','e')}<=X)
print({('s','e')}<=Y)