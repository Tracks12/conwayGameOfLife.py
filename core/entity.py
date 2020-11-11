#!/bin/python3
# -*- coding: utf-8 -*-

# Module de l'objet Entity
# ce module contient les fonctionnalités de chargement des entités

import json

from core.loader import loadBar

class Entity:
	def __init__(self):
		self.__path		= str("entity.json")
		self.__entities	= {}
		self.loaded		= bool(self.__loadJSON())

	def __loadJSON(self): # Chargement des entités depuis un fichier
		try:
			with open(self.__path, 'r') as outFile:
				loadBar(["Entity loading ...", "Entities loaded !"])
				self.__entities = dict(json.load(outFile))

			return(True)

		except Exception:
			return(False)

	def __build(self, coord): # Build with relative position
		entities = dict(self.__entities)

		for name in entities:
			entities[name]	= str(entities[name].replace("x", str(coord[0])))
			entities[name]	= str(entities[name].replace("y", str(coord[1])))
			entities[name]	= eval(entities[name])

		return(entities)

	def getEntitiesName(self):
		names = []

		for name in self.__entities:
			names.append(str(name))

		return(names)

	def get(self, name, coord = (5, 5)): # Récupération d'une
		return self.__build(coord)[name]
