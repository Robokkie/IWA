#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Baseballer:
	def __init__(self, row):
		self.name = row[0]
		self.team = row[1]
		self.datas = row[2:]
	def showinfo(self):
		print 'team:%s,name:%s'%(self.team, self.name)