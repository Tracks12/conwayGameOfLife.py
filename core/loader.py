#!/bin/python3
# -*- coding: utf-8 -*-

# Module de barre de chargement

from json import load
from time import sleep

from core.colors import Colors

def JSONloader(file, msg = ["", "", ""]): # Barre de charement
	arr = ['\\', '|', '/', '-']

	for i in range(0, 10):
		print(f" [{Colors.yellow}{arr[i % len(arr)]}{Colors.end}] {msg[0]}", end = "\r")
		sleep(.05)

	try:
		dataJSON = load(file)
		print(f" [{Colors.green}*{Colors.end}] {msg[1]}")
		return(dataJSON)

	except:
		print(f" [{Colors.red}*{Colors.end}] {msg[2]}")
		return(False)
