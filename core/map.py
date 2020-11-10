#!/bin/python3
# -*- coding: utf-8 -*-

# Module de l'objet Map
# ce module contient les fonctionnalités de sauvegarde et de chargement de la map
# ainsi que la mise à jour de celle-ci

import json
from os import system as shell
from platform import system
from time import sleep

from core.colors import Colors

class Map:
	# Fichier de chargement par défaut: "data.json"
	def __init__(self, path = "data"):
		self.__path	= "saves/{}.json".format(path)
		self.__map	= []
		self.loaded	= self.__loadJSON()

	def __loadJSON(self): # Chargement depuis un fichier
		try:
			self.__loadBar(["Loading map ...", "Map loaded !"])
			with open(self.__path) as outFile:
				self.__map = json.load(outFile)

			return(True)

		except Exception:
			return(False)

	def __saveJSON(self): # Sauvegarde dans un fichier
		try:
			with open(self.__path, 'w') as inFile:
				json.dump(self.__map, inFile)

			return(True)

		except Exception:
			return(False)

	def __loadBar(self, msg = ["", ""]): # Barre de charement
		arr = ['\\', '|', '/', '-']

		i = 0
		while(i < 10):
			print(" [{}{}{}] {}".format(Colors.yellow, arr[i % len(arr)], Colors.end, msg[0]), end = "\r")
			i += 1
			sleep(.05)

		print(" [{}*{}] {}".format(Colors.green, Colors.end, msg[1]))

	# Création d'une map sur un format pré-défini
	# Par défaut, on génère une map de 20x20 si les dimensions ne sont pas saisies
	def __makeMap(self, x = 20, y = 20):
		map = []
		for i in range(0, x):
			map.append([])
			for j in range(0, y):
				map[i].append(0)

		return map

	def __update(self): # Mise à jour de la map (autosave au passage)
		xmap = self.__makeMap(len(self.__map), len(self.__map[0]))

		for x in range(0, len(self.__map)-1):
			for y in range(0, len(self.__map[x])-1):
				active = 0

				for i in range(-1, 2):
					for j in range(-1, 2):
						active += self.__map[x+i][y+j] if((i != 0) or (j != 0)) else 0

				xmap[x][y] = 1 if((active == 3) or (self.__map[x][y] and (active == 2))) else 0

		self.__map = xmap
		self.__saveJSON()

	def addCells(self, cells): # Ajout de cellule(s) active(s)
		for cell in cells:
			self.__map[int(cell[0])-1][int(cell[1])-1] = 1

		return(self.__saveJSON())

	def display(self): # Affichage de la map
		shell('clear' if(system() == "Linux") else 'cls')

		for item in self.__map:
			row = ""
			for value in item:
				row += "{}O{}".format(Colors.green, Colors.end) if(value) else "{}.{}".format(Colors.cyan, Colors.end)
				row += " "

			print(row)

		return(True)

	def initMap(self, x, y): # Initialisation de la map dans l'objet
		self.__map = self.__makeMap(x, y)
		self.__saveJSON()

		return(True)

	def start(self): # Lancement du jeu
		while(True):
			self.__update()
			self.display()
			sleep(.1)

		return(True)
