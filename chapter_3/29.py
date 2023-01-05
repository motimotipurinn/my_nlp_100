import re
import requests
def remove_markup(text):
    pattern= r'\'{2,5}'
    text=re.sub(pattern,'',text)
    pattern = r'\[\[(?:[^|]*?\|)??([^|]*?)\]\]'
    text=re.sub(pattern,r'\1',text)
    pattern = r'<.+?>' 
    text = re.sub(pattern, '', text)
    pattern = r'https?://[\w!?/\+\-_~=;\.,*&@#$%\(\)\'\[\]]+'
    text = re.sub(pattern, '', text)
    pattern = r'\{\{(?:lang|仮リンク)(?:[^|]*?\|)*?([^|]*?)\}\}' 
    text = re.sub(pattern, r'\1', text)
    return text

def get_url(text):
    url_file=text['国旗画像'].replace(' ','_')
    url='https://commons.wikimedia.org/w/api.php?action=query&titles=File:' + url_file + '&prop=imageinfo&iiprop=url&format=json'
    data=requests.get(url)
    return re.search(r'"url":"(.+?)"',data.text).group(1)

with open('text_uk')as f:
    F=f.read()
pattern = r'\{\{基礎情報.*?$(.*?)^\}\}'
template =re.findall(pattern,F,re.MULTILINE+re.DOTALL)
#print(template[0])
pattern = r'^\|(.+?)\s*=\s*(.+?)(?:(?=\n\|)|(?=\n$))'
result=dict(re.findall(pattern,template[0],re.MULTILINE+re.DOTALL))
print(get_url(result))


"""
{{基礎情報 国
hoge
hogu
}}
"""