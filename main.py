#!/bin/python3
# -*- coding: utf-8 -*-

import json, re
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

def arg(map):
	args = {
		"prefix": (
			(("-a", "--add"), "[(x, y), ...]"),
			(("-A", "--add-entity"), "<type> <x> <y>"),
			(("-d", "--display"), ""),
			(("-n", "--new"), "<x> <y>"),
			(("-h", "--help"), ""),
			(("-v", "--version"), "")
		),
		"descriptions": (
			"\tInsérer une ou plusieur cellules",
			"Insérer une entité",
			"\t\t\tAfficher la map enregistrer",
			"\t\tCréer une nouvelle map\n",
			"\t\t\tAffichage du menu d'aide",
			"\t\t\tAffichage de la version du programme\n"
		)
	}

	if(argv[1] in args["prefix"][-2][0]):
		print(" Le jeu de la vie de John Horton Conway")
		print(" Lancement: python main.py <arg>\n")
		print(" Arguments:")

		for i in range(0, len(args["prefix"])):
			print(" {}, {} {}\t{}".format(args["prefix"][i][0][0], args["prefix"][i][0][1], args["prefix"][i][1], args["descriptions"][i]))

	elif(argv[1] in args["prefix"][-1][0]):
		print(" conwayGameOfLife.py 2.0 - Florian Cardinal\n")

	elif(argv[1] in args["prefix"][0][0]):
		if(map.loadJSON()):
			try:
				for cell in eval(argv[2]):
					map.addCell(int(cell[0]), int(cell[1]))

				map.saveJSON()

			except Exception:
				print("{}Coordonnées manquantes".format(Icon.warn))

				return False

		else:
			print("{}Il y a pas de map sauvegardée".format(Icon.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icon.info))

	elif(argv[1] in args["prefix"][1][0]):
		if(map.loadJSON()):
			try:
				x = int(argv[3])
				y = int(argv[4])

			except Exception:
				print("{}Les coordonnées de position doivent être des entiers".format(Icon.warn))

				return False

			try:
				with open("entity.json", 'r') as outFile:
					entity = json.load(outFile)

					for item in entity:
						entity[item].replace("x", str(x))
						entity[item].replace("y", str(y))
						entity[item] = eval(entity[item])

			except Exception:
				print("{}Le fichier d'entités est introuvables".format(Icon.warn))

				return False

			if(argv[2] in entity):
				for cell in entity[argv[2]]:
					map.addCell(cell[0], cell[1])

				map.display()
				map.saveJSON()

		else:
			print("{}Il y a pas de map sauvegardée".format(Icon.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icon.info))

	elif(argv[1] in args["prefix"][2][0]):
		if(map.loadJSON()):
			map.display()

		else:
			print("{}Il y a pas de map sauvegardée".format(Icon.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icon.info))

	elif(argv[1] in args["prefix"][3][0]):
		try:
			map.initMap(int(argv[2]), int(argv[3]))
			map.display()
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
		map.display()
		map.saveJSON()
		sleep(.1)

	return True

if __name__ == "__main__":
	map = Map("data.json")

	if(len(argv) > 1):
		arg(map)

	else:
		main(map)
