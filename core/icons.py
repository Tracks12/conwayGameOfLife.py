#!/bin/python3
# -*- coding: utf-8 -*-

# Module d'icône ascii

from core.colors import Colors

class Icons:
	warn = " {}{}[!]{} - ".format(Colors.bold, Colors.red, Colors.end)
	info = " {}{}(i){} - ".format(Colors.bold, Colors.blue, Colors.end)
	tips = " {}{}(?){} - ".format(Colors.bold, Colors.green, Colors.end)
