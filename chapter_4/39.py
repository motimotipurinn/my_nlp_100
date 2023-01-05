from collections import defaultdict
import matplotlib.pyplot as plt
import japanize_matplotlib
import math
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
ans=sorted(ans.items(),key=lambda x:x[1],reverse=True)
ranks=[r+1 for r in range(len(ans))]
values=[a[1]for a in ans]
plt.figure(figsize=(8, 4))
plt.scatter(ranks,values)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('出現頻度順位')
plt.ylabel('出現頻度')
plt.show()
