#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Webdata:
	def __init__(self, name, hitnum, strnum):
		self.name = name
		self.hitnum = hitnum
		self.strnum = strnum
	def showinfo(self):
		print '%s(%d/%d)(%f)'%(self.name, self.hitnum, self.strnum, float(self.hitnum)/self.strnum)
	def simple(self):
		return (self.name,self.hitnum,self.strnum)