#!/bin/python3
# -*- coding: utf-8 -*-

import json
from sys import argv, version_info

# Importation des dépendances internes
from core.icons import Icons
from core.map import Map

def arg(map = Map()): # Fonction d'entrée des arguments
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
			"\tInsérer une ou plusieurs cellules",
			"Insérer une entité",
			"\t\t\tAfficher la map enregistrée",
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
		print(" conwayGameOfLife.py 2.1 - Florian Cardinal\n")

	elif(argv[1] in args["prefix"][0][0]):
		if(map.loadJSON()):
			try:
				map.addCells(eval(argv[2]))

			except Exception:
				print("{}Coordonnées manquantes".format(Icons.warn))

				return(False)

		else:
			print("{}Il y a pas de map sauvegardée".format(Icons.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icons.info))

	elif(argv[1] in args["prefix"][1][0]):
		if(map.loadJSON()):
			try:
				x = int(argv[3])
				y = int(argv[4])

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

			if(argv[2] in entity):
				map.addCells(entity[argv[2]])
				map.display()

		else:
			print("{}Il y a pas de map sauvegardée".format(Icons.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icons.info))

	elif(argv[1] in args["prefix"][2][0]):
		if(map.loadJSON()):
			map.display()

		else:
			print("{}Il y a pas de map sauvegardée".format(Icons.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <x> <y>"'.format(Icons.info))

	elif(argv[1] in args["prefix"][3][0]):
		try:
			map.initMap(int(argv[2]), int(argv[3]))
			map.display()

		except Exception:
			print("{}Spécifier les dimension <x> et <y>".format(Icons.warn))

	return(True)

def main(map = Map()): # Fonction principale de l'execution du programme
	if(not map.loadJSON()):
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
