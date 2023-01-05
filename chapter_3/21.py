import re

with open('text_uk')as f:
    F=f.read()
pattern = r'^(.*\[\[Category:.*\]\].*)$'
result='\n'.join(re.findall(pattern,F,re.MULTILINE))
print(result)


#https://murashun.jp/article/programming/regular-expression.html
#https://docs.python.org/ja/3/library/re.html