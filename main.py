#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import system as shell
from sys import argv, version_info

# Importation des dépendances internes
from core import CMD_CLEAR, Colors, Icons

if(version_info.major < 3): # Vérification de l'éxecution du script avec Python3
	print("{}The program must be launched with Python 3".format(Icons.warn))
	exit()

from core.entity import Entity
from core.map import Map

def arg() -> bool: # Fonction d'entrée des arguments
	def errMsg() -> bool:
		print(f"{Icons.warn}There is no saved map with this name.")
		print(f'{Icons.info}Create a new map with "python main.py -n <mapName> <x> <y>"')
		return(False)

	args = {
		"prefix": (
			(("-a", "--add"), '<mapName> "[(x, y), ...]"'),
			(("-A", "--add-entity"), "<mapName> <type> <x> <y>"),
			(("-d", "--display"), "<mapName>"),
			(("-n", "--new"), "<mapName> <x> <y>"),
			(("-r", "--reset"), "<mapName>"),
			(("-s", "--start"), "<mapName>"),
			(("-h", "--help"), ""),
			(("-v", "--version"), "")
		),
		"descriptions": (
			"Insert one or more cells",
			"Insert an entity",
			"Display the saved map",
			"Create a new map",
			"Reset a map",
			"Play a map\n",
			"Display the help menu",
			"Display the program version\n"
		)
	}

	if(argv[1] in args["prefix"][-2][0]):
		print(" The Game of Life by John Horton Conway")
		print(" Launch: python main.py <arg>\n")
		print(" Arguments:")

		for i in range(len(args["prefix"])):
			_p = f'{args["prefix"][i][0][0]}, {args["prefix"][i][0][1]} {args["prefix"][i][1]}'
			print(f' {_p:<{44}}{args["descriptions"][i]}')

	elif(argv[1] in args["prefix"][-1][0]):
		print(" conwayGameOfLife.py 2.3 - Florian Cardinal\n")

	if(
		not (argv[1] in args["prefix"][-2][0])
		and not (argv[1] in args["prefix"][-1][0])
	):
		try:
			map = Map(str(argv[2]))

		except(Exception):
			print(f"{Icons.warn}No map name has been entered")
			return(False)

		if(argv[1] in args["prefix"][0][0]):
			if(map.loaded):
				try:
					map.addCells(eval(argv[3]))
					shell(CMD_CLEAR)
					map.display()

				except(Exception):
					print(f"{Icons.warn}Missing or incorrect contact information")
					return(False)

			else:
				return(errMsg())

		elif(argv[1] in args["prefix"][1][0]):
			if(map.loaded):
				entities = Entity()

				try:
					x = int(argv[4])
					y = int(argv[5])

				except(Exception):
					print(f"{Icons.warn}The position coordinates are incorrect")
					return(False)

				if(entities.loaded):
					if(argv[3] in entities.getEntitiesName()):
						map.addCells(entities.get(argv[3], (x, y)))
						shell(CMD_CLEAR)
						map.display()

					else:
						print(f"{Icons.warn}Unrecognized entity")

				else:
					print(f"{Icons.warn}The entity file could not be found")
					return(False)

			else:
				return(errMsg())

		elif(argv[1] in args["prefix"][2][0]):
			if(map.loaded):
				shell(CMD_CLEAR)
				map.display()

			else:
				return(errMsg())

		elif(argv[1] in args["prefix"][3][0]):
			try:
				map.initMap(int(argv[3]), int(argv[4]))
				shell(CMD_CLEAR)
				map.display()

			except(Exception):
				print(f"{Icons.warn}Specify the <x> and <y> dimensions")
				return(False)

		elif(argv[1] in args["prefix"][4][0]):
			if(map.loaded):
				map.reset()
				shell(CMD_CLEAR)
				map.display()

			else:
				return(errMsg())

		elif(argv[1] in args["prefix"][5][0]):
			if(map.loaded):
				map.start()

			else:
				return(errMsg())

	return(True)

def main() -> bool: # Fonction principale de l'execution du programme
	map = Map(str(input(f"Enter a map name to load: {Colors.green}")))
	print(Colors.end)

	if(not map.loaded):
		print(f"{Icons.warn}There is no saved map with this name")
		print(f"{Icons.info}Creating a new map ...")

		while("size" not in locals()):
			try:
				size = dict[str, int]({
					'x': int(input("Height <x> (> 5): ")),
					'y': int(input("Width <y> (> 5): "))
				})

				if((size["x"] < 5) or (size["y"] < 5)):
					del(size)
					print(f"{Icons.warn}Values must be greater than 5")

			except(Exception):
				print(f"{Icons.warn}Values must be integers greater than 5")

		map.initMap(int(size["x"]), int(size["y"]))

	map.start()

	return(True)

if(__name__ == "__main__"):
	arg() if(len(argv) > 1) else main()
