#!/bin/python3
# -*- coding: utf-8 -*-

from sys import argv, version_info

# Importation des dépendances internes
from core.icons import Icons

if(version_info.major < 3): # Vérification de l'éxecution du script avec Python3
	print("{}Le programme doit être lancer avec Python 3".format(Icons.warn))
	exit()

from core.entity import Entity
from core.map import Map

def arg(): # Fonction d'entrée des arguments
	def mapEntry():
		try:
			map = Map(str(argv[2]))

			return(map)

		except Exception:
			print("{}Aucun nom de map n'a été entrer".format(Icons.warn))

			return(False)

	def errMsg():
		print("{}Il y a pas de map sauvegardée portant ce nom".format(Icons.warn))
		print('{}Créer une nouvelle map avec "python main.py -n <mapName> <x> <y>"'.format(Icons.info))

		return(False)

	args = {
		"prefix": (
			(("-a", "--add"), "<mapName> \"[(x, y), ...]\""),
			(("-A", "--add-entity"), "<mapName> <type> <x> <y>"),
			(("-d", "--display"), "<mapName>"),
			(("-n", "--new"), "<mapName> <x> <y>"),
			(("-r", "--reset"), "<mapName>"),
			(("-s", "--start"), "<mapName>"),
			(("-h", "--help"), ""),
			(("-v", "--version"), "")
		),
		"descriptions": (
			"\tInsérer une ou plusieurs cellules",
			"Insérer une entité",
			"\t\tAfficher la map enregistrée",
			"\t\tCréer une nouvelle map",
			"\t\t\tRéinitialiser une map",
			"\t\t\tJouer une map\n",
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
		map = mapEntry()
		if(not map):
			return(False)

		if(map.loaded):
			try:
				map.addCells(eval(argv[3]))

			except Exception:
				print("{}Coordonnées manquantes ou incorrectes".format(Icons.warn))

				return(False)

		else:
			return(errMsg())

	elif(argv[1] in args["prefix"][1][0]):
		map			= mapEntry()
		entities	= Entity()
		if(not map):
			return(False)

		if(map.loaded):
			try:
				x = int(argv[4])
				y = int(argv[5])

			except Exception:
				print("{}Les coordonnées de position doivent être des entiers".format(Icons.warn))

				return(False)

			if(entities.loaded):
				if(argv[3] in entities.getEntitiesName()):
					map.addCells(entities.get(argv[3], (x, y)))
					map.display()

				else:
					print("{}Entitée non reconnue".format(Icons.warn))

			else:
				print("{}Le fichier d'entités est introuvables".format(Icons.warn))

				return(False)

		else:
			return(errMsg())

	elif(argv[1] in args["prefix"][2][0]):
		map = mapEntry()
		if(not map):
			return(False)

		if(map.loaded):
			map.display()

		else:
			print("{}Il y a pas de map sauvegardée portant ce nom".format(Icons.warn))
			print('{}Créer une nouvelle map avec "python main.py -n <mapName> <x> <y>"'.format(Icons.info))

			return(False)

	elif(argv[1] in args["prefix"][3][0]):
		map = mapEntry()
		if(not map):
			return(False)

		try:
			map.initMap(int(argv[3]), int(argv[4]))
			map.display()

		except Exception:
			print("{}Spécifier les dimension <x> et <y>".format(Icons.warn))

			return(False)

	elif(argv[1] in args["prefix"][4][0]):
		map = mapEntry()
		if(not map):
			return(False)

		if(map.loaded):
			map.reset()
			map.display()

		else:
			return(errMsg())

	elif(argv[1] in args["prefix"][5][0]):
		map = mapEntry()
		if(not map):
			return(False)

		if(map.loaded):
			map.start()

		else:
			return(errMsg())

	return(True)

def main(): # Fonction principale de l'execution du programme
	map = Map(str(input("Entrer un nom de map à charger: ")))

	if(not map.loaded):
		print("{}Il y a pas de map sauvegardée portant ce nom".format(Icons.warn))
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

		map.initMap(int(size["x"]), int(size["y"]))

	map.start()

	return(True)

if __name__ == "__main__":
	arg() if(len(argv) > 1) else main()
