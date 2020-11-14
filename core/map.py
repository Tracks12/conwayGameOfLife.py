#!/bin/python3
# -*- coding: utf-8 -*-

# Module de l'objet Map
# ce module contient les fonctionnalités de sauvegarde et de chargement de la map
# ainsi que la mise à jour de celle-ci

from json import dump
from os import system as shell
from platform import system
from time import sleep

from core import Colors, JSONloader

class Map:
	def __init__(self, mapName = "world"): # Fichier de chargement par défaut: "data.json"
		self.__path		= str(f"saves/{str(mapName)}.json")
		self.__dims		= tuple((0, 0))
		self.__cells	= int(self.__dims[0]*self.__dims[1])
		self.__map		= list([])
		self.mapName	= str(mapName)
		self.loaded		= bool(self.__loadJSON())
		self.stat		= bool(True)

	def __loadJSON(self): # Chargement depuis un fichier
		try:
			with open(self.__path, "r") as outFile:
				self.__map		= list(JSONloader(outFile, ["Loading map ...", "Map loaded !", "Map loading failed !"]))
				self.__dims		= tuple((len(self.__map), len(self.__map[0])))
				self.__cells	= int(self.__dims[1]*self.__dims[0])

			return(True)

		except Exception:
			return(False)

	def __saveJSON(self): # Sauvegarde dans un fichier
		try:
			with open(self.__path, "w") as inFile:
				dump(self.__map, inFile)

			return(True)

		except Exception:
			return(False)

	# Création d'une map sur un format pré-défini
	# Par défaut, on génère une map de 20x20 si les dimensions ne sont pas saisies
	def __makeMap(self, dims = (20, 20)):
		map = []
		for i in range(0, int(dims[0])):
			map.append([])
			for j in range(0, int(dims[1])):
				map[i].append(0)

		return(map)

	def __update(self): # Mise à jour de la map (autosave au passage)
		xmap = self.__makeMap(self.__dims)

		for x in range(0, self.__dims[0]-1):
			for y in range(0, self.__dims[1]-1):
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

	def display(self): # Affichage de la map avec/sans les statistiques
		shell('clear' if(system() == "Linux") else 'cls')

		if(bool(self.stat)): # Initialisation des statistiques
			active = 0

			for cells in self.__map:
				for cell in cells:
					active += cell

			stats = (
				f"Name       : {self.mapName}",
				f"Dimensions : {self.__dims[0]}x{self.__dims[1]}",
				f"Actives    : {Colors.green if(active < int(self.__cells/2)) else Colors.red}{active}{Colors.end}"
			)

		for i, line in enumerate(self.__map):
			row = ""
			for value in line:
				row += f"{Colors.green}O" if(value) else f"{Colors.cyan}."
				row += f"{Colors.end} "

			if(bool(self.stat) and (i < len(stats))): # Mise à jours des statistiques
				row += f" {stats[i]}"

			print(row)

		return(True)

	def initMap(self, x, y): # Initialisation de la map dans l'objet
		self.__map		= list(self.__makeMap((int(x), int(y))))
		self.__dims		= tuple((int(x), int(y)))
		self.__cells	= int(self.__dims[0]*self.__dims[1])

		return(self.__saveJSON())

	def reset(self): # Reset complet de toute la map
		for i in range(0, self.__dims[0]):
			for j in range(0, self.__dims[1]):
				self.__map[i][j] = 0

		self.__saveJSON()

	def start(self): # Lancement du jeu
		while(True):
			self.__update()
			self.display()
			sleep(.1)

		return(True)
