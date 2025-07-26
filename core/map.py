#!/bin/python3
# -*- coding: utf-8 -*-

# Module de l'objet Map
# ce module contient les fonctionnalités de sauvegarde et de chargement de la map
# ainsi que la mise à jour de celle-ci

from concurrent.futures import ThreadPoolExecutor
from json import dumps
from os import system as shell
from os.path import abspath, dirname
from zlib import compress

from core import SYSTEM, Icons, SystemEnum

match(SYSTEM):
	case(SystemEnum.WINDOWS):
		from keyboard import is_pressed, on_press
		from time import sleep

	case(SystemEnum.LINUX):
		from select import select
		from sys import stdin
		from termios import tcgetattr, tcsetattr, TCSADRAIN
		from tty import setcbreak

		def getch(timeout: float = .01) -> str | None:
			fd = stdin.fileno()
			old = tcgetattr(fd)

			try:
				setcbreak(fd)
				rlist, _, _ = select([ fd ], [], [], timeout)

				if(rlist):
					ch = stdin.read(1)
					return(ch)

			finally:
				tcsetattr(fd, TCSADRAIN, old)

			return(None)

from core import B64, CMD_CLEAR, Colors
from core.loader import Loader

class Map:
	def __init__(self, mapName: str = "world"): # Fichier de chargement par défaut: "data.json"
		self.__path			= abspath(f"{dirname(__file__)}/../saves/{str(mapName)}.map")
		self.__dims			= tuple[int]((0, 0))
		self.__cells		= int(self.__dims[0]*self.__dims[1])
		self.__map			= list[list[int]]([])
		self.__iterations	= int(0)
		self.__sleep		= float(.0625)
		self.mapName		= str(mapName)
		self.loaded			= bool(self.__loadJSON())
		self.helper			= bool(False)
		self.stats			= bool(True)

	def __loadJSON(self) -> bool: # Chargement depuis un fichier
		try:
			with open(self.__path, "rb") as outFile:
				self.__map		= list[list[int]](Loader.map(outFile, ["Loading map ...", "Map loaded !   ", "Map loading failed !"]))
				self.__dims		= tuple[int]((len(self.__map), len(self.__map[0])))
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
		if(self.__sleep < 2):
			self.__sleep *= 2

	def __increaseSpeed(self) -> None:
		if(self.__sleep > .001):
			self.__sleep /= 2

	def __label(self, text: str, color: Colors = "") -> None:
		__dims = (self.__dims[0]/8, self.__dims[1]/3.9)

		_ = str(' '*int((__dims[1]+(__dims[1]-1))/2))[int((len(text)-1)/2)-(1 if(len(text)%2) else 0):-4]

		print("\x1b[A"*int(__dims[0]), end="\r")
		print(f"{_} [ {color}{text}{Colors.end} ] {_}{'' if(len(text)%2) else ' '}")
		print("\x1b[B"*int((__dims[0])-1), end="\r")

	# Création d'une map sur un format pré-défini
	# Par défaut, on génère une map de 20x20 si les dimensions ne sont pas saisies
	def __makeMap(self, dims = (20, 20)) -> list[list[int]]:
		map = list[list[int]]([[ 0 for _ in range(int(dims[1])) ] for _ in range(int(dims[0])) ])

		return(map)

	def __onKeyPress(self, keys: list[bool]) -> None:
		keys[0] = True

	def __pause(self) -> None:
		self.__label("PAUSED", Colors.yellow)
		input("Press enter to continue ...")
		shell(CMD_CLEAR)

	def __update(self) -> None: # Mise à jour de la map
		def compute_row(x: int) -> list[int]:
			row = list[int]([])

			for y in range(self.__dims[1]):
				xm1, xp1 = (x - 1) % self.__dims[0], (x + 1) % self.__dims[0]
				ym1, yp1 = (y - 1) % self.__dims[1], (y + 1) % self.__dims[1]

				active = sum([
					self.__map[xm1][ym1],
					self.__map[xm1][y],
					self.__map[xm1][yp1],
					self.__map[x][ym1],
					self.__map[x][yp1],
					self.__map[xp1][ym1],
					self.__map[xp1][y],
					self.__map[xp1][yp1]
				])

				row.append(1 if (active == 3 or (self.__map[x][y] and active == 2)) else 0)

			return(row)

		with ThreadPoolExecutor() as executor:
			self.__map = list(executor.map(compute_row, range(self.__dims[0])))

	def addCells(self, cells: list[tuple[int]]) -> bool: # Ajout de cellule(s) active(s)
		for cell in cells:
			self.__map[int(cell[0])-1][int(cell[1])-1] = 1

		return(self.__saveJSON())

	def display(self) -> bool: # Affichage de la map avec/sans les statistiques
		if(self.stats): # Initialisation & Mise à jours des statistiques
			active = sum([ sum(cells) for cells in self.__map ])

			_ = int(12)
			stats = (
				f"{'Name':<{_}}: {self.mapName:<{len(self.mapName)+1}}",
				f"{'Dimensions':<{_}}: {self.__dims[0]}x{self.__dims[1]}",
				f"{'Actives':<{_}}: {Colors.green if(active < (self.__cells/2)) else Colors.red}{active:<{len(str(active))+1}}{Colors.end}",
				f"{'Iterations':<{_}}: {self.__iterations:<{len(str(self.__iterations))+1}}",
				f"{'Speed':<{_}}: {Colors.green}{self.__sleep:.3f}{Colors.end} {'sec':<{4}}",
			)

		if(self.helper):
			_ = int(12)
			help = (
				f"{Colors.red}{'Esc (Q)':<{_}}{Colors.end}: {'Exit':<{5}}",
				f"{Colors.yellow}{'Space (P)':<{_}}{Colors.end}: {'Pause/Resume':<{13}}",
				f"{Colors.yellow}{'(U)p/(D)own':<{_}}{Colors.end}: {'Speed up/Slow down':<{19}}"
			)

		braille_map = dict[tuple[int, int], int]({
			(0, 0): 0, (0, 1): 3,
			(1, 0): 1, (1, 1): 4,
			(2, 0): 2, (2, 1): 5,
			(3, 0): 6, (3, 1): 7,
		})

		output_lines = list[str]([])
		for y in range(0, self.__dims[0], 4):
			lines = list[str]([])
			for x in range(0, self.__dims[1], 2):
				braille = int(0)
				for dy in range(4):
					for dx in range(2):
						xx, yy = int(x + dx), int(y + dy)

						if(
							(yy < self.__dims[0])
							and (xx < self.__dims[1])
							and self.__map[yy][xx]
						):
							bit = int(braille_map[(dy, dx)])
							braille |= (1 << bit)

				char = chr(0x2800 + braille)
				lines.append(f"{Colors.green if braille else Colors.cyan}{char}{Colors.end}")

			output_lines.append("".join(lines))

		for i in range(len(output_lines)):
			if(self.stats and (i < len(stats))): # Affichage des statistiques
				output_lines[i] += f" {stats[i]}"

			if(self.helper and (len(output_lines)-i-1 < len(help))): # Affichage de l'aide
				output_lines[i] += f" {help[len(output_lines)-i-1]}"

		print("\n".join(output_lines), flush=True)

		return(True)

	def initMap(self, x: int, y: int) -> bool: # Initialisation de la map dans l'objet
		self.__map		= list[list[int]](self.__makeMap((int(x), int(y))))
		self.__dims		= tuple[int]((int(x), int(y)))
		self.__cells	= int(self.__dims[0]*self.__dims[1])

		return(self.__saveJSON())

	def reset(self) -> bool: # Reset complet de toute la map
		for i in range(self.__dims[0]):
			for j in range(self.__dims[1]):
				self.__map[i][j] = 0

		return(self.__saveJSON())

	def start(self) -> bool: # Lancement du jeu
		self.helper = True
		shell(CMD_CLEAR)

		if(SYSTEM == SystemEnum.WINDOWS):
			_keyPressed	= [ False ]
			_hook		= on_press(lambda _:self.__onKeyPress(_keyPressed))

		try:
			while(True):
				self.__iterations += 1

				print("\x1b[A"*self.__dims[0], end="\r")
				self.__update()
				self.display()

				if(SYSTEM == SystemEnum.WINDOWS):
					if(_keyPressed[0]):
						_keyPressed[0] = False

						if(is_pressed("space") or is_pressed("p")):
							self.__pause()

						if(is_pressed("esc") or is_pressed("q")):
							_hook()
							raise(KeyboardInterrupt)

						if(is_pressed("up") or is_pressed("u")):
							self.__increaseSpeed()

						if(is_pressed("down") or is_pressed("d")):
							self.__decreaseSpeed()

					sleep(self.__sleep)

				if(SYSTEM == SystemEnum.LINUX):
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
			self.__label(f"STOPPED", Colors.red)

			if(self.__saveJSON()):
				print(f"{Icons.succ}{self.mapName.capitalize()}{' saved !':<{self.__dims[1]-len(self.mapName)}}")

		return(True)
