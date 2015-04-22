#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 正規表現で打たれた文字について，各ファイルから探索しヒットした数を表示する

#import os # osモジュールのインポート
import codecs
import csv
from baseballer import Baseballer

# ----------- 関数群 -----------

# すべてのデータについて最大最小を調べる
def data_analyze(players):
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

# 二人の人物がどれだけ似ているかを返す（0に近いほど似ている）
def players_simlarity(player1,player2,max_datas):
	diff=0
	n=0
	for max_data in max_datas:
			x=float(float(player1.datas[n]) - float(player2.datas[n]))/float(max_data)
			diff+=x*x
			n+=1
	return diff

# playersの各選手について，id,名前,testerとの類似度のクラスを作り，リストで返す．
def similarity_analysis(tester,players,max_datas):
	similar_players=[]
	id=0
	for player in players:
		n=0
		diff=players_simlarity(tester, player, max_datas)
		similar_players.append(similarity_info(id,player.name,diff))
		id+=1
	return similar_players

# -----------------------------


# IDと名前，類似度（0に近いほどよい）を格納するクラス
class similarity_info:
	def __init__(self, id, name, score):
		self.id = id
		self.name = name
		self.score = score
	def showinfo(self):
		print 'id:{0:3d}, score({2:1.7f}) {1:20s} '.format(self.id, self.name, self.score)


# -- main -- #
csv_File = open('../csv/baseball.csv','r')
csv_rows = csv.reader(csv_File)

players=[]

for row in csv_rows:
	players.append(Baseballer(row))
	#print ','.join(row)

# 各データの最大最小をタプルで返す（最小は使ってない）
maxs, mins=data_analyze(players)

n=0
for player in players:
	print 'id:{0:1d}'.format(n)
	player.showinfo()
	n+=1

id = int(raw_input('Enter id: '))
selecter=players[id]

recommend_list=similarity_analysis(selecter,players,maxs)

# 類似度順に並べ，10番目までを表示
sorted_lists = sorted(recommend_list,key=lambda x: float(x.score))[0:10]
print selecter.name
print 'is similar to'
for i in sorted_lists:
	i.showinfo()

