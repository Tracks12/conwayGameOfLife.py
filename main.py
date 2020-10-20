#!/bin/python3
# -*- coding: utf-8 -*-

import json
from sys import argv
from os import system as shell
from platform import system
from random import getrandbits, randint
from time import sleep

from core.color import Color
from core.icon import Icon

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

	def displayMap(self):
		for item in self.map:
			row = ""
			for value in item:
				row += "{}O{} ".format(Color.green, Color.end) if(value) else ". "

			print(row)

		return True

def arg(map):
	args = {
		"prefix": (
			(("-a", "--add"), "[(x, y), ...]"),
			(("-d", "--display"), ""),
			(("-n", "--new"), "<x> <y>"),
			(("-h", "--help"), ""),
			(("-v", "--version"), "")
		),
		"descriptions": (
			"Insérer une ou plusieur cellules",
			"\tAfficher la map enregistrer",
			"\tCréer une nouvelle map\n",
			"\t\tAffichage du menu d'aide",
			"\tAffichage de la version du programme\n"
		)
	}

	if(argv[1] in args["prefix"][-2][0]):
		print(" Le jeu de la vie de John Horton Conway")
		print(" Lancement: python main.py <arg>\n")
		print(" Arguments:")

		for i in range(0, len(args["prefix"])):
			print(" {}, {} {} \t{}".format(args["prefix"][i][0][0], args["prefix"][i][0][1], args["prefix"][i][1], args["descriptions"][i]))

	elif(argv[1] in args["prefix"][-1][0]):
		print(" conwayGameOfLife.py 2.0 - Florian Cardinal\n")

	elif(argv[1] in args["prefix"][0][0]):
		if(map.loadJSON()):
			for glider in eval(argv[2]):
				map.map[int(glider[0])-1][int(glider[1])-1] = 1

			map.saveJSON()

		else:
			print("{}Il y a pas de map sauvegardée".format(Icon.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icon.info))

	elif(argv[1] in args["prefix"][1][0]):
		if(map.loadJSON()):
			map.displayMap()

		else:
			print("{}Il y a pas de map sauvegardée".format(Icon.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icon.info))

	elif(argv[1] in args["prefix"][2][0]):
		try:
			map.initMap(int(argv[2]), int(argv[3]))
			map.displayMap()
			map.saveJSON()

		except Exception:
			print("{}Spécifier les dimension <x> et <y>".format(Icon.warn))

	return True

def main(map):
	if(not map.loadJSON()):
		print("{}Il y a pas de map sauvegardée".format(Icon.warn))
		print("{}Création d'une nouvelle map ...".format(Icon.info))

		while("size" not in locals()):
			try:
				size = {
					'x': int(input("Hauteur <x> : ")),
					'y': int(input("Largeur <y> : "))
				}

			except Exception:
				print("{}La valeur doit être un entier".format(Icon.warn))

		map.initMap(size["x"], size["y"])

	while(True):
		map.update()
		map.displayMap()
		map.saveJSON()
		sleep(.1)

	return True

if __name__ == "__main__":
	map = Map("data.json")

	if(len(argv) > 1):
		arg(map)

	else:
		main(map)
