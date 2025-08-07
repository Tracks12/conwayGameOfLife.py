#!/bin/python3
# -*- coding: utf-8 -*-

# Module de l'objet Entity
# ce module contient les fonctionnalités de chargement des entités

from concurrent.futures import ThreadPoolExecutor, as_completed
from os import listdir
from os.path import abspath, dirname

from core.loader import Loader

class Entity:
	def __init__(self):
		self.__path		= str(f"{abspath(dirname(__file__))}/../entities")
		self.__entities	= dict[str, str]({})
		self.loaded		= bool(self.__loadJSON())

	def __loadJSON(self) -> bool: # Chargement des entités depuis le dossier "entities"
		def computeEntity(entity: str) -> dict[str, str]:
			_ = int(20)

			with open(f"{self.__path}/{entity}.json", 'r') as outFile:
				return(Loader.json(outFile, [f"Loading {entity} ...{'':<{_}}", f"{entity} loaded !{'':<{_}}", f"{entity} loading Failed !{'':<{_}}"])[entity])

		try:
			print("Loading entities ...")
			__entities = [ e.split(".")[0] for e in listdir(self.__path) if "json" in e.split(".") ]

			with ThreadPoolExecutor(max_workers=len(__entities)) as executor:
				threads = { executor.submit(computeEntity, entity): entity for entity in __entities }

				for thread in as_completed(threads):
					entity = threads[thread]
					self.__entities[entity] = thread.result()

			print("Entities loaded !")
			return(True)

		except(Exception):
			return(False)

	def __build(self, coord: tuple[int]) -> dict[str, list[tuple[int]]]: # Build with relative position
		entities = dict[str, str](self.__entities)

		for name in entities:
			entities[name]	= str(entities[name].replace("x", str(coord[0])))
			entities[name]	= str(entities[name].replace("y", str(coord[1])))
			entities[name]	= eval(entities[name])

		return(entities)

	def getEntitiesName(self) -> list[str]:
		return([ str(e) for e in self.__entities ])

	def get(self, name: str, coord: tuple[int] = (5, 5)) -> list[tuple[int]]: # Récupération d'une entité
		return(self.__build(coord)[name])
