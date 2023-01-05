import re

with open('text_uk')as f:
    F=f.read()
pattern = r'^(\={2,})\s*(.+?)\s*(\={2,}).*$'
result = '\n'.join(i[1]+':'+str(len(i[0])-1)for  i in re.findall(pattern, F, re.MULTILINE))
print(result)