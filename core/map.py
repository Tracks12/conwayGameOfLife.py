#!/bin/python3
# -*- coding: utf-8 -*-

# Module de l'objet Map
# ce module contient les fonctionnalités de sauvegarde et de chargement de la map
# ainsi que la mise à jour de celle-ci

import json
from os import system as shell
from platform import system

from core.colors import Colors

class Map:
	# Fichier de chargement par défaut: "data.json"
	def __init__(self, path = "data.json"):
		self.path = path
		self.map = []

	# Création d'une map sur un format pré-défini
	# Par défaut, on génère une map de 20x20 si les dimensions ne sont pas saisies
	def __makeMap(self, x = 20, y = 20):
		map = []
		for i in range(0, x):
			map.append([])
			for j in range(0, y):
				map[i].append(0)

		return map

	def saveJSON(self): # Sauvegarde dans un fichier
		try:
			with open(self.path, 'w') as inFile:
				json.dump(self.map, inFile)

			return(True)

		except Exception:
			return(False)

	def loadJSON(self): # Chargement depuis un fichier
		try:
			with open(self.path) as outFile:
				self.map = json.load(outFile)

			return(True)

		except Exception:
			return(False)

	def initMap(self, x, y): # Initialisation de la map dans l'objet
		self.map = self.__makeMap(x, y)

		return(True)

	def addCell(self, x, y): # Ajout de cellule(s) active(s)
		self.map[x-1][y-1] = 1

		return(True)

	def update(self): # Mise à jour de la map
		shell('clear' if(system() == "Linux") else 'cls')
		xmap = self.__makeMap(len(self.map), len(self.map[0]))

		for x in range(0, len(self.map)-1):
			for y in range(0, len(self.map[x])-1):
				active = 0

				for i in range(-1, 2):
					for j in range(-1, 2):
						active += self.map[x+i][y+j] if((i != 0) or (j != 0)) else 0

				xmap[x][y] = 1 if((active == 3) or (self.map[x][y] and (active == 2))) else 0

		self.map = xmap

		return(True)

	def display(self): # Affichage de la map
		for item in self.map:
			row = ""
			for value in item:
				row += "{}O{} ".format(Colors.green, Colors.end) if(value) else ". "

			print(row)

		return(True)
