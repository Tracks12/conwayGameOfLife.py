#!/bin/python3
# -*- coding: utf-8 -*-

# Module de barre de chargement

from time import sleep

from core.colors import Colors

def loadBar(msg = ["", ""]): # Barre de charement
	arr = ['\\', '|', '/', '-']

	for i in range(0, 10):
		print(f" [{Colors.yellow}{arr[i % len(arr)]}{Colors.end}] {msg[0]}", end = "\r")
		sleep(.05)

	print(f" [{Colors.green}*{Colors.end}] {msg[1]}")
