# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 Paderman
from __future__ import absolute_import

import gettext

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS

PluginLanguageDomain = "SimpleSwapManager"
PluginLanguagePath = "SystemPlugins/SimpleSwapManager/locale"


# The package scripts (install / update / removal in a terminal) read this file,
# so they can talk in the same language as the GUI.
LANGUAGE_FILE = "/etc/enigma2/simpleswapmanager.lang"


def rememberLanguage():
	try:
		lang = language.getLanguage() or ""
		try:
			with open(LANGUAGE_FILE, "r") as f:
				if f.read().strip() == lang:
					return
		except (IOError, OSError):
			pass
		with open(LANGUAGE_FILE, "w") as f:
			f.write(lang + "\n")
	except Exception:
		pass  # purely cosmetic, never fail because of it


# The catalogue is loaded into memory once per language, so texts stay translated
# even after the plugin files were removed (uninstall from the settings).
_catalog = None


def localeInit():
	global _catalog
	localedir = resolveFilename(SCOPE_PLUGINS, PluginLanguagePath)
	gettext.bindtextdomain(PluginLanguageDomain, localedir)
	try:
		_catalog = gettext.translation(PluginLanguageDomain, localedir, languages=[language.getLanguage()])
	except Exception:
		_catalog = None
	rememberLanguage()


def _(txt):
	if not txt:
		return txt
	if _catalog is not None:
		return _catalog.gettext(txt)  # str on Python 3, UTF-8 bytes on Python 2 (like dgettext)
	return gettext.dgettext(PluginLanguageDomain, txt)


localeInit()
language.addCallback(localeInit)
