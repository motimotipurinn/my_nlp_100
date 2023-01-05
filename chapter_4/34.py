filename = './neko.txt.mecab'

sentences = []
morphs = []
with open(filename, mode='r') as f:
  for line in f:  
    if line != 'EOS\n': 
      fields = line.split('\t')
      if len(fields) != 2 or fields[0] == '':
        continue
      else:
        attr =  fields[1].split(',')
        morph = {'surface': fields[0], 'base': attr[6], 'pos': attr[0], 'pos1': attr[1]}
        morphs.append(morph)
    else:
      sentences.append(morphs)
      morphs = []

ans=set()
for sentence in sentences:
    nouns=''
    num=0
    for morth in sentence:
        if morth['pos']=='名詞':
            nouns=''.join([nouns,morth['surface']])
            num+=1
        elif num>=2:
            ans.add(nouns)
            nouns=''
            num=0
        else:
            nouns=''
            num=0
print(len(ans))
for v in list(ans)[:10]:
    print(v)