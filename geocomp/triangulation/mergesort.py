#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import ceil

# Retorna True caso p esteja acima de q, ou entao caso tenham a mesma y coordenada e p tenha x coordenada menor
def Above(p, q):
	if(p.y > q.y):
		return True
	elif(p.y < q.y):
		return False
	else:
		if(p.x < q.x):
			return True
		elif(p.x > q.x):
			return False
		else:
			print("Are you sure? There are 2 points with the same coordinates."+str(p))
			return True


# Merge assumindo listas decrescentes
def Merge(l1, l2):
	len1 = len(l1['point'])
	len2 = len(l2['point'])
	res = {'point' : [], 'index' : []}
	i1 = 0
	i2 = 0
	for i in range(0, len1+len2):
		if(i1 < len1 and i2 < len2):
			if(Above(l1['point'][i1], l2['point'][i2])):
				res['point'].append(l1['point'][i1])
				res['index'].append(l1['index'][i1])
				i1 = i1+1
			else:
				res['point'].append(l2['point'][i2])
				res['index'].append(l2['index'][i2])
				i2 = i2+1
		elif(i1 < len1 and i2 == len2):
			res['point'].append(l1['point'][i1])
			res['index'].append(l1['index'][i1])
			i1 = i1+1
		else:
			res['point'].append(l2['point'][i2])
			res['index'].append(l2['index'][i2])
			i2 = i2+1
	return res


def RecMergeSort(v):
	if(len(v['point']) <= 1):
		return {'point' : v['point'], 'index' : v['index']}
	mid = len(v['point']) // 2
	inter1 = RecMergeSort({'point' : v['point'][mid:], 'index' : v['index'][mid:]})
	inter2 = RecMergeSort(({'point' : v['point'][:mid], 'index' : v['index'][:mid]}))
	return Merge(inter1,inter2)


def MergeSort(p, ind):
	res = RecMergeSort({'point' : p, 'index' : ind})
	return res['index']