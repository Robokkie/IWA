#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 正規表現で打たれた文字について，各ファイルから探索しヒットした数を表示する

#import os # osモジュールのインポート
import glob
import re # 正規表現検索
import codecs
import csv
from webdata import Webdata # 自作クラス（名前，検索後の個数）

# ----------- 関数群 -----------
# htmlテキストからbody内の本文のみを返す
def htmlbody(html):
	body = re.split(u'<body>|<BODY>', html)[-1]
	body = re.split(u'</body>|</BODY>', body)[0]
	return body

# htmlテキストをpythonのunicode型にデコードする
# 戻り値は変換されたテキストとエンコード方式のタプル
def conv_encoding(data):
	lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
			  'shift_jis', 'shift_jis_2004','shift_jisx0213',
			  'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
			  'iso2022_jp_ext','latin_1', 'ascii')
	encode = None
	for encoding in lookup:
		try:
			data = data.decode(encoding)
			encode = encoding
			break
		except:
			pass
	if isinstance(data, unicode):
		return data,encode
	else:
		raise LookupError


def count_word(words,re_word):
	i = 0
	number = 0
	while i >= 0:
		m = re_word.search(words, i)
		if m:	# マッチする組み合わせが文中に存在すれば
			i = m.start()+1		# 検索開始位置を見つけた位置から1ずらす（同じところでカウントしない）
			number += 1
		else:
			break
	return number
# -----------------------------



search_word = raw_input('Enter search word: ')
re_word = re.compile(search_word)

test_list = []

files = glob.glob('../web/*.html')

for file in files:
	f = open(file)
	html = f.read()
	bodytext, encode = conv_encoding(html)
	bodytext = htmlbody(bodytext)

	filename = file.rsplit('/',1)[-1] #右から1度だけスプリットして，ファイル名（一番右）だけを返す
	number = count_word(bodytext,re_word)
	strnum = count_word(bodytext,re.compile(" "))
	w = Webdata(filename, number, strnum)
	test_list.append(w)

	f.close()



csv_File = codecs.open("./pagelank.csv","w","utf_8")
writer = csv.writer(csv_File)
csv_header = ("html", search_word, "strnum", "score")
writer.writerow(csv_header)


#for i in test_list:
#	row = i.simple()
#	writer.writerow(row)

sorted_lists = sorted(test_list,key=lambda x: float(x.hitnum)/x.strnum, reverse=True)
for i in sorted_lists:
	i.showinfo()
	row = i.simple()
	writer.writerow(row)