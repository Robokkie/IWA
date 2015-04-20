#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 正規表現で打たれた文字について，各ファイルから探索しヒットした数を表示する

#import os # osモジュールのインポート
import codecs
import csv
from baseballer import Baseballer

# ----------- 関数群 -----------
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
# -----------------------------

def data_analize(players):
	max=[]
	min=[]
	for data in players[0].datas:
		max.append(float(data))
		min.append(float(data))
	for player in players:
		n=0
		for data in player.datas:
			if float(data) > max[n]:
				max[n]=data
			if float(data) < min[n]:
				min[n]=data
			n+=1
	return max, min

def recommender_player(tester,players,max_datas):
	player_return=[]
	for player in players:
		n=0
		diff=0
		for max_data in max_datas:
			x=float(float(tester.datas[n]) - float(player.datas[n]))/float(max_data)
			diff+=x*x
		player_return.append(Recommend_player(player.name,diff))
	return player_return


class Recommend_player:
	def __init__(self, name, score):
		self.name = name
		self.score = score
	def showinfo(self):
		print '%s(%f)'%(self.name, self.score)

csv_File = open('../csv/baseball.csv','r')
csv_rows = csv.reader(csv_File)

players=[]

for row in csv_rows:
	players.append(Baseballer(row))
	#print ','.join(row)
maxs, mins=data_analize(players)

n=0
for player in players:
	print n
	player.showinfo()
	n+=1

selecter=players[52]
recommend_list=recommender_player(selecter,players,maxs)

sorted_lists = sorted(recommend_list,key=lambda x: float(x.score))[0:4]
print selecter.name
print 'is similar to'
for i in sorted_lists:
	i.showinfo()

