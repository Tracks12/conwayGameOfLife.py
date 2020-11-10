#!/bin/python3
# -*- coding: utf-8 -*-

import json
from sys import argv, version_info

# Importation des dépendances internes
from core.icons import Icons

if(version_info.major < 3): # Vérification de l'éxecution du script avec Python3
	print("{}Le programme doit être lancer avec Python 3".format(Icons.warn))
	exit()

from core.map import Map

def arg(): # Fonction d'entrée des arguments
	def mapExist():
		try:
			map = Map(str(argv[2]))

			return(map)

		except Exception:
			print("{}Aucun nom de map n'a été entrer".format(Icons.warn))

			return(False)

	args = {
		"prefix": (
			(("-a", "--add"), "<mapName> \"[(x, y), ...]\""),
			(("-A", "--add-entity"), "<mapName> <type> <x> <y>"),
			(("-d", "--display"), "<mapName>"),
			(("-n", "--new"), "<mapName> <x> <y>"),
			(("-h", "--help"), ""),
			(("-v", "--version"), "")
		),
		"descriptions": (
			"\tInsérer une ou plusieurs cellules",
			"Insérer une entité",
			"\t\tAfficher la map enregistrée",
			"\t\tCréer une nouvelle map\n",
			"\t\t\t\tAffichage du menu d'aide",
			"\t\t\t\tAffichage de la version du programme\n"
		)
	}

	if(argv[1] in args["prefix"][-2][0]):
		print(" Le jeu de la vie de John Horton Conway")
		print(" Lancement: python main.py <arg>\n")
		print(" Arguments:")

		for i in range(0, len(args["prefix"])):
			print(" {}, {} {}\t{}".format(args["prefix"][i][0][0], args["prefix"][i][0][1], args["prefix"][i][1], args["descriptions"][i]))

	elif(argv[1] in args["prefix"][-1][0]):
		print(" conwayGameOfLife.py 2.1 - Florian Cardinal\n")

	elif(argv[1] in args["prefix"][0][0]):
		map = mapExist()
		if(not map):
			return(False)

		if(map.loaded):
			try:
				map.addCells(eval(argv[3]))

			except Exception:
				print("{}Coordonnées manquantes ou incorrectes".format(Icons.warn))

				return(False)

		else:
			print("{}Il y a pas de map sauvegardée".format(Icons.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icons.info))

			return(False)

	elif(argv[1] in args["prefix"][1][0]):
		map = mapExist()
		if(not map):
			return(False)

		if(map.loaded):
			try:
				x = int(argv[4])
				y = int(argv[5])

			except Exception:
				print("{}Les coordonnées de position doivent être des entiers".format(Icons.warn))

				return(False)

			try:
				with open("entity.json", 'r') as outFile:
					entity = json.load(outFile)

					for item in entity:
						entity[item].replace("x", str(x))
						entity[item].replace("y", str(y))
						entity[item] = eval(entity[item])

			except Exception:
				print("{}Le fichier d'entités est introuvables".format(Icons.warn))

				return(False)

			if(argv[3] in entity):
				map.addCells(entity[argv[3]])
				map.display()

		else:
			print("{}Il y a pas de map sauvegardée".format(Icons.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icons.info))

			return(False)

	elif(argv[1] in args["prefix"][2][0]):
		map = mapExist()
		if(not map):
			return(False)

		if(map.loaded):
			map.display()

		else:
			print("{}Il y a pas de map sauvegardée".format(Icons.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icons.info))

			return(False)

	elif(argv[1] in args["prefix"][3][0]):
		map = mapExist()
		if(not map):
			return(False)

		try:
			map.initMap(int(argv[3]), int(argv[4]))
			map.display()

		except Exception:
			print("{}Spécifier les dimension <x> et <y>".format(Icons.warn))

			return(False)

	return(True)

def main(): # Fonction principale de l'execution du programme
	map = Map(str(input("Enter map name to load: ")))

	if(not map.loaded):
		print("{}Il y a pas de map sauvegardée".format(Icons.warn))
		print("{}Création d'une nouvelle map ...".format(Icons.info))

		while("size" not in locals()):
			try:
				size = {
					'x': int(input("Hauteur <x> (> 5): ")),
					'y': int(input("Largeur <y> (> 5): "))
				}

				if((size["x"] < 5) or (size["y"] < 5)):
					del size

			except Exception as e:
				print("{}La valeur doit être un entier et supérieur à 5".format(Icons.warn))

		map.initMap(size["x"], size["y"])

	map.start()

	return(True)

if __name__ == "__main__":
	arg() if(len(argv) > 1) else main()
