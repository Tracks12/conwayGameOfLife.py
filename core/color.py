#!/bin/python3
# -*- coding: utf-8 -*-

from platform import system

class Color:
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
