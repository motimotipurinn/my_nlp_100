import random
def shuffle(str):
    result=[]
    for word in str.split():
        if len(word)>4:
            word=word[:1]+''.join(random.sample(word[1:-1],len(word)-2))+word[-1:]
        result.append(word)
    return ' '.join(result)

str="I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
print(shuffle(str))