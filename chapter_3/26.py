import re
def remove_markup(text):
    pattern= r'\'{2,5}'
    text=re.sub(pattern,'',text)
    return text

with open('text_uk')as f:
    F=f.read()
pattern = r'\{\{基礎情報.*?$(.*?)^\}\}'
template =re.findall(pattern,F,re.MULTILINE+re.DOTALL)
#print(template[0])
pattern = r'^\|(.+?)\s*=\s*(.+?)(?:(?=\n\|)|(?=\n$))'
result=dict(re.findall(pattern,template[0],re.MULTILINE+re.DOTALL))
result_rm={k: remove_markup(v) for k,v in result.items()}
for k,v in result_rm.items():
    print(k+': '+v)


"""
{{基礎情報 国
hoge
hogu
}}
"""