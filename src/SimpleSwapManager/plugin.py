# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 Paderman
#
# Simple Swap Manager for Enigma2 (openATV, OpenPLi, OpenViX, ...)
#
from __future__ import absolute_import

import os

from enigma import eTimer
from Components.config import config, ConfigSubsection, ConfigText, ConfigSelection, ConfigInteger, ConfigYesNo
from Plugins.Plugin import PluginDescriptor

from . import _
from . import swaputil

VERSION = "1.1.1"

config.plugins.simpleswapmanager = ConfigSubsection()
config.plugins.simpleswapmanager.bootfile = ConfigText(default="")
config.plugins.simpleswapmanager.swappiness = ConfigSelection(
	default="system",
	choices=[("system", _("System default"))] + [(str(i), str(i)) for i in range(0, 101, 10)])
# zram: compressed swap in RAM (size 0 = not configured)
config.plugins.simpleswapmanager.zram_size = ConfigInteger(default=0, limits=(0, 65536))
config.plugins.simpleswapmanager.zram_autostart = ConfigYesNo(default=True)
config.plugins.simpleswapmanager.zram_algo = ConfigText(default="auto")
config.plugins.simpleswapmanager.menu = ConfigSelection(
	default="both",
	choices=[("both", _("Plugins and storage menu")), ("plugins", _("Plugin browser only"))])
# update check: asks GitHub at most once a day when the plugin is opened,
# only after the user agreed (asked once when the plugin is opened for the first time)
config.plugins.simpleswapmanager.update_check = ConfigYesNo(default=False)
config.plugins.simpleswapmanager.update_asked = ConfigYesNo(default=False)
config.plugins.simpleswapmanager.update_last = ConfigText(default="")    # time of the last check
config.plugins.simpleswapmanager.update_latest = ConfigText(default="")  # latest version found


def zramAlgorithm():
	"""Configured algorithm, or the best available one for 'auto'."""
	value = config.plugins.simpleswapmanager.zram_algo.value
	available = swaputil.zram_algorithms()[0]
	if value and value != "auto" and value in available:
		return value
	return swaputil.zram_best_algorithm(available)


class SwapAutoStart(object):
	"""Activates the configured swap file after enigma2 has started.

	Removable media are often mounted a little later than enigma2 starts,
	so we wait (non-blocking) for the file to appear.
	"""
	RETRY_MS = 5000
	MAX_TRIES = 36  # 3 minutes

	def __init__(self):
		self.tries = 0
		self.container = None
		self.timer = eTimer()
		try:
			self.timer.callback.append(self.check)
		except AttributeError:
			self.timer_conn = self.timer.timeout.connect(self.check)

	def start(self):
		cfg = config.plugins.simpleswapmanager
		# remember OOM kills before the kernel log forgets them (e.g. enigma2 itself was killed)
		swaputil.update_oom_history()
		if cfg.swappiness.value != "system":
			swaputil.set_swappiness(cfg.swappiness.value)
		if cfg.bootfile.value:
			self.timer.start(3000, True)
		self.startZram()

	def startZram(self):
		"""zram needs no drive, so it can be activated right away."""
		cfg = config.plugins.simpleswapmanager
		if not cfg.zram_size.value or not cfg.zram_autostart.value:
			return
		if swaputil.zram_path() in swaputil.active_paths():
			print("[SimpleSwapManager] zram already active")
			return
		if not swaputil.zram_supported():
			print("[SimpleSwapManager] zram configured but not supported by this kernel")
			return
		algo = zramAlgorithm()
		print("[SimpleSwapManager] activating zram: %d MB, %s" % (cfg.zram_size.value, algo or "default"))
		from enigma import eConsoleAppContainer
		self.zcontainer = eConsoleAppContainer()
		self.zcontainer.execute(swaputil.zram_setup_cmd(cfg.zram_size.value, algo))

	def check(self):
		path = config.plugins.simpleswapmanager.bootfile.value
		if not path:
			return
		if path in swaputil.active_paths():
			print("[SimpleSwapManager] swap already active: %s" % path)
			return
		if swaputil.is_swap_file(path):
			print("[SimpleSwapManager] activating swap file %s" % path)
			from enigma import eConsoleAppContainer
			self.container = eConsoleAppContainer()
			self.container.execute("swapon %s" % swaputil.shell_quote(path))
			return
		self.tries += 1
		if self.tries < self.MAX_TRIES:
			self.timer.start(self.RETRY_MS, True)
		else:
			print("[SimpleSwapManager] swap file %s not found, giving up" % path)


autoStarter = None


def sessionstart(reason, session=None, **kwargs):
	global autoStarter
	if reason == 0 and autoStarter is None:
		autoStarter = SwapAutoStart()
		autoStarter.start()


def main(session, **kwargs):
	try:
		from .ui import SwapManagerScreen
		session.open(SwapManagerScreen, VERSION)
	except Exception as e:
		# never take the whole GUI down because of the plugin
		import traceback
		traceback.print_exc()
		from Screens.MessageBox import MessageBox
		session.open(MessageBox, "Simple Swap Manager:\n%s" % e, MessageBox.TYPE_ERROR)


def _menuTarget():
	"""Menu id of the storage / system menu - differs between images."""
	try:
		with open("/usr/share/enigma2/menu.xml", "r") as f:
			xml = f.read()
	except (IOError, OSError):
		xml = ""
	for key in ("harddisk", "extended"):  # openATV and derivatives
		if 'key="%s"' % key in xml:
			return key
	return "system"  # OpenPLi, OpenViX, ...


MENU_TARGET = _menuTarget()


def menu(menuid, **kwargs):
	if menuid == MENU_TARGET and config.plugins.simpleswapmanager.menu.value == "both":
		return [(_("Simple Swap Manager"), main, "simple_swap_manager", 50)]
	return []


def Plugins(path=None, **kwargs):
	name = _("Simple Swap Manager")
	desc = _("Create and manage swap files")
	icon = "plugin.png"
	return [
		PluginDescriptor(name=name, description=desc, where=PluginDescriptor.WHERE_PLUGINMENU, icon=icon, fnc=main),
		PluginDescriptor(name=name, description=desc, where=PluginDescriptor.WHERE_MENU, fnc=menu),
		PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=sessionstart),
	]
