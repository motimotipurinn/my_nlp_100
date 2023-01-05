import json

filename='jawiki-country.json'
with open(filename,mode='r')as f:
    for line in f:
        line=json.loads(line)
        if line['title']=='イギリス':
            F = open('text_uk', 'x', encoding='UTF-8')
            F.write(line['text'])
            break
#$ wget https://nlp100.github.io/data/jawiki-country.json.gz
#$ gzip -d jawiki-country.json.gz 