#!/bin/python3
# -*- coding: utf-8 -*-

# Module de coloration pour les système Linux/Unix

from platform import system

class Colors:
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
