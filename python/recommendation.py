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
				max[n]=float(data)
			if float(data) < min[n]:
				min[n]=float(data)
			n+=1
	return max, min


def players_simlarity(player1,player2,max_datas):
	player1.showinfo()
	player2.showinfo()
	diff=0
	n=0
	for max_data in max_datas:
			x=float(float(player1.datas[n]) - float(player2.datas[n]))/float(max_data)
			diff+=x*x
			n+=1
			print diff
	print diff

def recommender_player(tester,players,max_datas):
	similar_players=[]
	id=0
	for player in players:
		n=0
		diff=0
		for max_data in max_datas:
			x=float(float(tester.datas[n]) - float(player.datas[n]))/float(max_data)
			diff+=x*x
			n+=1
		similar_players.append(similar_player_score(id,player.name,diff))
		id+=1

	return similar_players




class similar_player_score:
	def __init__(self, id, name, score):
		self.id = id
		self.name = name
		self.score = score
	def showinfo(self):
		print '%5d:%10s(%3.10f)'%(self.id, self.name, self.score)

csv_File = open('../csv/baseball.csv','r')
csv_rows = csv.reader(csv_File)

players=[]

for row in csv_rows:
	players.append(Baseballer(row))
	#print ','.join(row)
maxs, mins=data_analize(players)

#n=0
#for player in players:
#print n
#player.showinfo()
#n+=1

			
selecter=players[22]
recommend_list=recommender_player(selecter,players,maxs)


sorted_lists = sorted(recommend_list,key=lambda x: float(x.score))[0:4]
print selecter.name
print 'is similar to'
for i in sorted_lists:
	i.showinfo()

