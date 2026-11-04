# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 Paderman
#
# Simple Swap Manager - user interface
#
# The skin is designed for 1920x1080 and scaled to the current desktop,
# so it looks the same on HD, FullHD and UHD skins and on every image.
#
from __future__ import absolute_import, division

import os
import re
import signal
import time

from enigma import eConsoleAppContainer, eListbox, eListboxPythonMultiContent, eTimer, eSize, ePoint, \
	getDesktop, gFont, RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, RT_VALIGN_CENTER

from Components.ActionMap import ActionMap
from Components.config import config, configfile
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Screens.Screen import Screen

from . import _
from . import swaputil

# ---------------------------------------------------------------- look & feel

C_BG = 0x0F141B
C_CARD = 0x1A2230
C_SEL = 0x26344A
C_LINE = 0x2C3A4F
C_TEXT = 0xE6EDF3
C_MUTED = 0x8B98A5
C_ACCENT = 0x3FA9F5
C_PURPLE = 0xA371F7
C_GREEN = 0x2EA043
C_RED = 0xDA3633
C_YELLOW = 0xD29922
C_BLUE = 0x1F6FEB
C_TRACK = 0x303A4A
C_ORANGE = 0xDB6D28
C_HELP = 0xB4BFCA        # explanation texts: brighter than muted, calmer than text
C_RED_TEXT = 0xF85149    # red as text color, readable on the selection bar too
# darker badge backgrounds so the white label reaches a contrast of 4.5:1
PILL_COLORS = {C_GREEN: 0x238636, C_ORANGE: 0xBD561D, C_YELLOW: 0x9E6A03}


def _hex(c):
	return "#00%06X" % c


_DESKTOP_W = getDesktop(0).size().width() or 1280
_F = _DESKTOP_W / 1920.0


def S(v):
	return int(round(v * _F))


def scaleSkin(xml):
	"""Scale a 1920x1080 skin to the current desktop size and insert colors."""
	def pair(m):
		return '%s="%d,%d"' % (m.group(1), S(int(m.group(2))), S(int(m.group(3))))

	def font(m):
		return 'font="%s;%d"' % (m.group(1), S(int(m.group(2))))

	xml = re.sub(r'\b(position|size)="(\d+),(\d+)"', pair, xml)
	xml = re.sub(r'font="(\w+);(\d+)"', font, xml)
	for name, value in COLORS.items():
		xml = xml.replace("$%s$" % name, _hex(value))
	return xml


COLORS = {
	"bg": C_BG, "card": C_CARD, "sel": C_SEL, "line": C_LINE, "text": C_TEXT, "muted": C_MUTED,
	"accent": C_ACCENT, "purple": C_PURPLE, "green": C_GREEN, "red": C_RED, "yellow": C_YELLOW,
	"blue": C_BLUE, "track": C_TRACK, "help": C_HELP,
}


def footerSkin(y, width, keys=("red", "green", "yellow", "blue")):
	"""Colored key hints: a slim colored bar plus the label."""
	out = []
	step = width // len(keys)
	for i, key in enumerate(keys):
		x = 40 + i * step
		out.append('<widget name="keybar_%s" position="%d,%d" size="6,36" backgroundColor="$%s$" zPosition="2" />' % (key, x, y + 7, key))
		out.append('<widget name="key_%s" position="%d,%d" size="%d,50" font="Regular;26" halign="left" valign="center" '
			'foregroundColor="$text$" backgroundColor="$bg$" transparent="1" zPosition="2" />' % (key, x + 18, y, step - 30))
	return "".join(out)


class KeyLabel(Label):
	"""Color key label; hides the matching colored bar when the text is empty."""

	def __init__(self, screen, color, text=""):
		self.bar = Label("")
		Label.__init__(self, text)
		screen["keybar_" + color] = self.bar
		screen["key_" + color] = self
		screen.onLayoutFinish.append(self._sync)

	def setText(self, text):
		Label.setText(self, text)
		self._sync()

	def _sync(self):
		bar = getattr(self, "bar", None)
		if bar is not None and bar.instance:
			if self.getText():
				bar.show()
			else:
				bar.hide()


class ModernList(MenuList):
	"""MenuList with a multi content template, scaled fonts and own colors."""

	def __init__(self, items=None, itemHeight=100):
		MenuList.__init__(self, items or [], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.l.setFont(0, gFont("Regular", S(32)))
		self.l.setFont(1, gFont("Regular", S(24)))
		self.l.setFont(2, gFont("Regular", S(20)))
		self.l.setFont(3, gFont("Regular", S(26)))  # description lines under a title
		self.l.setItemHeight(S(itemHeight))

	def moveUp(self):
		if self.instance:
			self.instance.moveSelection(eListbox.moveUp)

	def moveDown(self):
		if self.instance:
			self.instance.moveSelection(eListbox.moveDown)

	def pageUpList(self):
		if self.instance:
			self.instance.moveSelection(eListbox.pageUp)

	def pageDownList(self):
		if self.instance:
			self.instance.moveSelection(eListbox.pageDown)

	def index(self):
		return self.getSelectionIndex() if self.instance else 0


def _text(x, y, w, h, font, text, color=C_TEXT, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, back=None, back_sel=None, color_sel=None):
	return MultiContentEntryText(pos=(S(x), S(y)), size=(S(w), S(h)), font=font, flags=flags, text=text,
		color=color, color_sel=color if color_sel is None else color_sel, backcolor=back, backcolor_sel=back if back_sel is None else back_sel)


def _pill(x, y, w, text, color):
	return _text(x, y, w, 40, 2, text, color=0xFFFFFF, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, back=PILL_COLORS.get(color, color))


class Bar(object):
	"""A flat progress bar built from two labels (works with every image)."""

	def __init__(self, screen, name):
		self.screen = screen
		self.name = name
		screen[name + "_track"] = Label("")
		screen[name + "_fill"] = Label("")
		self.value = 0.0

	def set(self, fraction):
		self.value = max(0.0, min(1.0, fraction))
		track = self.screen[self.name + "_track"].instance
		fill = self.screen[self.name + "_fill"].instance
		if track is None or fill is None:
			return
		size = track.size()
		w = int(size.width() * self.value)
		if w <= 0:
			fill.hide()
		else:
			fill.move(track.position())  # may have been moved by setSegment()
			fill.resize(eSize(w, size.height()))
			fill.show()

	def setSegment(self, start, length):
		"""Indeterminate mode: show a moving segment."""
		track = self.screen[self.name + "_track"].instance
		fill = self.screen[self.name + "_fill"].instance
		if track is None or fill is None:
			return
		size = track.size()
		pos = track.position()
		x = int(size.width() * start)
		w = max(1, min(int(size.width() * length), size.width() - x))
		fill.move(ePoint(pos.x() + x, pos.y()))
		fill.resize(eSize(w, size.height()))
		fill.show()


def barSkin(name, x, y, w, h, color):
	return ('<widget name="%s_track" position="%d,%d" size="%d,%d" backgroundColor="$track$" zPosition="1" />'
		'<widget name="%s_fill" position="%d,%d" size="%d,%d" backgroundColor="$%s$" zPosition="2" />') % (
		name, x, y, w, h, name, x, y, w, h, color)


class StackBar(object):
	"""Bar with two coloured parts side by side (e.g. RAM used + swap used)."""

	def __init__(self, screen, name):
		self.screen = screen
		self.name = name
		for part in ("track", "a", "b"):
			screen["%s_%s" % (name, part)] = Label("")

	def set(self, first, second):
		track = self.screen[self.name + "_track"].instance
		a = self.screen[self.name + "_a"].instance
		b = self.screen[self.name + "_b"].instance
		if track is None or a is None or b is None:
			return
		size = track.size()
		pos = track.position()
		first = max(0.0, min(1.0, first))
		second = max(0.0, min(1.0 - first, second))
		wa = int(size.width() * first)
		wb = int(size.width() * second)
		if wa > 0:
			a.resize(eSize(wa, size.height()))
			a.show()
		else:
			a.hide()
		if wb > 0:
			b.move(ePoint(pos.x() + wa, pos.y()))
			b.resize(eSize(wb, size.height()))
			b.show()
		else:
			b.hide()


def stackBarSkin(name, x, y, w, h, color_a, color_b):
	return ('<widget name="%s_track" position="%d,%d" size="%d,%d" backgroundColor="$track$" zPosition="1" />'
		'<widget name="%s_a" position="%d,%d" size="%d,%d" backgroundColor="$%s$" zPosition="2" />'
		'<widget name="%s_b" position="%d,%d" size="%d,%d" backgroundColor="$%s$" zPosition="2" />') % (
		name, x, y, w, h, name, x, y, w, h, color_a, name, x, y, w, h, color_b)


def kindName(kind):
	return {"hdd": _("Hard disk"), "usb": _("USB storage"), "sd": _("SD card"), "flash": _("Internal flash")}.get(kind, kind)


# ---------------------------------------------------------------- selection screen

class SwapSelectScreen(Screen):
	"""Generic modern selection / confirmation screen.

	items: list of tuples (key, title, detail, badge, badgeColor)
	Returns the key of the selected item or None.
	"""
	skin = scaleSkin("""
	<screen name="SimpleSwapSelect" position="center,center" size="1100,760" flags="wfNoBorder" backgroundColor="$bg$">
		<eLabel position="0,0" size="1100,760" backgroundColor="$bg$" zPosition="-1" />
		<eLabel position="0,0" size="1100,6" backgroundColor="$accent$" zPosition="1" />
		<widget name="title" position="40,28" size="1020,56" font="Regular;40" foregroundColor="$text$" backgroundColor="$bg$" transparent="1" />
		<widget name="message" position="40,100" size="1020,236" font="Regular;30" foregroundColor="$help$" backgroundColor="$bg$" transparent="1" valign="top" />
		<widget name="list" position="40,346" size="1020,336" scrollbarMode="showOnDemand" backgroundColor="$bg$" backgroundColorSelected="$sel$" foregroundColor="$text$" foregroundColorSelected="$text$" transparent="0" />
		<eLabel position="40,690" size="1020,2" backgroundColor="$line$" />
		<widget name="hint" position="40,700" size="1020,50" font="Regular;24" foregroundColor="$muted$" backgroundColor="$bg$" transparent="1" valign="center" />
	</screen>""")

	def __init__(self, session, title, message, items, selected=None):
		Screen.__init__(self, session)
		self.skinName = "SimpleSwapSelect"
		self.entries = items
		self["title"] = Label(title)
		self["message"] = Label(message)
		self["hint"] = Label(_("OK  Select     EXIT  Back"))
		self["list"] = ModernList(itemHeight=84)
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], {
			"ok": self.ok,
			"cancel": self.cancel,
			"up": self["list"].moveUp,
			"down": self["list"].moveDown,
			"left": self["list"].pageUpList,
			"right": self["list"].pageDownList,
		}, -1)
		self.selected = selected
		self.onLayoutFinish.append(self.build)

	def build(self):
		self.setTitle(self["title"].getText())
		rows = []
		start = 0
		for i, item in enumerate(self.entries):
			key, title, detail = item[0], item[1], item[2]
			badge = item[3] if len(item) > 3 else None
			badgeColor = item[4] if len(item) > 4 else C_ACCENT
			row = [key]
			if detail:
				row.append(_text(24, 6, 720, 44, 0, title))
				row.append(_text(24, 46, 710 if badge else 940, 34, 3, detail, color=C_MUTED))
			else:
				row.append(_text(24, 0, 720, 84, 0, title))
			if badge:
				row.append(_pill(750, 22, 240, badge, badgeColor))
			rows.append(row)
			if key == self.selected:
				start = i
		self["list"].setList(rows)
		if rows:
			self["list"].moveToIndex(start)

	def ok(self):
		cur = self["list"].getCurrent()
		self.close(cur[0] if cur else None)

	def cancel(self):
		self.close(None)


def openMessage(session, title, message, callback=None):
	cb = (lambda r: callback()) if callback else (lambda r: None)
	session.openWithCallback(cb, SwapSelectScreen, title, message, [("ok", _("OK"), "")])


def openConfirm(session, callback, title, message, yesText, noText=None, default="yes"):
	items = [("yes", yesText, ""), ("no", noText or _("Cancel"), "")]
	session.openWithCallback(lambda r: callback(r == "yes"), SwapSelectScreen, title, message, items, default)


# ---------------------------------------------------------------- task / progress screen

# messages printed by our own shell scripts -> readable, translated text
KNOWN_ERRORS = {
	"zram device not found": _("The zram device could not be created. This kernel probably does not support zram."),
}

class SwapTaskScreen(Screen):
	"""Runs a list of shell steps asynchronously and shows the progress.

	steps: list of dicts: {"label": str, "cmd": str, "progress": (path, bytes) optional,
	                       "cancel": bool, "fallback": str}
	Closes with (success, message).
	"""
	skin = scaleSkin("""
	<screen name="SimpleSwapTask" position="center,center" size="1100,520" flags="wfNoBorder" backgroundColor="$bg$">
		<eLabel position="0,0" size="1100,520" backgroundColor="$bg$" zPosition="-1" />
		<eLabel position="0,0" size="1100,6" backgroundColor="$accent$" zPosition="1" />
		<widget name="title" position="40,28" size="1020,56" font="Regular;40" foregroundColor="$text$" backgroundColor="$bg$" transparent="1" />
		<widget name="step" position="40,120" size="760,50" font="Regular;30" foregroundColor="$text$" backgroundColor="$bg$" transparent="1" valign="center" />
		<widget name="percent" position="800,100" size="260,80" font="Regular;64" halign="right" foregroundColor="$accent$" backgroundColor="$bg$" transparent="1" valign="center" />
		""" + barSkin("bar", 40, 200, 1020, 26, "accent") + """
		<widget name="detail" position="40,250" size="1020,130" font="Regular;26" foregroundColor="$muted$" backgroundColor="$bg$" transparent="1" valign="top" />
		<eLabel position="40,430" size="1020,2" backgroundColor="$line$" />
		""" + footerSkin(450, 1020, ("red",)) + """
	</screen>""")

	def __init__(self, session, title, steps, autoClose=False, doneText=""):
		Screen.__init__(self, session)
		self.skinName = "SimpleSwapTask"
		self.steps = steps
		self.autoClose = autoClose
		self.doneText = doneText
		self.index = -1
		self.output = ""
		self.running = False
		self.cancelled = False
		self.finished = False
		self.success = False
		self.anim = 0.0
		self["title"] = Label(title)
		self["step"] = Label("")
		self["percent"] = Label("")
		self["detail"] = Label("")
		KeyLabel(self, "red")
		self.bar = Bar(self, "bar")
		self.container = eConsoleAppContainer()
		self._connect(self.container, "appClosed", self.stepClosed)
		self._connect(self.container, "dataAvail", self.dataAvail)
		try:
			self._connect(self.container, "stderrAvail", self.dataAvail)
		except AttributeError:
			pass
		self.timer = eTimer()
		self._connect(self.timer, "callback", self.tick)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {
			"ok": self.okPressed,
			"cancel": self.cancelPressed,
			"red": self.cancelPressed,
		}, -1)
		self.onLayoutFinish.append(self.startNext)
		self.onClose.append(self.cleanup)

	def _connect(self, obj, signal, fnc):
		if not hasattr(self, "_conns"):
			self._conns = []
		if signal == "callback":
			try:
				obj.callback.append(fnc)
				return
			except AttributeError:
				self._conns.append(obj.timeout.connect(fnc))
				return
		sig = getattr(obj, signal)
		try:
			sig.append(fnc)
		except AttributeError:
			self._conns.append(sig.connect(fnc))

	def currentStep(self):
		return self.steps[self.index] if 0 <= self.index < len(self.steps) else None

	def startNext(self):
		self.setTitle(self["title"].getText())
		self.index += 1
		step = self.currentStep()
		if step is None:
			self.done(True)
			return
		self.runStep(step, step["cmd"])

	def runStep(self, step, cmd):
		self.output = ""
		self["step"].setText(step["label"])
		self["key_red"].setText(_("Cancel") if step.get("cancel") else "")
		if step.get("progress"):
			self.bar.set(0)
			self["percent"].setText("0%")
		else:
			self["percent"].setText("")
			self.anim = 0.0
			self.bar.setSegment(0, 0.2)
		self["detail"].setText(_("Please wait..."))
		self.running = True
		print("[SimpleSwapManager] run: %s" % cmd)
		if self.container.execute(cmd):
			self.running = False
			self.fail(_("Could not start command."))
			return
		self.timer.start(250, False)

	def tick(self):
		step = self.currentStep()
		if step is None:
			return
		prog = step.get("progress")
		if prog:
			path, total = prog
			try:
				cur = os.path.getsize(path)
			except OSError:
				cur = 0
			frac = float(cur) / total if total else 0
			self.bar.set(frac)
			self["percent"].setText("%d%%" % int(frac * 100))
			self["detail"].setText(_("%s of %s written") % (swaputil.human_bytes(cur), swaputil.human_bytes(total)))
		else:
			self.anim = (self.anim + 0.03) % 1.0
			self.bar.setSegment(self.anim * 0.8, 0.2)

	def dataAvail(self, data):
		if isinstance(data, bytes):
			data = data.decode("utf-8", "ignore")
		self.output += data

	def stepClosed(self, retval):
		self.timer.stop()
		self.running = False
		if self.cancelled:
			return
		step = self.currentStep()
		if retval != 0:
			fallback = step.get("fallback")
			if fallback and not step.get("_fallbackUsed"):
				step["_fallbackUsed"] = True
				self.runStep(step, fallback)
				return
			msg = self.output.strip().splitlines()
			self.fail(msg[-1] if msg else _("Error code %d") % retval)
			return
		if step.get("progress"):
			self.bar.set(1)
			self["percent"].setText("100%")
		self.startNext()

	def fail(self, message):
		self.finished = True
		self.success = False
		self.message = message
		self.timer.stop()
		self["step"].setText(_("Error"))
		self["percent"].setText("")
		self.bar.set(0)
		message = KNOWN_ERRORS.get(message.strip(), message)
		self.message = message
		self["detail"].setText(u"%s\n%s" % (self.currentStep()["label"], message))
		self["key_red"].setText(_("Close"))
		failed = self.currentStep()
		if failed and failed.get("onFail"):
			try:
				failed["onFail"]()
			except Exception as e:
				print("[SimpleSwapManager] cleanup error: %s" % e)

	def done(self, success):
		self.finished = True
		self.success = success
		self.message = ""
		self.bar.set(1)
		self["percent"].setText("")
		self["step"].setText(_("Done"))
		self["detail"].setText(self.doneText)
		self["key_red"].setText(_("Close"))
		if self.autoClose:
			self.close((True, ""))
		else:
			self["percent"].setText("100%")

	def okPressed(self):
		if self.finished:
			self.close((self.success, self.message))

	def cancelPressed(self):
		if self.finished:
			self.close((self.success, self.message))
			return
		step = self.currentStep()
		if step and step.get("cancel") and self.running:
			self.cancelled = True
			self.timer.stop()
			self.killProcessGroup()
			if step.get("onCancel"):
				try:
					step["onCancel"]()
				except Exception as e:
					print("[SimpleSwapManager] cancel cleanup error: %s" % e)
			self.close((False, _("Cancelled.")))

	def killProcessGroup(self):
		"""Kill the shell and its children (dd) - the container runs them in their own session."""
		try:
			pid = self.container.getPID()
			if pid and pid > 0:
				os.killpg(pid, signal.SIGKILL)
		except Exception as e:
			print("[SimpleSwapManager] killpg: %s" % e)
		try:
			self.container.kill()
		except Exception:
			pass

	def cleanup(self):
		self.timer.stop()
		if self.running:
			self.killProcessGroup()


# ---------------------------------------------------------------- capabilities

def zramReasonText(reason, kernel=""):
	"""Human readable explanation of swaputil.zram_status()."""
	return {
		"loaded": _("zram is loaded and ready to use."),
		"builtin": _("zram is built into the kernel."),
		"module": _("zram is available as a kernel module and is loaded when needed."),
		"not_in_kernel": _("The kernel of this receiver (%s) was built without zram. A swap file on a drive is the best solution here.") % kernel,
		"module_missing": _("The kernel supports zram as a module, but the module is not installed (kernel %s).") % kernel,
		"unknown": _("No zram support was found in the kernel (%s).") % kernel,
	}.get(reason, reason)


def zramShortText(supported, reason):
	if supported:
		return _("available")
	if reason == "module_missing":
		return _("module missing")
	return _("not supported")


class SwapInfoScreen(Screen):
	"""What does this receiver support? Box, kernel, zram, zswap, drives."""
	skin = scaleSkin("""
	<screen name="SimpleSwapInfo" position="center,center" size="1300,860" flags="wfNoBorder" backgroundColor="$bg$">
		<eLabel position="0,0" size="1300,860" backgroundColor="$bg$" zPosition="-1" />
		<eLabel position="0,0" size="1300,6" backgroundColor="$accent$" zPosition="1" />
		<widget name="title" position="40,28" size="1220,56" font="Regular;40" foregroundColor="$text$" backgroundColor="$bg$" transparent="1" />
		<widget name="list" position="40,104" size="1220,490" scrollbarMode="showOnDemand" backgroundColor="$bg$" backgroundColorSelected="$sel$" foregroundColor="$text$" foregroundColorSelected="$text$" />
		<widget name="help" position="40,606" size="1220,180" font="Regular;30" foregroundColor="$help$" backgroundColor="$bg$" transparent="1" valign="top" />
		<eLabel position="40,790" size="1220,2" backgroundColor="$line$" />
		<widget name="hint" position="40,800" size="1220,50" font="Regular;24" foregroundColor="$muted$" backgroundColor="$bg$" transparent="1" valign="center" />
	</screen>""")

	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = "SimpleSwapInfo"
		self["title"] = Label(_("System information"))
		self["help"] = Label("")
		self["hint"] = Label(_("UP/DOWN  Details     EXIT  Back"))
		self["list"] = ModernList(itemHeight=70)
		self.rows = []
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], {
			"ok": self.close,
			"cancel": self.close,
			"up": self.up,
			"down": self.down,
			"left": self.pageUp,
			"right": self.pageDown,
		}, -1)
		self.onLayoutFinish.append(self.build)

	def collect(self):
		si = swaputil.system_info()
		yes, no = C_GREEN, C_ORANGE
		rows = []

		def add(label, value, color=C_TEXT, help=""):
			rows.append((label, value, color, help))

		add(_("Receiver"), si["model"] or "-")
		add(_("Image"), si["image"] or "-")
		add(_("Kernel"), u"%s  (%s)" % (si["kernel"], si["arch"]), help=_("The kernel decides which memory features are available. It is part of the image and cannot be changed by a plugin."))
		add(_("Python"), si["python"])
		add(_("RAM"), swaputil.human_kb(si["ram_kb"]))
		oom = swaputil.update_oom_history()
		if oom["total"]:
			last = oom["events"][-1] if oom["events"] else None
			ov = _("%d times") % oom["total"]
			if last:
				ov += u"  ·  " + _("last: %s, %s") % (last["name"], time.strftime("%Y-%m-%d %H:%M", time.localtime(last["time"])))
			oc = C_RED
		else:
			ov, oc = _("never"), yes
		add(_("Out of memory"), ov, oc,
			_("How often RAM and swap were full and the kernel had to end a program (counted since the plugin was installed). If it happens, a swap file - or a bigger one - helps."))
		add(_("Swap support"), _("yes") if si["swap_kernel"] else _("no"), yes if si["swap_kernel"] else C_RED,
			_("Required for swap files, swap partitions and zram."))

		supported, reason = swaputil.zram_status()
		zhelp = zramReasonText(reason, si["kernel"]) + "\n" + _("zram compresses swapped out memory inside the RAM (about 2-3:1) - no drive needed.")
		add(_("zram (compressed RAM)"), zramShortText(supported, reason), yes if supported else no, zhelp)
		if supported:
			algos, current = swaputil.zram_algorithms()
			loaded = reason == "loaded"
			add(_("zram algorithms"), ", ".join(algos) if loaded else _("known after loading"), help=_("Compression algorithms offered by the kernel. lz4 is fastest, zstd compresses best."))

		zs = swaputil.zswap_status()
		if zs["available"]:
			zv = _("active (%s)") % zs["compressor"] if zs["enabled"] else _("available, inactive")
		else:
			zv = _("not supported")
		add(_("zswap"), zv, yes if zs["available"] else C_MUTED,
			_("zswap is a compressed cache in front of a swap file. It is only shown here for information."))

		locs = swaputil.find_locations()
		drives = [l for l in locs if l["kind"] != "flash"]
		if drives:
			dv = ", ".join(l["mount"] for l in drives)
			dc = yes
		else:
			dv = _("none (only internal flash)") if locs else _("none")
			dc = no
		add(_("Drives for swap files"), dv, dc, _("Drives with a Linux file system (ext2/3/4, xfs, ...) that can hold a swap file."))

		kc = _("yes") if si["kconfig"] else _("no")
		add(_("Kernel configuration"), kc, help=_("/proc/config.gz lets the plugin see exactly which features the kernel was built with."))
		add(_("Swappiness"), str(swaputil.get_swappiness()))
		add(_("Page size"), _("%d bytes") % si["page_size"])
		return rows

	def build(self):
		self.setTitle(self["title"].getText())
		self.rows = self.collect()
		lst = []
		for i, (label, value, color, help) in enumerate(self.rows):
			lst.append([i,
				_text(24, 0, 470, 70, 1, label, color=C_MUTED),
				_text(500, 0, 680, 70, 1, value, color=color, flags=RT_HALIGN_RIGHT | RT_VALIGN_CENTER),
			])
		self["list"].setList(lst)
		# start on the zram line - that is what people usually look for
		# ... unless memory already ran out: then that is the important line
		start = None
		for i, r in enumerate(self.rows):
			if r[0] == _("zram (compressed RAM)") and start is None:
				start = i
			if r[0] == _("Out of memory") and r[2] == C_RED:
				start = i
		if start is not None:
			self["list"].moveToIndex(start)
		self.updateHelp()

	def updateHelp(self):
		i = self["list"].index()
		self["help"].setText(self.rows[i][3] if 0 <= i < len(self.rows) else "")

	def up(self):
		self["list"].moveUp()
		self.updateHelp()

	def down(self):
		self["list"].moveDown()
		self.updateHelp()

	def pageUp(self):
		self["list"].pageUpList()
		self.updateHelp()

	def pageDown(self):
		self["list"].pageDownList()
		self.updateHelp()


# ---------------------------------------------------------------- settings screen

class SwapSettingsScreen(Screen):
	skin = scaleSkin("""
	<screen name="SimpleSwapSettings" position="center,center" size="1300,760" flags="wfNoBorder" backgroundColor="$bg$">
		<eLabel position="0,0" size="1300,760" backgroundColor="$bg$" zPosition="-1" />
		<eLabel position="0,0" size="1300,6" backgroundColor="$accent$" zPosition="1" />
		<widget name="title" position="40,28" size="1220,56" font="Regular;40" foregroundColor="$text$" backgroundColor="$bg$" transparent="1" />
		<widget name="list" position="40,110" size="1220,340" scrollbarMode="showOnDemand" backgroundColor="$bg$" backgroundColorSelected="$sel$" foregroundColor="$text$" foregroundColorSelected="$text$" />
		<widget name="help" position="40,464" size="1220,210" font="Regular;30" foregroundColor="$help$" backgroundColor="$bg$" transparent="1" valign="top" />
		<eLabel position="40,680" size="1220,2" backgroundColor="$line$" />
		""" + footerSkin(696, 1220, ("red", "green")) + """
	</screen>""")

	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = "SimpleSwapSettings"
		cfg = config.plugins.simpleswapmanager
		self["title"] = Label(_("Simple Swap Manager settings"))
		self["help"] = Label("")
		KeyLabel(self, "red", _("Cancel"))
		KeyLabel(self, "green", _("Save"))
		self["list"] = ModernList(itemHeight=85)

		files = [s["path"] for s in swaputil.list_swaps((cfg.bootfile.value,)) if s["type"] == "file"]
		if cfg.bootfile.value and cfg.bootfile.value not in files:
			files.append(cfg.bootfile.value)
		bootChoices = [("", _("Off"))] + [(f, f) for f in files]

		swapChoices = [("system", _("System default"))] + [(str(i), str(i)) for i in range(0, 101, 10)]
		current = swaputil.get_swappiness()

		self.options = [
			{
				"title": _("Swap file at startup"),
				"help": _("This swap file is activated automatically every time the receiver starts. The plugin waits up to three minutes for the storage device to be mounted."),
				"choices": bootChoices,
				"value": cfg.bootfile.value,
				"config": cfg.bootfile,
			},
			{
				"title": _("Swappiness"),
				"help": _("How eagerly the kernel moves memory to swap (0-100). Lower values keep data in RAM longer; 10-30 is a good choice for receivers. Current value: %d") % current
					+ "\n" + _("Lower values also mean fewer writes, which spares SD cards and USB sticks."),
				"choices": [(k, v) for k, v in swapChoices],
				"value": cfg.swappiness.value,
				"config": cfg.swappiness,
			},
		]
		zsupported, zreason = swaputil.zram_status()
		kernel = swaputil.system_info()["kernel"]
		self.options.append({
			"title": _("zram (compressed RAM)"),
			"help": zramReasonText(zreason, kernel),
			"choices": [("info", zramShortText(zsupported, zreason))],
			"value": "info",
			"config": None,
			"color": C_GREEN if zsupported else C_ORANGE,
		})
		if zsupported:
			algos = swaputil.zram_algorithms()[0]
			algoChoices = [("auto", _("Automatic (%s)") % (swaputil.zram_best_algorithm(algos) or "-"))] + [(a, a) for a in algos]
			if cfg.zram_algo.value not in dict(algoChoices):
				algoChoices.append((cfg.zram_algo.value, cfg.zram_algo.value))
			self.options.append({
				"title": _("zram compression"),
				"help": _("Compression algorithm for the compressed RAM swap. lz4 is fastest, zstd compresses best but needs more CPU. A change takes effect the next time zram is set up."),
				"choices": algoChoices,
				"value": cfg.zram_algo.value,
				"config": cfg.zram_algo,
			})
			if cfg.zram_size.value:
				self.options.append({
					"title": _("zram at startup"),
					"help": _("Set up the compressed RAM swap (%s) every time the receiver starts.") % swaputil.human_kb(cfg.zram_size.value * 1024),
					"choices": [(True, _("On")), (False, _("Off"))],
					"value": cfg.zram_autostart.value,
					"config": cfg.zram_autostart,
				})
		self.options += [
			{
				"title": _("Check for updates"),
				"help": _("When the plugin is opened, it asks GitHub at most once a day whether a new version exists, and shows a hint at the top. Only your IP address is transmitted; nothing is installed automatically. Downloads: %s") % swaputil.RELEASES_URL.replace("https://", ""),
				"choices": [(True, _("On")), (False, _("Off"))],
				"value": cfg.update_check.value,
				"config": cfg.update_check,
			},
			{
				"title": _("Show plugin in"),
				"help": _("Where Simple Swap Manager can be opened. A change takes effect after restarting the GUI."),
				"choices": [("both", _("Plugins and storage menu")), ("plugins", _("Plugin browser only"))],
				"value": cfg.menu.value,
				"config": cfg.menu,
			},
			{
				"title": _("System information"),
				"help": _("Shows what this receiver supports: kernel, zram, zswap and drives. Press OK to open."),
				"choices": [("open", _("Open"))],
				"value": "open",
				"config": None,
				"action": self.openInfo,
			},
			{
				"title": _("Uninstall plugin..."),
				"help": _("Removes Simple Swap Manager from this receiver. You can choose whether the swap space is kept or deleted."),
				"choices": [("go", _("Uninstall"))],
				"value": "go",
				"config": None,
				"action": self.uninstall,
				"color": C_RED_TEXT,
			},
		]
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions"], {
			"ok": lambda: self.change(1),
			"cancel": self.close,
			"red": self.close,
			"green": self.save,
			"up": self.up,
			"down": self.down,
			"left": lambda: self.change(-1),
			"right": lambda: self.change(1),
		}, -1)
		self.onLayoutFinish.append(self.build)

	def build(self):
		self.setTitle(self["title"].getText())
		idx = self["list"].index()
		rows = []
		for i, o in enumerate(self.options):
			label = dict(o["choices"]).get(o["value"], o["value"])
			rows.append([i,
				_text(24, 0, 600, 85, 0, o["title"]),
				_text(620, 0, 520, 85, 1, label if o["config"] is None else u"\u2039  %s  \u203A" % label,
					color=o.get("color", C_ACCENT), flags=RT_HALIGN_RIGHT | RT_VALIGN_CENTER),
			])
		self["list"].setList(rows)
		self["list"].moveToIndex(idx)
		self.updateHelp()

	def updateHelp(self):
		self["help"].setText(self.options[self["list"].index()]["help"])

	def up(self):
		self["list"].moveUp()
		self.updateHelp()

	def down(self):
		self["list"].moveDown()
		self.updateHelp()

	def openInfo(self):
		self.session.open(SwapInfoScreen)

	# -- uninstall ----------------------------------------------------

	def uninstall(self):
		cfg = config.plugins.simpleswapmanager
		bootfile = cfg.bootfile.value
		# swap files and an active zram; partitions are not ours
		self.uninstallSwaps = [s for s in swaputil.list_swaps((bootfile,) if bootfile else ())
			if s["type"] == "file" or (s["type"] == "zram" and s["active"])]
		title = _("Uninstall Simple Swap Manager")
		if not self.uninstallSwaps:
			openConfirm(self.session, lambda yes: yes and self.doUninstall(False), title,
				_("Simple Swap Manager will be removed from this receiver."), _("Uninstall"), default="no")
			return
		names = []
		for s in self.uninstallSwaps:
			if s["type"] == "zram":
				names.append(u"\u2022  " + _("Compressed RAM (zram)"))
			else:
				names.append(u"\u2022  %s (%s)" % (s["path"], swaputil.human_kb(s["size_kb"])))
		items = [
			("keep", _("Keep swap space"), _("Stays active until the next restart, then it is no longer used")),
			("delete", _("Delete swap space"), _("Deactivate now and free the disk space")),
			("cancel", _("Cancel"), ""),
		]
		self.session.openWithCallback(self.uninstallChosen, SwapSelectScreen, title,
			_("What should happen to the swap space?") + "\n" + "\n".join(names), items, "keep")

	def uninstallChosen(self, key):
		if key == "keep":
			self.doUninstall(False)
		elif key == "delete":
			# all swap spaces are switched off one after another: the RAM must hold everything
			used = sum(s["used_kb"] for s in self.uninstallSwaps if s["active"])
			if not swaputil.can_swapoff({"active": True, "used_kb": used}):
				openMessage(self.session, _("Not enough free memory"),
					_("%s are currently stored in this swap space, but there is not enough free RAM to take it back. Close some plugins or restart the GUI first.") % swaputil.human_kb(used))
				return
			self.doUninstall(True)

	def doUninstall(self, deleteSwap):
		cfg = config.plugins.simpleswapmanager
		steps = []
		if deleteSwap:
			for s in self.uninstallSwaps:
				q = swaputil.shell_quote(s["path"])
				if s["type"] == "zram":
					steps.append({"label": _("Moving data back to RAM..."), "cmd": swaputil.zram_stop_cmd(os.path.basename(s["path"]))})
					continue
				if s["active"]:
					steps.append({"label": _("Moving data back to RAM..."), "cmd": "swapoff %s" % q})
				steps.append({"label": _("Deleting swap file..."), "cmd": "rm -f %s" % q})
			# a clean removal: back to the defaults, enigma2 then drops the entries from its settings
			for item in (cfg.bootfile, cfg.swappiness, cfg.zram_size, cfg.zram_autostart, cfg.zram_algo, cfg.menu,
					cfg.update_check, cfg.update_asked, cfg.update_last, cfg.update_latest):
				item.value = item.default
				item.save()
			configfile.save()
		try:
			cmd = swaputil.uninstall_cmd(os.path.dirname(os.path.abspath(__file__)))
		except ValueError as e:
			openMessage(self.session, _("Error"), str(e))
			return
		steps.append({"label": _("Removing plugin..."), "cmd": cmd})

		def finished(result):
			ok, msg = result if result else (False, "")
			if ok:
				self.close("uninstalled")
		self.session.openWithCallback(finished, SwapTaskScreen, _("Uninstall Simple Swap Manager"), steps,
			False, _("Simple Swap Manager has been removed."))

	def change(self, direction):
		o = self.options[self["list"].index()]
		if o.get("action"):
			if direction == 1:
				o["action"]()
			return
		if o["config"] is None:
			return
		keys = [k for k, v in o["choices"]]
		try:
			i = keys.index(o["value"])
		except ValueError:
			i = 0
		o["value"] = keys[(i + direction) % len(keys)]
		self.build()

	def save(self):
		for o in self.options:
			if o["config"] is None:
				continue
			o["config"].value = o["value"]
			o["config"].save()
		cfg = config.plugins.simpleswapmanager
		if not cfg.update_asked.value and cfg.update_check.value:
			cfg.update_asked.value = True  # switched on in the settings: no need to ask any more
			cfg.update_asked.save()
		if cfg.swappiness.value != "system":
			swaputil.set_swappiness(cfg.swappiness.value)
		configfile.save()
		self.close(True)


# ---------------------------------------------------------------- main screen

class SwapManagerScreen(Screen):
	skin = scaleSkin("""
	<screen name="SimpleSwapManager" position="center,center" size="1300,960" flags="wfNoBorder" backgroundColor="$bg$">
		<eLabel position="0,0" size="1300,960" backgroundColor="$bg$" zPosition="-1" />
		<eLabel position="0,0" size="1300,6" backgroundColor="$accent$" zPosition="1" />
		<widget name="title" position="40,26" size="900,60" font="Regular;44" foregroundColor="$text$" backgroundColor="$bg$" transparent="1" />
		<widget name="version" position="940,40" size="320,40" font="Regular;24" halign="right" foregroundColor="$muted$" backgroundColor="$bg$" transparent="1" />
		<widget name="update" position="440,40" size="720,40" font="Regular;24" halign="right" foregroundColor="$accent$" backgroundColor="$bg$" transparent="1" />

		<eLabel position="40,110" size="1220,330" backgroundColor="$card$" zPosition="0" />
		<widget name="ram_label" position="70,130" size="155,50" font="Regular;30" foregroundColor="$text$" backgroundColor="$card$" transparent="1" valign="center" zPosition="1" />
		""" + barSkin("ram", 240, 145, 620, 20, "accent") + """
		<widget name="ram_value" position="880,130" size="350,50" font="Regular;26" halign="right" foregroundColor="$text$" backgroundColor="$card$" transparent="1" valign="center" zPosition="1" />
		<widget name="swap_label" position="70,190" size="155,50" font="Regular;30" foregroundColor="$text$" backgroundColor="$card$" transparent="1" valign="center" zPosition="1" />
		""" + barSkin("swap", 240, 205, 620, 20, "purple") + """
		<widget name="swap_value" position="880,190" size="350,50" font="Regular;26" halign="right" foregroundColor="$text$" backgroundColor="$card$" transparent="1" valign="center" zPosition="1" />
		<widget name="total_label" position="70,250" size="155,50" font="Regular;30" foregroundColor="$text$" backgroundColor="$card$" transparent="1" valign="center" zPosition="1" />
		""" + stackBarSkin("total", 240, 265, 620, 20, "accent", "purple") + """
		<widget name="total_value" position="880,250" size="350,50" font="Regular;26" halign="right" foregroundColor="$text$" backgroundColor="$card$" transparent="1" valign="center" zPosition="1" />
		<widget name="cpu_label" position="70,310" size="155,50" font="Regular;30" foregroundColor="$text$" backgroundColor="$card$" transparent="1" valign="center" zPosition="1" />
		""" + barSkin("cpu", 240, 325, 620, 20, "green") + """
		<widget name="cpu_value" position="880,310" size="350,50" font="Regular;26" halign="right" foregroundColor="$text$" backgroundColor="$card$" transparent="1" valign="center" zPosition="1" />
		<widget name="info" position="70,376" size="1160,44" font="Regular;24" foregroundColor="$muted$" backgroundColor="$card$" transparent="1" valign="center" zPosition="1" />

		<widget name="section" position="40,465" size="320,44" font="Regular;28" foregroundColor="$accent$" backgroundColor="$bg$" transparent="1" valign="center" />
		<widget name="swapio" position="360,465" size="900,44" font="Regular;24" halign="right" foregroundColor="$muted$" backgroundColor="$bg$" transparent="1" valign="center" />
		<widget name="status" position="360,465" size="900,44" font="Regular;24" halign="right" foregroundColor="$green$" backgroundColor="$bg$" transparent="1" valign="center" zPosition="1" />
		<widget name="list" position="40,520" size="1220,320" scrollbarMode="showOnDemand" backgroundColor="$bg$" backgroundColorSelected="$sel$" foregroundColor="$text$" foregroundColorSelected="$text$" />
		<widget name="empty" position="40,540" size="1220,280" font="Regular;30" halign="center" valign="center" foregroundColor="$muted$" backgroundColor="$bg$" transparent="1" zPosition="3" />

		<eLabel position="40,858" size="1220,2" backgroundColor="$line$" />
		""" + footerSkin(870, 1220) + """
		<widget name="hint" position="40,920" size="1220,34" font="Regular;22" foregroundColor="$muted$" backgroundColor="$bg$" transparent="1" valign="center" />
	</screen>""")

	def __init__(self, session, version="1.0"):
		Screen.__init__(self, session)
		self.skinName = "SimpleSwapManager"
		self.cfg = config.plugins.simpleswapmanager
		self.swaps = []
		self["title"] = Label(_("Simple Swap Manager"))
		self.version = version
		self.closed = False
		self["version"] = Label("v%s" % version)
		self["update"] = Label("")
		self["ram_label"] = Label(_("RAM"))
		self["swap_label"] = Label(_("Swap"))
		self["ram_value"] = Label("")
		self["swap_value"] = Label("")
		self["total_label"] = Label(_("Total"))
		self["total_value"] = Label("")
		self["cpu_label"] = Label(_("CPU"))
		self["cpu_value"] = Label(u"\u2013")
		self["info"] = Label("")
		self["section"] = Label(_("Swap spaces"))
		self["status"] = Label("")
		self["swapio"] = Label("")
		self["empty"] = Label(_("No swap space found.\nPress YELLOW to create a swap file."))
		self["hint"] = Label(_("OK  Options     MENU  Settings     INFO  System info     EXIT  Close"))
		KeyLabel(self, "red")
		KeyLabel(self, "green")
		KeyLabel(self, "yellow", _("Create"))
		KeyLabel(self, "blue", _("Settings"))
		self["list"] = ModernList(itemHeight=106)
		self.ramBar = Bar(self, "ram")
		self.swapBar = Bar(self, "swap")
		self.totalBar = StackBar(self, "total")
		self.cpuBar = Bar(self, "cpu")
		self.cpuColor = None
		self.cpuPrev = swaputil.read_cpu_times()
		self.ioPrev = swaputil.read_swap_io()
		self.ioTime = time.time()
		self.cpuFreq = swaputil.cpu_freq_mhz()

		self["infoActions"] = ActionMap(["InfoActions"], {"info": self.openInfo}, -1)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "MenuActions"], {
			"ok": self.options,
			"cancel": self.close,
			"red": self.deleteSwap,
			"green": self.toggleSwap,
			"yellow": self.createSwap,
			"blue": self.openSettings,
			"menu": self.openSettings,
			"up": self.up,
			"down": self.down,
			"left": self.pageUp,
			"right": self.pageDown,
		}, -1)

		self.refreshTimer = eTimer()
		self.statusTimer = eTimer()
		self.askTimer = eTimer()
		try:
			self.refreshTimer.callback.append(self.refresh)
			self.statusTimer.callback.append(self.clearStatus)
			self.askTimer.callback.append(self.askUpdateCheck)
		except AttributeError:
			self._c1 = self.refreshTimer.timeout.connect(self.refresh)
			self._c2 = self.statusTimer.timeout.connect(self.clearStatus)
			self._c3 = self.askTimer.timeout.connect(self.askUpdateCheck)
		self.onLayoutFinish.append(self.firstShow)
		self.onClose.append(self.stopTimers)

	# -- helpers ------------------------------------------------------

	def firstShow(self):
		self.setTitle(_("Simple Swap Manager"))
		self.cpuBar.set(0)  # the skin draws the fill full width until the first sample
		self.refresh()
		self.refreshTimer.start(3000, False)
		recent = swaputil.oom_this_boot(swaputil.update_oom_history())
		if recent:
			self.setStatus(_("Out of memory %d times since start - INFO for details") % len(recent), error=True)
		self.checkUpdate()

	def askUpdateCheck(self):
		"""Ask once whether the plugin may look for updates; nothing is sent before a yes."""
		self.askTimer.stop()
		if self.closed or self.cfg.update_asked.value:
			return
		items = [
			("yes", _("Yes, check for updates"), _("At most once a day, when the plugin is opened")),
			("no", _("No"), _("Can be switched on later in the settings")),
		]
		self.session.openWithCallback(self.updateCheckAnswered, SwapSelectScreen, _("Check for updates?"),
			_("Simple Swap Manager can ask GitHub whether a new version is available. Only the IP address of this receiver is transmitted; nothing is installed automatically.\nThis can be changed at any time in the settings."),
			items, "yes")

	def updateCheckAnswered(self, key):
		if key not in ("yes", "no"):
			return  # EXIT: no decision yet, ask again next time
		self.cfg.update_check.value = key == "yes"
		self.cfg.update_check.save()
		self.cfg.update_asked.value = True
		self.cfg.update_asked.save()
		configfile.save()
		self.checkUpdate()

	def checkUpdate(self):
		"""Show a hint when GitHub has a newer release (at most one request a day)."""
		if not self.cfg.update_asked.value:
			self.askTimer.start(200, True)  # open the question once this screen is shown
			return
		if not self.cfg.update_check.value:
			return
		self.showUpdate(self.cfg.update_latest.value)
		try:
			last = float(self.cfg.update_last.value or 0)
		except ValueError:
			last = 0
		if not swaputil.update_check_due(last):
			return
		try:
			from twisted.internet import threads
		except ImportError:
			return
		# remember the attempt right away: no new request on every open while GitHub is unreachable
		self.cfg.update_last.value = "%d" % time.time()
		self.cfg.update_last.save()
		configfile.save()
		threads.deferToThread(swaputil.fetch_latest_version, self.version).addCallback(self.updateChecked)

	def updateChecked(self, latest):
		if not latest:
			return
		if latest != self.cfg.update_latest.value:
			self.cfg.update_latest.value = latest
			self.cfg.update_latest.save()
			configfile.save()
		if not self.closed:  # the screen may have been closed meanwhile
			self.showUpdate(latest)

	def showUpdate(self, latest):
		self["update"].setText(_("Update available: v%s") % latest if swaputil.is_newer(latest, self.version) else "")

	def stopTimers(self):
		self.closed = True
		self.askTimer.stop()
		self.refreshTimer.stop()
		self.statusTimer.stop()

	def setStatus(self, text, error=False):
		self["status"].setText(text)
		self["swapio"].hide()
		inst = self["status"].instance
		if inst:
			from enigma import gRGB
			inst.setForegroundColor(gRGB(C_RED if error else C_GREEN))
		self.statusTimer.start(6000, True)

	def clearStatus(self):
		self["status"].setText("")
		self["swapio"].show()

	def current(self):
		cur = self["list"].getCurrent()
		if not cur:
			return None
		for s in self.swaps:
			if s["path"] == cur[0]:
				return s
		return None

	def up(self):
		self["list"].moveUp()
		self.updateKeys()

	def down(self):
		self["list"].moveDown()
		self.updateKeys()

	def pageUp(self):
		self["list"].pageUpList()
		self.updateKeys()

	def pageDown(self):
		self["list"].pageDownList()
		self.updateKeys()

	# -- display ------------------------------------------------------

	def refresh(self):
		mi = swaputil.read_meminfo()
		total = mi.get("MemTotal", 0)
		avail = mi.get("MemAvailable", 0)
		used = max(0, total - avail)
		self.ramBar.set(float(used) / total if total else 0)
		self["ram_value"].setText(_("%s of %s used") % (swaputil.human_kb(used), swaputil.human_kb(total)))

		bootfile = self.cfg.bootfile.value
		zsize = self.cfg.zram_size.value if swaputil.zram_supported() else 0
		self.swaps = swaputil.list_swaps((bootfile,) if bootfile else (), zsize)
		stotal = sum(s["size_kb"] for s in self.swaps if s["active"])
		sused = sum(s["used_kb"] for s in self.swaps if s["active"])
		self.swapBar.set(float(sused) / stotal if stotal else 0)
		if stotal:
			self["swap_value"].setText(_("%s of %s used") % (swaputil.human_kb(sused), swaputil.human_kb(stotal)))
		else:
			self["swap_value"].setText(_("not active"))

		# RAM + swap = memory the programs can really use
		vtotal = total + stotal
		self.totalBar.set(float(used) / vtotal if vtotal else 0, float(sused) / vtotal if vtotal else 0)
		self["total_value"].setText(_("%s of %s used") % (swaputil.human_kb(used + sused), swaputil.human_kb(vtotal)))

		sw = swaputil.get_swappiness()
		parts = [_("Swappiness: %d") % sw]
		if bootfile:
			parts.append(_("Startup: %s") % bootfile)
		else:
			parts.append(_("Startup: off"))
		if zsize and self.cfg.zram_autostart.value:
			parts.append(_("zram: %s") % swaputil.human_kb(self.cfg.zram_size.value * 1024))
		self.updateCpu()
		self["info"].setText(u"   ·   ".join(parts))
		self.buildList()

	def updateCpu(self):
		"""CPU load, clock, temperature and swap activity since the last sample."""
		cur = swaputil.read_cpu_times()
		now = time.time()
		if not cur or not self.cpuPrev or cur[1] - self.cpuPrev[1] < 50:
			return  # too short since the last sample (e.g. refresh after a key press)
		usage = swaputil.cpu_usage(self.cpuPrev, cur)
		self.cpuPrev = cur
		if usage is not None:
			self.cpuBar.set(usage)
			color = C_GREEN if usage < 0.7 else (C_YELLOW if usage < 0.9 else C_RED)
			fill = self["cpu_fill"].instance
			if fill and color != self.cpuColor:
				from enigma import gRGB
				try:
					fill.setBackgroundColor(gRGB(color))
					fill.invalidate()
				except Exception as e:
					print("[SimpleSwapManager] cpu bar color: %s" % e)
				self.cpuColor = color
			parts = [u"%d %%" % int(round(usage * 100))]
			freq = swaputil.cpu_freq_mhz() or self.cpuFreq
			if freq >= 1000:
				parts.append(u"%.1f GHz" % (freq / 1000.0))
			elif freq:
				parts.append(u"%d MHz" % freq)
			temp = swaputil.cpu_temperature()
			if temp is not None:
				parts.append(u"%d \u00b0C" % temp)
			self["cpu_value"].setText(u"  ·  ".join(parts))
		io = swaputil.read_swap_io()
		dt = now - self.ioTime
		if io and self.ioPrev and dt > 0:
			kb = swaputil.page_size() / 1024.0 / dt
			text = _("Swap in: %s/s, out: %s/s") % (
				swaputil.human_rate_kb((io[0] - self.ioPrev[0]) * kb),
				swaputil.human_rate_kb((io[1] - self.ioPrev[1]) * kb))
			if any(s["active"] for s in self.swaps):
				# total swapped out since boot = what the swap space really had to write (wear)
				text += u"   ·   " + _("Written since boot: %s") % swaputil.human_bytes(io[1] * swaputil.page_size())
			self["swapio"].setText(text)
		self.ioPrev = io
		self.ioTime = now

	def buildList(self):
		idx = self["list"].index()
		bootfile = self.cfg.bootfile.value
		rows = []
		for s in self.swaps:
			if s["type"] == "zram":
				rows.append(self.zramRow(s))
				continue
			if s["type"] == "partition":
				kind = _("Swap partition")
			else:
				m = swaputil.mount_of(s["path"])
				kind = _("Swap file")
				if m:
					kind = u"%s  ·  %s" % (kind, kindName(swaputil.device_kind(m["device"], m["mount"])))
			detail = u"%s  ·  %s" % (swaputil.human_kb(s["size_kb"]), kind)
			if s["active"]:
				detail += u"  ·  " + _("%s used") % swaputil.human_kb(s["used_kb"])
			row = [s["path"],
				_text(24, 8, 740, 48, 0, s["path"]),
				_text(24, 56, 740, 40, 3, detail, color=C_MUTED),
				_pill(990, 33, 200, _("ACTIVE") if s["active"] else _("INACTIVE"), C_GREEN if s["active"] else C_TRACK),
			]
			if s["path"] == bootfile:
				row.append(_pill(774, 33, 200, _("STARTUP"), C_BLUE))
			rows.append(row)
		self["list"].setList(rows)
		if rows:
			self["list"].moveToIndex(min(idx, len(rows) - 1))
			self["list"].show()
			self["empty"].hide()
		else:
			self["list"].hide()
			self["empty"].setText(self.emptyText())
			self["empty"].show()
		self.updateKeys()

	def emptyText(self):
		"""Hint when there is no swap yet - mention it if no external drive is mounted."""
		if any(l["kind"] != "flash" for l in swaputil.find_locations()):
			return _("No swap space found.\nPress YELLOW to create a swap file.")
		if swaputil.zram_supported():
			return _("No swap space found.\nNo external drive with a Linux file system (ext4, ...) is mounted - press YELLOW for compressed RAM (zram).")
		return _("No swap space found.\nNo external drive with a Linux file system (ext4, ...) is mounted. Connect a USB drive or hard disk and mount it in the image's drive settings.")

	def zramRow(self, s):
		parts = [swaputil.human_kb(s["size_kb"])]
		st = swaputil.zram_stats() if s["active"] else None
		if st:
			if st["algo"]:
				parts.append(st["algo"])
			parts.append(_("%s used") % swaputil.human_kb(s["used_kb"]))
			if st["mem_kb"]:
				parts.append(_("%s RAM") % swaputil.human_kb(st["mem_kb"]))
			ratio = swaputil.zram_ratio(st)
			if ratio:
				parts.append(_("ratio %.1f:1") % ratio)
		else:
			parts.append(_("compressed swap in RAM"))
		row = [s["path"],
			_text(24, 8, 740, 48, 0, _("Compressed RAM (zram)")),
			_text(24, 56, 740, 40, 3, u"  \u00B7  ".join(parts), color=C_MUTED),
			_pill(990, 33, 200, _("ACTIVE") if s["active"] else _("INACTIVE"), C_GREEN if s["active"] else C_TRACK),
		]
		if self.zramIsOurs(s) and self.cfg.zram_autostart.value:
			row.append(_pill(774, 33, 200, _("STARTUP"), C_BLUE))
		return row

	def zramIsOurs(self, s):
		return s["type"] == "zram" and s["path"] == swaputil.zram_path() and self.cfg.zram_size.value > 0

	def updateKeys(self):
		s = self.current()
		if s is None:
			self["key_red"].setText("")
			self["key_green"].setText("")
			return
		self["key_green"].setText(_("Deactivate") if s["active"] else _("Activate"))
		if s["type"] == "file":
			self["key_red"].setText(_("Delete"))
		elif s["type"] == "zram":
			self["key_red"].setText(_("Remove"))
		else:
			self["key_red"].setText("")

	# -- actions ------------------------------------------------------

	def runTask(self, title, steps, doneText, autoClose=True):
		def finished(result):
			ok, msg = result if result else (False, "")
			self.refresh()
			if ok:
				self.setStatus(doneText)
			elif msg:
				self.setStatus(msg, error=True)
		self.session.openWithCallback(finished, SwapTaskScreen, title, steps, autoClose)

	def options(self):
		s = self.current()
		if s is None:
			self.createSwap()
			return
		items = []
		if s["active"]:
			items.append(("toggle", _("Deactivate"), _("Stop using this swap space now")))
		else:
			items.append(("toggle", _("Activate"), _("Start using this swap space now")))
		if s["type"] == "zram":
			if self.zramIsOurs(s) and self.cfg.zram_autostart.value:
				items.append(("boot", _("Don't activate at startup"), _("Remove automatic activation")))
			else:
				items.append(("boot", _("Activate at startup"), _("Set up the compressed RAM swap every time the receiver starts")))
			items.append(("delete", _("Remove"), _("Deactivate zram and give the memory back")))
			items.append(("zram", _("Change size"), _("Set up zram again with a different size")))
		if s["type"] == "file":
			if self.cfg.bootfile.value == s["path"]:
				items.append(("boot", _("Don't activate at startup"), _("Remove automatic activation")))
			else:
				items.append(("boot", _("Activate at startup"), _("Use this swap file every time the receiver starts")))
			items.append(("resize", _("Change size"), _("Create the swap file again with a different size")))
			items.append(("delete", _("Delete"), _("Remove the swap file and free the disk space")))
		items.append(("create", _("Create new swap file"), ""))
		items.append(("info", _("System information"), _("What this receiver supports")))
		title = _("Compressed RAM (zram)") if s["type"] == "zram" else s["path"]
		self.session.openWithCallback(self.optionChosen, SwapSelectScreen, title,
			self.describe(s), items)

	def describe(self, s):
		lines = [_("Size: %s") % swaputil.human_kb(s["size_kb"])]
		if s["type"] == "zram":
			st = swaputil.zram_stats() if s["active"] else None
			if st:
				lines.append(_("Stored: %s, compressed to %s (%s RAM in use)") % (
					swaputil.human_kb(st["orig_kb"]), swaputil.human_kb(st["compr_kb"]), swaputil.human_kb(st["mem_kb"])))
				if st["algo"]:
					lines.append(_("Algorithm: %s, priority %d") % (st["algo"], s["prio"]))
			else:
				lines.append(_("Status: inactive"))
			return "\n".join(lines)
		if s["active"]:
			lines.append(_("Used: %s, priority %d") % (swaputil.human_kb(s["used_kb"]), s["prio"]))
		else:
			lines.append(_("Status: inactive"))
		return "\n".join(lines)

	def optionChosen(self, key):
		if key == "toggle":
			self.toggleSwap()
		elif key == "boot":
			self.toggleBoot()
		elif key == "delete":
			self.deleteSwap()
		elif key == "create":
			self.createSwap()
		elif key == "zram":
			self.chooseZramSize()
		elif key == "resize":
			self.resizeSwap()
		elif key == "info":
			self.openInfo()

	def toggleBoot(self):
		s = self.current()
		if s is not None and s["type"] == "zram":
			if self.zramIsOurs(s) and self.cfg.zram_autostart.value:
				self.cfg.zram_autostart.value = False
				msg = _("Startup activation disabled")
			else:
				if not self.cfg.zram_size.value:
					self.cfg.zram_size.value = max(64, s["size_kb"] // 1024)
					self.cfg.zram_size.save()
				self.cfg.zram_autostart.value = True
				msg = _("Activated at every startup")
			self.cfg.zram_autostart.save()
			configfile.save()
			self.refresh()
			self.setStatus(msg)
			return
		if s is None or s["type"] != "file":
			return
		if self.cfg.bootfile.value == s["path"]:
			self.cfg.bootfile.value = ""
			msg = _("Startup activation disabled")
		else:
			self.cfg.bootfile.value = s["path"]
			msg = _("Activated at every startup")
		self.cfg.bootfile.save()
		configfile.save()
		self.refresh()
		self.setStatus(msg)

	def toggleSwap(self):
		s = self.current()
		if s is None:
			return
		q = swaputil.shell_quote(s["path"])
		if s["type"] == "zram" and not s["active"]:
			size = s["size_kb"] // 1024
			self.runTask(_("Activate swap"), [{"label": _("Setting up compressed RAM swap..."),
				"cmd": swaputil.zram_setup_cmd(size, self.zramAlgo())}], _("Swap activated"))
			return
		if s["active"]:
			if not swaputil.can_swapoff(s):
				openMessage(self.session, _("Not enough free memory"),
					_("%s are currently stored in this swap space, but there is not enough free RAM to take it back. Close some plugins or restart the GUI first.") % swaputil.human_kb(s["used_kb"]))
				return
			cmd = swaputil.zram_stop_cmd(os.path.basename(s["path"])) if s["type"] == "zram" else "swapoff %s" % q
			self.runTask(_("Deactivate swap"), [{"label": _("Moving data back to RAM..."), "cmd": cmd}], _("Swap deactivated"))
		else:
			if s["type"] == "file" and not swaputil.is_swap_file(s["path"]):
				openMessage(self.session, _("Error"), _("The file is not a valid swap file."))
				return
			self.runTask(_("Activate swap"), [{"label": _("Activating swap..."), "cmd": "chmod 600 %s 2>/dev/null; swapon %s" % (q, q)}], _("Swap activated"))

	def deleteSwap(self):
		s = self.current()
		if s is not None and s["type"] == "zram":
			self.removeZram(s)
			return
		if s is None or s["type"] != "file":
			return
		if s["active"] and not swaputil.can_swapoff(s):
			openMessage(self.session, _("Not enough free memory"),
				_("%s are currently stored in this swap space, but there is not enough free RAM to take it back. Close some plugins or restart the GUI first.") % swaputil.human_kb(s["used_kb"]))
			return

		def confirmed(yes):
			if not yes:
				return
			q = swaputil.shell_quote(s["path"])
			steps = []
			if s["active"]:
				steps.append({"label": _("Moving data back to RAM..."), "cmd": "swapoff %s" % q})
			steps.append({"label": _("Deleting swap file..."), "cmd": "rm -f %s" % q})
			if self.cfg.bootfile.value == s["path"]:
				self.cfg.bootfile.value = ""
				self.cfg.bootfile.save()
				configfile.save()
			self.runTask(_("Delete swap file"), steps, _("Swap file deleted"))

		openConfirm(self.session, confirmed, _("Delete swap file?"),
			_("%s (%s) will be deactivated and deleted.") % (s["path"], swaputil.human_kb(s["size_kb"])),
			_("Delete"), default="no")

	def openSettings(self):
		self.session.openWithCallback(self.settingsClosed, SwapSettingsScreen)

	def settingsClosed(self, result=None):
		if result != "uninstalled":
			self.refresh()
			if self.cfg.update_check.value:
				self.checkUpdate()
			else:
				self["update"].setText("")
			return
		self.stopTimers()

		def restart(yes):
			if yes:
				from Screens.Standby import TryQuitMainloop
				# warns about running recordings; if the restart is declined we just close
				self.session.openWithCallback(lambda *args: self.close(), TryQuitMainloop, 3)
			else:
				self.close()
		openConfirm(self.session, restart, _("Restart GUI?"),
			_("The plugin is unloaded completely after restarting the GUI. Restart now?"),
			_("Restart now"), _("Later"))

	def openInfo(self):
		self.session.open(SwapInfoScreen)

	# -- create wizard ------------------------------------------------

	def createSwap(self):
		self.locations = swaputil.find_locations()
		zram = swaputil.zram_supported()
		if not self.locations and not zram:
			openMessage(self.session, _("No suitable storage"),
				_("No storage device with a Linux file system (ext2/3/4, xfs, ...) was found.\nSwap files cannot be created on FAT, exFAT, NTFS or network drives."))
			return
		bootfile = self.cfg.bootfile.value
		existing = dict((s["path"], s) for s in swaputil.list_swaps((bootfile,) if bootfile else ()) if s["type"] == "file")
		items = []
		if zram:
			items.append(("zram", _("Compressed RAM (zram)"), _("No drive needed  \u00B7  fastest  \u00B7  uses a little CPU"), _("FASTEST"), C_PURPLE))
		else:
			items.append(("zram_unsupported", _("Compressed RAM (zram)"), _("Not available on this receiver - press OK for details"), _("NOT SUPPORTED"), C_TRACK))
		for i, l in enumerate(self.locations):
			detail = u"%s  ·  %s  ·  %s" % (kindName(l["kind"]), l["fstype"], _("%s free") % swaputil.human_bytes(l["free"]))
			badge, color = None, C_ACCENT
			if l["kind"] == "flash":  # soldered in: if it wears out, the receiver itself is affected
				badge, color = _("NOT RECOMMENDED"), C_ORANGE
			elif l["kind"] == "sd":  # wears out too, but can be replaced
				badge, color = _("NOT IDEAL"), C_YELLOW
			elif i == 0:
				badge, color = _("RECOMMENDED"), C_GREEN
			if swaputil.max_size_mb(l["free"]) < swaputil.MIN_SIZE_MB:
				badge, color = _("FULL"), C_RED
			l["existing"] = existing.get(l["path"])
			if l["existing"]:  # one swap file per drive: choosing it again means changing its size
				detail = u"%s  ·  %s  ·  %s" % (kindName(l["kind"]), l["fstype"], _("swap file %s") % swaputil.human_kb(l["existing"]["size_kb"]))
				badge, color = _("EXISTS"), C_BLUE
			items.append((i, l["mount"], detail, badge, color))
		msg = _("Where should the swap file be stored?\nA hard disk or USB drive is best; internal flash wears out faster.")
		if zram:
			msg = _("Where should the swap space be created?\nzram compresses memory inside the RAM; it can be combined with a swap file on a drive.")
		if any(l.get("existing") for l in self.locations):
			msg += "\n" + _("A drive marked %s already has a swap file; choosing it changes the size.") % _("EXISTS")
		self.session.openWithCallback(self.locationChosen, SwapSelectScreen, _("Create swap file  1/2"), msg, items)

	def locationChosen(self, idx):
		if idx is None:
			return
		if idx == "zram":
			self.chooseZramSize()
			return
		if idx == "zram_unsupported":
			reason = swaputil.zram_status()[1]
			openMessage(self.session, _("zram not supported"),
				zramReasonText(reason, swaputil.system_info()["kernel"]),
				callback=self.createSwap)
			return
		loc = self.locations[idx]
		if loc.get("existing"):
			self.resizeSwap(loc["existing"])
			return
		if swaputil.max_size_mb(loc["free"]) < swaputil.MIN_SIZE_MB:
			openMessage(self.session, _("Not enough space"), _("There is not enough free space on %s.") % loc["mount"])
			return
		if loc["kind"] == "flash":
			def ok(yes):
				if yes:
					self.chooseSize(loc)
			openConfirm(self.session, ok, _("Use internal flash?"),
				_("Swapping to the internal flash memory causes many write cycles and may shorten its life. A USB drive or hard disk is recommended.")
				+ "\n" + _("The internal flash is soldered in and cannot be replaced like an SD card or USB drive - if it wears out, the receiver itself is affected."),
				_("Use internal flash anyway"), default="no")
			return
		if loc["kind"] == "sd":
			def okSd(yes):
				if yes:
					self.chooseSize(loc)
			openConfirm(self.session, okSd, _("Use SD card?"),
				_("Swapping writes to the card again and again, so SD cards wear out faster. A USB drive or hard disk is recommended.\nIf you use the card: a low swappiness (10-20) keeps the writes to a minimum."),
				_("Use SD card anyway"), default="no")
			return
		self.chooseSize(loc)

	def resizeSwap(self, s=None):
		"""Recreate a swap file with another size; startup and active state stay as they are."""
		if s is None:
			s = self.current()
		if s is None or s["type"] != "file":
			return
		if s["active"] and not swaputil.can_swapoff(s):
			openMessage(self.session, _("Not enough free memory"),
				_("%s are currently stored in this swap space, but there is not enough free RAM to take it back. Close some plugins or restart the GUI first.") % swaputil.human_kb(s["used_kb"]))
			return
		m = swaputil.mount_of(s["path"])
		if m is None:
			return
		free = swaputil.disk_space(m["mount"])[0] + s["size_kb"] * 1024  # the old file is removed first
		loc = {"mount": m["mount"], "device": m["device"], "fstype": m["fstype"], "path": s["path"],
			"kind": swaputil.device_kind(m["device"], m["mount"]), "free": free, "resize": s}
		self.chooseSize(loc)

	def chooseSize(self, loc):
		self.loc = loc
		mem = swaputil.read_meminfo().get("MemTotal", 0)
		items = []
		rec = None
		for size, isRec in swaputil.size_choices(mem, loc["free"]):
			items.append((size, swaputil.human_kb(size * 1024), "", _("RECOMMENDED") if isRec else None, C_GREEN))
			if isRec:
				rec = size
		items.append(("custom", _("Custom size..."), _("Enter a size between %d and %d MB") % (swaputil.MIN_SIZE_MB, swaputil.max_size_mb(loc["free"]))))
		if loc.get("resize"):
			title = _("Change size")
			msg = _("New size for %s (currently %s):") % (loc["path"], swaputil.human_kb(loc["resize"]["size_kb"]))
			msg += "\n" + _("RAM: %s  ·  available: %s") % (swaputil.human_kb(mem), swaputil.human_bytes(loc["free"]))
		else:
			title = _("Create swap file  2/2")
			msg = _("Select the size of the swap file on %s.\nRAM: %s  ·  free space: %s") % (loc["mount"], swaputil.human_kb(mem), swaputil.human_bytes(loc["free"]))
		self.session.openWithCallback(self.sizeChosen, SwapSelectScreen, title, msg, items, rec)

	def sizeChosen(self, size):
		if size is None:
			return
		if size == "custom":
			from Screens.InputBox import InputBox
			from Components.Input import Input
			self.session.openWithCallback(self.customSize, InputBox, title=_("Swap file size in MB (%d-%d)") % (swaputil.MIN_SIZE_MB, swaputil.max_size_mb(self.loc["free"])),
				text="512", maxSize=False, type=Input.NUMBER)
			return
		self.confirmCreate(int(size))

	def customSize(self, value):
		if value is None:
			return
		try:
			size = int(str(value).strip())
		except ValueError:
			size = 0
		limit = swaputil.max_size_mb(self.loc["free"])
		if size < swaputil.MIN_SIZE_MB or size > limit:
			openMessage(self.session, _("Invalid size"), _("Please enter a size between %d and %d MB.") % (swaputil.MIN_SIZE_MB, limit))
			return
		self.confirmCreate(size)

	def confirmCreate(self, size):
		loc = self.loc
		path = loc["path"]
		existing = None
		for s in swaputil.list_swaps((path,)):
			if s["path"] == path:
				existing = s
		if existing is None and os.path.exists(path):
			openMessage(self.session, _("File exists"), _("%s already exists and is not a swap file. Please remove it first.") % path)
			return
		if existing and existing["active"] and not swaputil.can_swapoff(existing):
			openMessage(self.session, _("Not enough free memory"),
				_("The existing swap file is in use and there is not enough free RAM to replace it."))
			return
		resize = loc.get("resize")
		if resize:
			msg = _("%s will be recreated with %s instead of %s.") % (path, swaputil.human_kb(size * 1024), swaputil.human_kb(resize["size_kb"]))
		else:
			msg = _("A swap file of %s will be created at\n%s\nand activated at every startup.") % (swaputil.human_kb(size * 1024), path)
			if existing:
				msg += "\n" + _("The existing swap file (%s) will be replaced.") % swaputil.human_kb(existing["size_kb"])
		seconds = size // 15
		if seconds > 20:
			msg += "\n" + _("This takes about %d seconds.") % seconds

		def ok(yes):
			if yes:
				self.doCreate(path, size, existing, resize=bool(resize))
		if resize:
			openConfirm(self.session, ok, _("Change size"), msg, _("Change size"))
		else:
			openConfirm(self.session, ok, _("Create swap file?"), msg, _("Create swap file"))

	def doCreate(self, path, size, existing, resize=False):
		q = swaputil.shell_quote(path)

		def removePartial():
			try:
				if os.path.exists(path) and not swaputil.is_swap_file(path):
					os.remove(path)
			except OSError:
				pass

		def removeAfterCancel():
			# dd was killed: the file is incomplete in any case
			try:
				os.remove(path)
			except OSError:
				pass

		steps = []
		if existing:
			if existing["active"]:
				steps.append({"label": _("Deactivating old swap file..."), "cmd": "swapoff %s" % q})
			steps.append({"label": _("Removing old swap file..."), "cmd": "rm -f %s" % q})
		steps.append({
			"label": _("Writing swap file..."),
			# nice + O_DIRECT: does not flood the page cache and keeps the box responsive.
			# IMPORTANT: never 'exec' dd. BusyBox dd moves the output file onto fd 1, which
			# closes the stdout pipe to enigma2; enigma2 then blocks in waitpid() until dd
			# has finished and the whole GUI freezes. The surrounding shell keeps the pipe open.
			"cmd": "nice -n 19 dd if=/dev/zero of=%s bs=1M count=%d oflag=direct 2>&1; exit $?" % (q, size),
			"fallback": "nice -n 19 dd if=/dev/zero of=%s bs=1M count=%d conv=fsync 2>&1; exit $?" % (q, size),
			"progress": (path, size * 1024 * 1024),
			"cancel": True,
			"onCancel": removeAfterCancel,
			"onFail": removeAfterCancel,
		})
		steps.append({"label": _("Formatting swap file..."), "cmd": "chmod 600 %s && mkswap %s" % (q, q), "onFail": removePartial})
		if not resize or existing is None or existing["active"]:
			steps.append({"label": _("Activating swap..."), "cmd": "swapon %s" % q})
		if not resize:  # a new swap file is used at every startup; resizing keeps the setting
			self.cfg.bootfile.value = path
			self.cfg.bootfile.save()
			configfile.save()
		doneText = _("Size changed") if resize else _("Swap file created and activated")

		def finished(result):
			ok, msg = result if result else (False, "")
			if not ok:
				if self.cfg.bootfile.value == path and not swaputil.is_swap_file(path):
					self.cfg.bootfile.value = ""
					self.cfg.bootfile.save()
					configfile.save()
			self.refresh()
			if ok:
				self.setStatus(doneText)
				if not resize and getattr(self, "loc", None) and self.loc.get("kind") == "sd":
					self.offerLowSwappiness()
			elif msg:
				self.setStatus(msg, error=True)
		self.session.openWithCallback(finished, SwapTaskScreen, _("Change size") if resize else _("Create swap file"), steps, False, doneText)

	def offerLowSwappiness(self):
		"""Swap on an SD card: offer swappiness 10 (fewer writes) if it is higher."""
		current = swaputil.get_swappiness()
		if current <= 20:
			return

		def answer(yes):
			if yes:
				self.cfg.swappiness.value = "10"
				self.cfg.swappiness.save()
				configfile.save()
				swaputil.set_swappiness("10")
				self.refresh()
				self.setStatus(_("Swappiness set to %d") % 10)
		openConfirm(self.session, answer, _("Protect the SD card?"),
			_("The swappiness is %d. With 10, the receiver swaps out less often and writes less to the card.") % current,
			_("Set swappiness to 10"), _("Keep %d") % current)

	# -- zram ---------------------------------------------------------

	def zramAlgo(self):
		from .plugin import zramAlgorithm
		return zramAlgorithm()

	def zramEntry(self):
		for e in swaputil.list_swaps(zram_size_mb=self.cfg.zram_size.value):
			if e["path"] == swaputil.zram_path():
				return e
		return None

	def chooseZramSize(self):
		mem = swaputil.read_meminfo().get("MemTotal", 0)
		items = []
		rec = None
		for size, isRec in swaputil.zram_size_choices(mem):
			# with ~2.5:1 compression a full zram needs about 40% of its size in RAM
			items.append((size, swaputil.human_kb(size * 1024), _("needs at most about %s RAM when full") % swaputil.human_kb(size * 1024 * 2 // 5),
				_("RECOMMENDED") if isRec else None, C_GREEN))
			if isRec:
				rec = size
		self.session.openWithCallback(self.zramSizeChosen, SwapSelectScreen, _("Compressed RAM (zram)  2/2"),
			_("Select the size of the compressed swap (RAM: %s).\nThe memory is only used when data is actually swapped out; about half the RAM is a good value.") % swaputil.human_kb(mem),
			items, rec)

	def zramSizeChosen(self, size):
		if size is None:
			return
		size = int(size)
		existing = self.zramEntry()
		if existing and existing["active"] and not swaputil.can_swapoff(existing):
			openMessage(self.session, _("Not enough free memory"),
				_("The existing swap file is in use and there is not enough free RAM to replace it."))
			return
		algo = self.zramAlgo()
		msg = _("A compressed RAM swap of %s will be set up (algorithm: %s) and activated at every startup.") % (
			swaputil.human_kb(size * 1024), algo or _("kernel default"))
		msg += "\n" + _("It is used before swap files on drives.")
		if existing and existing["active"]:
			msg += "\n" + _("The current zram swap (%s) will be replaced.") % swaputil.human_kb(existing["size_kb"])

		def ok(yes):
			if yes:
				self.doZram(size, algo)
		openConfirm(self.session, ok, _("Set up zram?"), msg, _("Set up zram"))

	def doZram(self, size, algo):
		old = (self.cfg.zram_size.value, self.cfg.zram_autostart.value)
		self.cfg.zram_size.value = size
		self.cfg.zram_autostart.value = True
		self.cfg.zram_size.save()
		self.cfg.zram_autostart.save()
		configfile.save()
		steps = [{"label": _("Setting up compressed RAM swap..."), "cmd": swaputil.zram_setup_cmd(size, algo)}]

		def finished(result):
			ok, msg = result if result else (False, "")
			if not ok:
				self.cfg.zram_size.value, self.cfg.zram_autostart.value = old
				self.cfg.zram_size.save()
				self.cfg.zram_autostart.save()
				configfile.save()
			self.refresh()
			if ok:
				self.setStatus(_("zram activated"))
			elif msg:
				self.setStatus(msg, error=True)
		self.session.openWithCallback(finished, SwapTaskScreen, _("Compressed RAM (zram)"), steps, False, _("zram activated"))

	def removeZram(self, s):
		if s["active"] and not swaputil.can_swapoff(s):
			openMessage(self.session, _("Not enough free memory"),
				_("%s are currently stored in this swap space, but there is not enough free RAM to take it back. Close some plugins or restart the GUI first.") % swaputil.human_kb(s["used_kb"]))
			return

		def confirmed(yes):
			if not yes:
				return
			if s["path"] == swaputil.zram_path():
				self.cfg.zram_size.value = 0
				self.cfg.zram_size.save()
				configfile.save()
			if s["active"]:
				self.runTask(_("Remove zram"), [{"label": _("Moving data back to RAM..."),
					"cmd": swaputil.zram_stop_cmd(os.path.basename(s["path"]))}], _("zram removed"))
			else:
				self.refresh()
				self.setStatus(_("zram removed"))

		openConfirm(self.session, confirmed, _("Remove zram?"),
			_("The compressed RAM swap will be deactivated and will no longer be set up at startup."),
			_("Remove"), default="no")
