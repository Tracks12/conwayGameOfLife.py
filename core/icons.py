#!/bin/python3
# -*- coding: utf-8 -*-

# Module d'icône ascii

from core.colors import Colors

class Icons:
	warn = f" {Colors.bold}{Colors.red}[!]{Colors.end} - "
	info = f" {Colors.bold}{Colors.blue}(i){Colors.end} - "
	tips = f" {Colors.bold}{Colors.green}(?){Colors.end} - "
