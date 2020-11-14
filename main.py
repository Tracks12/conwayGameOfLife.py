#!/bin/python3
# -*- coding: utf-8 -*-

from sys import argv, version_info

# Importation des dépendances internes
from core import Colors, Icons

if(version_info.major < 3): # Vérification de l'éxecution du script avec Python3
	print(f"{Icons.warn}Le programme doit être lancer avec Python 3")
	exit()

from core.entity import Entity
from core.map import Map

def arg(): # Fonction d'entrée des arguments
	def errMsg():
		print(f"{Icons.warn}Il y a pas de map sauvegardée portant ce nom")
		print(f'{Icons.info}Créer une nouvelle map avec "python main.py -n <mapName> <x> <y>"')

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
			print(f' {args["prefix"][i][0][0]}, {args["prefix"][i][0][1]} {args["prefix"][i][1]}\t{args["descriptions"][i]}')

	elif(argv[1] in args["prefix"][-1][0]):
		print(" conwayGameOfLife.py 2.1 - Florian Cardinal\n")

	if(
		not (argv[1] in args["prefix"][-2][0])
		and not (argv[1] in args["prefix"][-1][0])
	):
		try:
			map = Map(str(argv[2]))

		except Exception:
			print(f"{Icons.warn}Aucun nom de map n'a été entrer")

			return(False)

		if(argv[1] in args["prefix"][0][0]):
			if(map.loaded):
				try:
					map.addCells(eval(argv[3]))
					map.display()

				except Exception:
					print(f"{Icons.warn}Coordonnées manquantes ou incorrectes")

					return(False)

			else:
				return(errMsg())

		elif(argv[1] in args["prefix"][1][0]):
			if(map.loaded):
				entities = Entity()

				try:
					x = int(argv[4])
					y = int(argv[5])

				except Exception:
					print(f"{Icons.warn}Les coordonnées de position sont incorrectes")

					return(False)

				if(entities.loaded):
					if(argv[3] in entities.getEntitiesName()):
						map.addCells(entities.get(argv[3], (x, y)))
						map.display()

					else:
						print(f"{Icons.warn}Entitée non reconnue")

				else:
					print(f"{Icons.warn}Le fichier d'entités est introuvables")

					return(False)

			else:
				return(errMsg())

		elif(argv[1] in args["prefix"][2][0]):
			if(map.loaded):
				map.display()

			else:
				return(errMsg())

		elif(argv[1] in args["prefix"][3][0]):
			try:
				map.initMap(int(argv[3]), int(argv[4]))
				map.display()

			except Exception:
				print(f"{Icons.warn}Spécifier les dimension <x> et <y>")

				return(False)

		elif(argv[1] in args["prefix"][4][0]):
			if(map.loaded):
				map.reset()
				map.display()

			else:
				return(errMsg())

		elif(argv[1] in args["prefix"][5][0]):
			if(map.loaded):
				map.start()

			else:
				return(errMsg())

	return(True)

def main(): # Fonction principale de l'execution du programme
	map = Map(str(input(f"Entrer un nom de map à charger: {Colors.green}")))
	print(Colors.end)

	if(not map.loaded):
		print(f"{Icons.warn}Il y a pas de map sauvegardée portant ce nom")
		print(f"{Icons.info}Création d'une nouvelle map ...")

		while("size" not in locals()):
			try:
				size = {
					'x': int(input("Hauteur <x> (> 5): ")),
					'y': int(input("Largeur <y> (> 5): "))
				}

				if((size["x"] < 5) or (size["y"] < 5)):
					del size
					print(f"{Icons.warn}Les valeurs doivent être supérieur à 5")

			except Exception as e:
				print(f"{Icons.warn}Les valeurs doivent être des entiers supérieur à 5")

		map.initMap(int(size["x"]), int(size["y"]))

	map.start()

	return(True)

if __name__ == "__main__":
	arg() if(len(argv) > 1) else main()
