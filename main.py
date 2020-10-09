#!/bin/python3
# -*- coding: utf-8 -*-

import json
from sys import argv
from os import system as shell
from platform import system
from random import getrandbits, randint
from time import sleep

def initMap(x, y):
	map = []
	for i in range(0, x):
		map.append([])
		for j in range(0, y):
			map[i].append(0)

	return map

def displayMap(map):
	for item in map:
		row = ""
		for value in item:
			row += "O " if(value) else ". "

		print(row)

	return True

def saveJSON(map):
	try:
		with open("data.json", 'w') as inFile:
			json.dump(map, inFile)

		return True

	except Exception:
		return False

def loadJSON():
	with open("data.json") as inFile:
		map = json.load(inFile)

	return map

def update(map):
	shell('clear' if(system() == "Linux") else 'cls')
	xmap = initMap(len(map), len(map[0]))

	for x in range(0, len(map)-1):
		for y in range(0, len(map[x])-1):
			xmap[x][y] = map[x][y]
			active = 0

			for i in range(-1, 2):
				for j in range(-1, 2):
					active += map[x+i][y+j] if((i != 0) or (j != 0)) else 0

			xmap[x][y] = 1 if((active == 3) or (map[x][y] and (active == 2))) else 0

	return xmap

def main():
	try:
		map = loadJSON()

	except Exception:
		print("[!] - Il y a pas de map sauvegardée")
		print("(i) - Création d'une nouvelle map ...")

		size = {
			'x': int(input("Hauteur <x> : ")),
			'y': int(input("Largeur <y> : "))
		}

		map = initMap(size["x"], size["y"])

	while(True):
		map = update(map)
		displayMap(map)
		saveJSON(map)
		sleep(.1)

	return True

if __name__ == "__main__":
	if(len(argv) > 1):
		if(argv[1] in ("-d", "--display")):
			try:
				map = loadJSON()
				displayMap(map)

			except Exception:
				print("[!] - Il y a pas de map sauvegardée")
				print('(i) - Créer une nouvelle map avec "python main.py -n <x> <y>"')

		elif(argv[1] in ("-n", "--new")):
			try:
				map = initMap(int(argv[2]), int(argv[3]))
				displayMap(map)
				saveJSON(map)

			except Exception:
				print("[!] - Spécifier les dimension <x> et <y>")

		elif(argv[1] in ("-a", "--add")):
			try:
				map = loadJSON()
				for glider in eval(argv[2]):
					map[int(glider[0])-1][int(glider[1])-1] = 1

				saveJSON(map)

			except Exception:
				print("[!] - Il y a pas de map sauvegardée")
				print('(i) - Créer une nouvelle map avec "python main.py -n <x> <y>"')

	else:
		main()
