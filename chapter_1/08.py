def cipher(str):
    C=[chr(219-ord(x))if x.islower() else x for x in str]
    return ''.join(C)

M='I am  an apple'
C=cipher(M)
print(C)
print(cipher(C))