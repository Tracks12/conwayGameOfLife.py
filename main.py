#!/bin/python3
# -*- coding: utf-8 -*-

from random import getrandbits, randint
from time import sleep
import json, os

class c:
	r = "\033[31m"
	b = "\033[34m"
	g = "\033[32m"
	e = "\033[0m"

def initMap(x, y):
	map = []

	for i in range(0, x):
		map.append([])

		for j in range(0, y):
			map[i].append(0)

	return map

def displayMap(map):
	for item in map:
		row = ""
		for value in item:
			if(value): row += "{}{}{} ".format(c.g, value, c.e)
			else: row += "{} ".format(value)

		print(row)

def addGlider(map, xy, state):
	if(state):
		map[xy[0]-1][xy[1]] = 1
		map[xy[0]-1][xy[1]-1] = 1
		map[xy[0]-1][xy[1]-2] = 1

	else:
		map[xy[0]][xy[1]-1] = 1
		map[xy[0]-1][xy[1]-1] = 1
		map[xy[0]-2][xy[1]-1] = 1

	return [xy, state]

def update(map, g):
	sleep(1)
	try: os.system('clear')
	except: os.system('cls')

	for i in range(0, len(g)):
		if(g[i][1]):
			map[g[i][0][0]-1][g[i][0][1]] = 0
			map[g[i][0][0]-1][g[i][0][1]-2] = 0
			map[g[i][0][0]][g[i][0][1]-1] = 1
			map[g[i][0][0]-2][g[i][0][1]-1] = 1
			g[i][1] = False
		else:
			map[g[i][0][0]-1][g[i][0][1]] = 1
			map[g[i][0][0]-1][g[i][0][1]-2] = 1
			map[g[i][0][0]][g[i][0][1]-1] = 0
			map[g[i][0][0]-2][g[i][0][1]-1] = 0
			g[i][1] = True

	displayMap(map)

	with open("save.json", 'w') as outFile:
		json.dump(g, outFile, sort_keys=True, indent=2)

	update(map, g)

def main():
	gliders = []
	map = initMap(39, 39)

	for x in range(0, 80):
		gliders.append(addGlider(map, (randint(1, len(map)-1), randint(1, len(map[0])-1)), bool(getrandbits(1))))

	displayMap(map)
	update(map, gliders)

if __name__ == "__main__":
	main()
