class Morph:
    def __init__(self,morph):
        surface,attr=morph.split('\t')
        attr=attr.split(',')
        self.surface=surface
        self.base=attr[6]
        self.pos=attr[0]
        self.pos1=attr[1]

filename='./ai.ja.txt.parsed'
sentences=[]
morphs=[]
with open(filename,mode='r')as f:
    for line in f:
        if line[0]=='*':
            continue
        elif line!='EOS\n':
            morphs.append(Morph(line))
        else:
            sentences.append(morphs)
            morphs=[]
for m in sentences[2]:
    print(vars(m))