#!/bin/python3
# -*- coding: utf-8 -*-

# Module d'icône ascii

from core.color import Color

class Icon:
	warn = " {}{}[!]{} - ".format(Color.bold, Color.red, Color.end)
	info = " {}{}(i){} - ".format(Color.bold, Color.blue, Color.end)
	tips = " {}{}(?){} - ".format(Color.bold, Color.green, Color.end)
