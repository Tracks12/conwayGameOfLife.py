#!/bin/python3
# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode
from platform import system

class SystemEnum:
	LINUX	= "Linux"
	WINDOWS	= "Windows"

SYSTEM = system()
_isLinux = bool(SYSTEM == SystemEnum.LINUX)

CMD_CLEAR = "clear" if(_isLinux) else "cls" # Commande de nettoyage de la console

BRAILLE_MAP = dict[tuple[int, int], int]({
	(0, 0): 0, (0, 1): 3,
	(1, 0): 1, (1, 1): 4,
	(2, 0): 2, (2, 1): 5,
	(3, 0): 6, (3, 1): 7,
})

class Border:
	ASCII	= [ "+", "+", "+", "+", "-", "|", "+", "+", "+", "+" ]
	SIMPLE	= [ "┌", "┐", "└", "┘", "─", "│", "┌", "┐", "└", "┘" ]
	SMOOTH	= [ "╭", "╮", "╰", "╯", "─", "│", "┌", "┐", "└", "┘" ]
	DASHED	= [ "┌", "┐", "└", "┘", "╌", "┆", "┌", "┐", "└", "┘" ]
	DOTTED	= [ "┌", "┐", "└", "┘", "┈", "┊", "┌", "┐", "└", "┘" ]
	DOUBLE	= [ "╔", "╗", "╚", "╝", "═", "║", "╔", "╗", "╚", "╝" ]

class Colors: # Module de coloration pour les système Linux/Unix
	bold	= "\033[1m"		if(_isLinux) else ""
	italic	= "\033[3m"		if(_isLinux) else ""

	red		= "\033[31m"	if(_isLinux) else ""
	green	= "\033[32m"	if(_isLinux) else ""
	yellow	= "\033[33m"	if(_isLinux) else ""
	blue	= "\033[34m"	if(_isLinux) else ""
	purple	= "\033[35m"	if(_isLinux) else ""
	cyan	= "\033[36m"	if(_isLinux) else ""
	white	= "\033[37m"	if(_isLinux) else ""

	end		= "\033[0m"		if(_isLinux) else ""

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
