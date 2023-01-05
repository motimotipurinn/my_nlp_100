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
    for morph in sentence:
        if morph['pos']=='動詞':
            ans.add(morph['surface'])

print(len(ans))
for v in list(ans)[:10]:
    print(v)