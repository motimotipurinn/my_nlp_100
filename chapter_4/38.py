from collections import defaultdict
import matplotlib.pyplot as plt
import japanize_matplotlib
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

ans=defaultdict(int)
for sentence in sentences:
    for morph in sentence:
        if morph['pos']!='記号':
            ans[morph['base']]+=1
ans=ans.values()
plt.figure(figsize=(8, 4))
plt.hist(ans,bins=100)
plt.xlabel('出現頻度')
plt.ylabel('単語の種類数')
plt.show()
