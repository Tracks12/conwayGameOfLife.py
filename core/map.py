#!/bin/python3
# -*- coding: utf-8 -*-

# Module de l'objet Map
# ce module contient les fonctionnalités de sauvegarde et de chargement de la map
# ainsi que la mise à jour de celle-ci

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from json import dumps
from math import prod
from os import system as shell
from os.path import abspath, dirname
from random import choice, randrange
from time import time
from zlib import compress

from core import CMD_CLEAR, SYSTEM, B64, Border, Colors, Icons, SystemEnum
from core.entity import Entity
from core.loader import Loader

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

class Map:
	def __init__(self, mapName: str = "world"): # Fichier de chargement par défaut: "data.json"
		self.__createdAt	= float(time())
		self.__lastUpdate	= float(time())
		self.__entities		= None
		self.__path			= abspath(f"{dirname(__file__)}/../saves/{str(mapName)}.map")
		self.__dims			= tuple[int]((0, 0))
		self.__cells		= int(prod(self.__dims))
		self.__map			= list[list[int]]([])
		self.__mapFrame		= Border.SMOOTH
		self.__iterations	= int(0)
		self.__sleep		= float(.0625)
		self.mapName		= str(mapName)
		self.loaded			= bool(self.__loadJSON())
		self.helper			= bool(False)
		self.stats			= bool(True)

	def __loadJSON(self) -> bool: # Chargement depuis un fichier
		try:
			with open(self.__path, "rb") as outFile:
				__data = Loader.map(outFile, ["Loading map ...", "Map loaded !   ", "Map loading failed !"])

				self.__createdAt	= float(__data["createdAt"])
				self.__lastUpdate	= float(__data["lastUpdate"])
				self.__iterations	= int(__data["iterations"])
				self.__map			= list[list[int]](__data["map"])
				self.__dims			= tuple[int]((len(self.__map), len(self.__map[0])))
				self.__cells		= int(prod(self.__dims))

			return(True)

		except(Exception):
			return(False)

	def __saveJSON(self) -> bool: # Sauvegarde dans un fichier
		try:
			self.__lastUpdate = time()

			with open(self.__path, "wb") as inFile:
				inFile.write(compress(B64.encode(dumps({
					"createdAt": self.__createdAt,
					"lastUpdate": self.__lastUpdate,
					"iterations": self.__iterations,
					"map": self.__map
				}))))

			return(True)

		except(Exception):
			return(False)

	def __controlsWindows(self, _keyPressed: list[bool] = [ False ], _hook = None) -> None:
		if(_keyPressed[0]):
			_keyPressed[0] = False

			if(is_pressed("space") or is_pressed("p")):
				self.__pause()

			if(is_pressed("esc") or is_pressed("q")):
				raise(KeyboardInterrupt)

			if(is_pressed("+")):
				self.__increaseSpeed()

			if(is_pressed("-")):
				self.__decreaseSpeed()

			if(is_pressed("r")):
				self.reset()

			if(is_pressed("a")):
				self.__addRandomEntity()

		sleep(self.__sleep)

	def __controlsLinux(self) -> None:
		key = getch(self.__sleep)

		match(key):
			case(" " | "p"): self.__pause()
			case("\x1b" | "q"): raise(KeyboardInterrupt)
			case("+"): self.__increaseSpeed()
			case("-"): self.__decreaseSpeed()
			case("r"): self.reset()
			case("a"): self.__addRandomEntity()

	def __decreaseSpeed(self) -> None:
		if(self.__sleep < 2):
			self.__sleep *= 2

	def __increaseSpeed(self) -> None:
		if(self.__sleep > .001):
			self.__sleep /= 2

	def __addRandomEntity(self) -> None:
		if(self.__entities.loaded):
			name		= choice(self.__entities.getEntitiesName())
			position	= (randrange(self.__dims[0]), randrange(self.__dims[1]))
			entity		= self.__entities.get(name, position)

			try:
				self.addCells(entity)
				print(f"{Icons.succ}Entity '{name}' added at {position} !{'':<{self.__dims[1]-len(name)-len(str(position))}}")

			except(IndexError):
				pass

	def __label(self, text: str, color: Colors = "") -> None:
		__dims	= tuple[float]((self.__dims[0]/8, self.__dims[1]/2))
		_		= str(" "*int(__dims[1]/2))[int((len(text)+2)/2):-1]

		print("\x1b[A"*int(__dims[0]+2), end="\r")
		print(f"{self.__mapFrame[5]}{_}[ {color}{text}{Colors.end} ]{_[:-1]}")
		print("\x1b[B"*int(__dims[0]+1), end="\r")

	# Création d'une map sur un format pré-défini
	# Par défaut, on génère une map de 20x20 si les dimensions ne sont pas saisies
	def __makeMap(self, dims = (20, 20)) -> list[list[int]]:
		map = list[list[int]]([[ 0 for _ in range(int(dims[1])) ] for _ in range(int(dims[0])) ])

		return(map)

	def __onKeyPress(self, keys: list[bool]) -> None:
		keys[0] = True

	def __pause(self) -> None:
		self.__label("PAUSED", Colors.yellow)
		input(f"{'Press enter to continue ...':<{int(self.__dims[1]/2)}}")
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

				# RULES = [
				# 	1 if(active == 3 or (self.__map[x][y] and active == 2)) else 0,
				# 	1 if(active == 2 or (active == 1)) else 0,
				# 	1 if(not active < 4 or (not self.__map[x][y] and active > 2)) else 0
				# ]
				# row.append(RULES[2])

				row.append(1 if(active == 3 or (self.__map[x][y] and active == 2)) else 0)

			return(row)

		# self.__map = list([ compute_row(x) for x in range(self.__dims[0]) ])

		with ThreadPoolExecutor(max_workers=self.__dims[0]) as executor:
			self.__map = list(executor.map(compute_row, range(self.__dims[0])))

	def addCells(self, cells: list[tuple[int]]) -> bool: # Ajout de cellule(s) active(s)
		for cell in cells:
			self.__map[int(cell[0])-1][int(cell[1])-1] = 1

		return(self.__saveJSON())

	def display(self) -> bool: # Affichage de la map avec/sans les statistiques
		_, __ = int(12), int(20)

		if(self.stats): # Initialisation & Mise à jours des statistiques
			createdAt = datetime.fromtimestamp(self.__createdAt).strftime("%Y-%m-%d %H:%M")
			lastUpdate = datetime.fromtimestamp(self.__lastUpdate).strftime("%Y-%m-%d %H:%M")
			active = sum([ sum(cells) for cells in self.__map ])

			stats = (
				f"{'Created at':<{_}}: {createdAt:<{__}}",
				f"{'Last Update':<{_}}: {lastUpdate:<{__}}",
				f"{'Iterations':<{_}}: {self.__iterations:<{__}}",
				f"{'Speed':<{_}}: {Colors.green}{self.__sleep*1000:<{5}.0f}{Colors.end}{'ms':<{__-5}}",
				f"{'Actives':<{_}}: {Colors.green if(active < (self.__cells/1.5)) else Colors.red}{active:<{__}}{Colors.end}",
				f"{'Filled':<{_}}: {Colors.green if(active < (self.__cells/1.5)) else Colors.red}{round((active/self.__cells)*100, 2):<{7}.2f}{Colors.end}{'%':<{__-7}}",
			)

		if(self.helper):
			help = (
				f"{Colors.red}{'Esc (Q)':<{_}}{Colors.end}: {'Exit':<{__}}",
				f"{Colors.yellow}{'R':<{_}}{Colors.end}: {'Reset':<{__}}",
				f"{Colors.yellow}{'A':<{_}}{Colors.end}: {'Add random entity':<{__}}",
				f"{Colors.yellow}{'Space (P)':<{_}}{Colors.end}: {'Pause/Resume':<{__}}",
				f"{Colors.yellow}{'+/-':<{_}}{Colors.end}: {'Speed up/Slow down':<{__}}",
			)

		braille_map = dict[tuple[int, int], int]({
			(0, 0): 0, (0, 1): 3,
			(1, 0): 1, (1, 1): 4,
			(2, 0): 2, (2, 1): 5,
			(3, 0): 6, (3, 1): 7,
		})

		output_lines = [ "".join([
			self.__mapFrame[0], self.__mapFrame[7],
			Colors.purple, self.mapName.capitalize(), Colors.end,
			self.__mapFrame[6], self.__mapFrame[4]*(len([ n for n in range(0, self.__dims[1], 2) ])-len(self.mapName)-2), self.__mapFrame[1],
		])]

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
				lines.append(f"{Colors.green if(braille) else Colors.blue}{char}{Colors.end}")

			output_lines.append(f"{self.__mapFrame[5]}{''.join(lines)}{self.__mapFrame[5]}")

		__dimsOutput = f"{self.__dims[0]}x{self.__dims[1]}"
		output_lines.append("".join([
			self.__mapFrame[2], self.__mapFrame[4]*(len([ n for n in range(0, self.__dims[1], 2) ])-len(__dimsOutput)-2), self.__mapFrame[9],
			Colors.purple, __dimsOutput, Colors.end,
			self.__mapFrame[8], self.__mapFrame[3]
		]))

		for i in range(len(output_lines)):
			if(self.stats and (i < len(stats))): # Affichage des statistiques
				output_lines[i] += f" {stats[i]}"

			elif(self.helper and (len(output_lines)-i-1 < len(help))): # Affichage de l'aide
				output_lines[i] += f" {help[len(output_lines)-i-1]}"

			else:
				output_lines[i] += " "*sum([_, __, 2])

		print("\n".join(output_lines), flush=True)
		return(True)

	def initMap(self, x: int, y: int) -> bool: # Initialisation de la map dans l'objet
		self.__map		= list[list[int]](self.__makeMap((int(x), int(y))))
		self.__dims		= tuple[int]((int(x), int(y)))
		self.__cells	= int(prod(self.__dims))

		return(self.__saveJSON())

	def reset(self) -> bool: # Reset complet de toute la map
		self.__iterations = 0
		self.__map = self.__makeMap(self.__dims)
		print(f"{Icons.succ}Map '{self.mapName}' reset !{'':<{self.__dims[1]-len(self.mapName)}}")
		return(self.__saveJSON())

	def start(self) -> bool: # Lancement du jeu
		self.__entities = Entity()
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

				match(SYSTEM):
					case(SystemEnum.WINDOWS):
						self.__controlsWindows(_keyPressed, _hook)

					case(SystemEnum.LINUX):
						self.__controlsLinux()

		except(KeyboardInterrupt):
			self.__label(f"STOPPED", Colors.red)

			if("_hook" in locals()):
				_hook()

			if(self.__saveJSON()):
				print(f"{Icons.succ}Map '{self.mapName}' saved !{'':<{self.__dims[1]-len(self.mapName)}}")

		return(True)
