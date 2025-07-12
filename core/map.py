#!/bin/python3
# -*- coding: utf-8 -*-

# Module de l'objet Map
# ce module contient les fonctionnalités de sauvegarde et de chargement de la map
# ainsi que la mise à jour de celle-ci

from json import dumps
from os import system as shell
from os.path import abspath, dirname
from platform import system
from zlib import compress

from core import SYSTEM, Icons

match(SYSTEM):
	case("Windows"):
		from keyboard import is_pressed, on_press
		from time import sleep

	case("Linux"):
		from select import select
		from sys import stdin
		import termios, tty

		def getch(timeout: float = .01) -> str | None:
			fd = stdin.fileno()
			old = termios.tcgetattr(fd)

			try:
				tty.setcbreak(fd)
				rlist, _, _ = select([fd], [], [], timeout)

				if(rlist):
					ch = stdin.read(1)
					return(ch)

			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old)

			return(None)

from core import B64, CMD_CLEAR, Colors
from core.loader import Loader

class Map:
	def __init__(self, mapName = "world"): # Fichier de chargement par défaut: "data.json"
		self.__path		= str(f"{dirname(abspath(__file__))}/../saves/{str(mapName)}.map")
		self.__dims		= tuple((0, 0))
		self.__cells	= int(self.__dims[0]*self.__dims[1])
		self.__map		= list([])
		self.__iter		= int(0)
		self.__sleep	= float(.03)
		self.mapName	= str(mapName)
		self.loaded		= bool(self.__loadJSON())
		self.helper		= bool(True)
		self.stats		= bool(True)

	def __loadJSON(self) -> bool: # Chargement depuis un fichier
		try:
			with open(self.__path, "rb") as outFile:
				self.__map		= list(Loader.map(outFile, ["Loading map ...", "Map loaded !   ", "Map loading failed !"]))
				self.__dims		= tuple((len(self.__map), len(self.__map[0])))
				self.__cells	= int(self.__dims[1]*self.__dims[0])

			return(True)

		except(Exception):
			return(False)

	def __saveJSON(self) -> bool: # Sauvegarde dans un fichier
		try:
			with open(self.__path, "wb") as inFile:
				inFile.write(compress(B64.encode(dumps(self.__map))))

			return(True)

		except(Exception):
			return(False)

	def __decreaseSpeed(self) -> None:
		self.__sleep *= 2

	def __increaseSpeed(self) -> None:
		if(self.__sleep > .001):
			self.__sleep /= 2

	def __label(self, text: str, color: Colors = "") -> None:
		_ = str(' '*int((self.__dims[1]+(self.__dims[1]-1))/2))[int((len(text)-1)/2)-(1 if(len(text)%2) else 0):-4]

		print("\x1b[A"*int(self.__dims[0]/2), end="\r")
		print(f"{_} [ {color}{text}{Colors.end} ] {_}{'' if(len(text)%2) else ' '}")
		print("\x1b[B"*int((self.__dims[0]/2)-1), end="\r")

	# Création d'une map sur un format pré-défini
	# Par défaut, on génère une map de 20x20 si les dimensions ne sont pas saisies
	def __makeMap(self, dims = (20, 20)) -> list[list[int]]:
		map = []
		for i in range(0, int(dims[0])):
			map.append([])
			for j in range(0, int(dims[1])):
				map[i].append(0)

		return(map)

	def __onKeyPress(self, keys: list[bool]) -> None:
		keys[0] = True

	def __pause(self) -> None:
		self.__label("PAUSED", Colors.yellow)
		input("Press enter to continue ...")
		shell(CMD_CLEAR)

	def __update(self): # Mise à jour de la map
		map = self.__makeMap(self.__dims)

		for x in range(0, self.__dims[0]-1):
			for y in range(0, self.__dims[1]-1):
				active = 0

				for i in range(-1, 2):
					for j in range(-1, 2):
						active += self.__map[x+i][y+j] if((i != 0) or (j != 0)) else 0

				map[x][y] = 1 if((active == 3) or (self.__map[x][y] and (active == 2))) else 0

		self.__map = map

	def addCells(self, cells) -> bool: # Ajout de cellule(s) active(s)
		for cell in cells:
			self.__map[int(cell[0])-1][int(cell[1])-1] = 1

		return(self.__saveJSON())

	def display(self) -> bool: # Affichage de la map avec/sans les statistiques
		if(bool(self.stats)): # Initialisation & Mise à jours des statistiques
			active = 0

			for cells in self.__map:
				for cell in cells:
					active += cell

			_ = int(12)
			stats = (
				f"{'Name':<{_}}: {self.mapName}{' '*2}",
				f"{'Dimensions':<{_}}: {self.__dims[0]}x{self.__dims[1]}",
				f"{'Iterations':<{_}}: {self.__iter}",
				f"{'Actives':<{_}}: {Colors.green if(active < (self.__cells/2)) else Colors.red}{active:<{5}}{Colors.end}",
				f"{'Speed':<{_}}: {Colors.green}{self.__sleep:.3f}{Colors.end} sec",
			)

		if(bool(self.helper)):
			_ = int(12)
			help = (
				f"{Colors.yellow}{'Space':<{_}}{Colors.end}: Pause/Resume",
				f"{Colors.yellow}{'Up/Down':<{_}}{Colors.end}: Speed up/Slow down",
				f"{Colors.red}{'Esc':<{_}}{Colors.end}: Exit",
			)

		for i, line in enumerate(self.__map):
			row = ""
			for value in line:
				row += f'{f"{Colors.green}O" if(value) else f"{Colors.cyan}."}{Colors.end} '

			if(bool(self.stats) and (i < len(stats))): # Affichage des statistiques
				row += f" {stats[i]}"

			if(bool(self.helper) and (self.__dims[0]-i-1 < len(help))): # Affichage de l'aide
				row += f" {help[::-1][self.__dims[0]-i-1]}"

			print(row)

		return(True)

	def initMap(self, x, y) -> bool: # Initialisation de la map dans l'objet
		self.__map		= list(self.__makeMap((int(x), int(y))))
		self.__dims		= tuple((int(x), int(y)))
		self.__cells	= int(self.__dims[0]*self.__dims[1])

		return(self.__saveJSON())

	def reset(self) -> bool: # Reset complet de toute la map
		for i in range(0, self.__dims[0]):
			for j in range(0, self.__dims[1]):
				self.__map[i][j] = 0

		return(self.__saveJSON())

	def start(self) -> bool: # Lancement du jeu
		if(SYSTEM == "Windows"):
			_keyPressed	= [ False ]
			_hook	= on_press(lambda e:self.__onKeyPress(_keyPressed))

		shell(CMD_CLEAR)

		try:
			while(True):
				self.__iter += 1

				print("\x1b[A"*self.__dims[0], end="\r")
				self.__update()
				self.display()

				if(SYSTEM == "Windows"):
					if(_keyPressed[0]):
						_keyPressed[0] = False

						if(is_pressed("space") or is_pressed("p")):
							self.__pause()

						if(is_pressed("esc") or is_pressed("q")):
							raise(KeyboardInterrupt)

						if(is_pressed("up") or is_pressed("u")):
							self.__increaseSpeed()

						if(is_pressed("down") or is_pressed("d")):
							self.__decreaseSpeed()

					sleep(self.__sleep)

				if(SYSTEM == "Linux"):
					key = getch(self.__sleep)

					if(key is not None):
						if(key in (" ", "p")):
							self.__pause()

						if(key in ("\x1b", "q")):
							raise(KeyboardInterrupt)

						if(key == "u"):
							self.__increaseSpeed()

						if(key == "d"):
							self.__decreaseSpeed()

		except(KeyboardInterrupt):
			self.__label(f"STOP", Colors.red)

			if(self.__saveJSON()):
				print(f"{Icons.succ}{self.mapName.capitalize()}{' saved !':<{self.__dims[1]-len(self.mapName)}}")

			return(True)
