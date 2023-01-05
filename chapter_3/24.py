import re

with open('text_uk')as f:
    F=f.read()
pattern = r'\[\[ファイル:(.+?)\|'
result='\n'.join(re.findall(pattern,F,re.MULTILINE))
print(result)
