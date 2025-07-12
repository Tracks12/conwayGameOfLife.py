#!/bin/python3
# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode
from platform import system

SYSTEM = system()
CMD_CLEAR = "clear" if(SYSTEM == "Linux") else "cls" # Commande de nettoyage de la console

class Colors: # Module de coloration pour les système Linux/Unix
	if(SYSTEM == "Linux"):
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
	# Icônes fixes
	warn	= f" {Colors.bold}{Colors.red}[!]{Colors.end} - "
	info	= f" {Colors.bold}{Colors.blue}(i){Colors.end} - "
	tips	= f" {Colors.bold}{Colors.green}(?){Colors.end} - "

	# Icônes de chargement
	succ	= f" [{Colors.bold}{Colors.green}*{Colors.end}] "
	fail	= f" [{Colors.bold}{Colors.red}x{Colors.end}] "

class B64: # Encode/Decode ascii string in base64
	def encode(str: str = "") -> bytes:
		return(b64encode(str.encode("ascii")))

	def decode(str: bytes = "") -> str:
		return(b64decode(str).decode("ascii"))
