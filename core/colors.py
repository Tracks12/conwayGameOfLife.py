#!/bin/python3
# -*- coding: utf-8 -*-

# Module de coloration pour les système Linux/Unix

from platform import system

class Colors:
	if(system() == "Linux"):
		bold   = "\033[1m"
		italic = "\033[3m"

		red    = "\033[31m"
		green  = "\033[32m"
		blue   = "\033[34m"
		yellow = "\033[33m"

		end    = "\033[0m"

	else:
		bold = italic = end = ""
		red = green = blue = yellow = ""
