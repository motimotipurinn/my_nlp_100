import re

with open('text_uk')as f:
    F=f.read()
pattern = r'^.*\[\[Category:(.*?)(?:\|.*)?\]\].*$'
result = '\n'.join(re.findall(pattern, F, re.MULTILINE))
print(result)

"""
^ 文字列の先頭
. 改行以外の任意の1文字
* 直前のパターンを0回以上繰り返し
? 直前のパターンを0回または1回繰り返し
[] にもメタ文字となってるために\[,\]を使う必要がある

EXAMPLE
[[Category:イギリス連邦加盟国]]->イギリス連邦加盟国
"""