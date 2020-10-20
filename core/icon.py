#!/bin/python3
# -*- coding: utf-8 -*-

from core.color import Color

class Icon:
	warn = " {}{}[!]{} - ".format(Color.bold, Color.red, Color.end)
	info = " {}{}(i){} - ".format(Color.bold, Color.blue, Color.end)
