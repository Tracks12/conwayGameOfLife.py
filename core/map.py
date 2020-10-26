#!/bin/python3
# -*- coding: utf-8 -*-

import json
from os import system as shell
from platform import system

from core.color import Color

class Map:
	def __init__(self, path):
		self.path = path
		self.map = []

	def saveJSON(self):
		try:
			with open("data.json", 'w') as inFile:
				json.dump(self.map, inFile)

			return True

		except Exception:
			return False

	def loadJSON(self):
		try:
			with open(self.path) as outFile:
				self.map = json.load(outFile)

			return True

		except Exception:
			return False

	def makeMap(self, x, y):
		map = []
		for i in range(0, x):
			map.append([])
			for j in range(0, y):
				map[i].append(0)

		return map

	def initMap(self, x, y):
		self.map = self.makeMap(x, y)

		return True

	def addCell(self, x, y):
		self.map[x-1][y-1] = 1

		return True

	def update(self):
		shell('clear' if(system() == "Linux") else 'cls')
		xmap = self.makeMap(len(self.map), len(self.map[0]))

		for x in range(0, len(self.map)-1):
			for y in range(0, len(self.map[x])-1):
				active = 0

				for i in range(-1, 2):
					for j in range(-1, 2):
						active += self.map[x+i][y+j] if((i != 0) or (j != 0)) else 0

				xmap[x][y] = 1 if((active == 3) or (self.map[x][y] and (active == 2))) else 0

		self.map = xmap

		return True

	def display(self):
		for item in self.map:
			row = ""
			for value in item:
				row += "{}O{} ".format(Color.green, Color.end) if(value) else ". "

			print(row)

		return True
