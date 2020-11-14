#!/bin/python3
# -*- coding: utf-8 -*-

from json import loads
from time import sleep
from zlib import decompress

from core import B64, Colors, Icons

class Loader: # Module de chargements
	def anim(msg):
		arr = ['\\', '|', '/', '-']

		for i in range(0, 10):
			print(f" [{Colors.yellow}{arr[i % len(arr)]}{Colors.end}] {msg}", end = "\r")
			sleep(.05)

	def map(file, msg = ["", "", ""]): # Méthode de chargement pour fichier MAP
		Loader.anim(msg[0])

		try:
			dataMAP = loads(B64.decode(decompress(file.read())))
			print(f"{Icons.succ}{msg[1]}")
			return(dataMAP)

		except Exception:
			print(f"{Icons.fail}{msg[2]}")
			return(False)

	def json(file, msg = ["", "", ""]): # Méthode de chargement pour fichier JSON
		Loader.anim(msg[0])

		try:
			dataMAP = loads(file.read())
			print(f"{Icons.succ}{msg[1]}")
			return(dataMAP)

		except Exception:
			print(f"{Icons.fail}{msg[2]}")
			return(False)
