#!/bin/python3
# -*- coding: utf-8 -*-

from json import load
from platform import system
from time import sleep

class Colors: # Module de coloration pour les système Linux/Unix
	if(system() == "Linux"):
		bold	= "\033[1m"
		italic	= "\033[3m"

		red		= "\033[31m"
		green	= "\033[32m"
		yellow	= "\033[33m"
		blue	= "\033[34m"
		purple	= "\033[35m"
		cyan	= "\033[36m"
		white	= "\033[37m"

		end		= "\033[0m"

	else:
		bold = italic = end = ""
		red = green = yellow = blue = purple = cyan = white = ""

class Icons: # Module d'icône ascii
	warn = f" {Colors.bold}{Colors.red}[!]{Colors.end} - "
	info = f" {Colors.bold}{Colors.blue}(i){Colors.end} - "
	tips = f" {Colors.bold}{Colors.green}(?){Colors.end} - "

class B64: # Encode/Decode ascii string
    def encode(str = ""):
        return(b64encode(str.encode("ascii")).decode("ascii"))

    def decode(str = ""):
        return(b64decode(str).decode("ascii"))

def JSONloader(file, msg = ["", "", ""]): # Fonction de barre de chargement
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
