# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 Paderman
#
# Tests for swaputil (no receiver needed, Python 3 and Python 2.7):
#   python3 -m unittest discover -s tests
#
# Files under /proc and /sys are faked by replacing swaputil._read.

from __future__ import absolute_import, division

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "SimpleSwapManager"))
import swaputil  # noqa: E402


class FakeSys(object):
	"""Replace swaputil._read (and optionally os.path.realpath) with fake files."""

	def __init__(self, files=None, links=None):
		self.files = files or {}
		self.links = links or {}

	def __enter__(self):
		self._read, self._realpath = swaputil._read, os.path.realpath
		swaputil._read = lambda path, default="": self.files.get(path, default)
		real = self._realpath
		os.path.realpath = lambda p: self.links.get(p, real(p))
		return self

	def __exit__(self, *exc):
		swaputil._read, os.path.realpath = self._read, self._realpath
		return False


class Formatting(unittest.TestCase):

	def test_human_kb(self):
		self.assertEqual(swaputil.human_kb(0), "0 MB")
		self.assertEqual(swaputil.human_kb(512 * 1024), "512 MB")
		self.assertEqual(swaputil.human_kb(1536 * 1024), "1.5 GB")

	def test_human_bytes(self):
		self.assertEqual(swaputil.human_bytes(2 * 1024 ** 3), "2.0 GB")

	def test_human_rate_kb(self):
		self.assertEqual(swaputil.human_rate_kb(0), "0 KB")
		self.assertEqual(swaputil.human_rate_kb(12.4), "12 KB")
		self.assertEqual(swaputil.human_rate_kb(3000), "2.9 MB")

	def test_shell_quote(self):
		self.assertEqual(swaputil.shell_quote("/media/hdd/swapfile"), "'/media/hdd/swapfile'")
		self.assertEqual(swaputil.shell_quote("a'b"), "'a'\\''b'")


class Sizes(unittest.TestCase):
	GB = 1024 ** 3

	def test_max_size_keeps_reserve(self):
		self.assertEqual(swaputil.max_size_mb(1024 * 1024 * 1024), 1024 - swaputil.RESERVE_MB)
		self.assertEqual(swaputil.max_size_mb(100 * 1024 * 1024), 0)
		self.assertEqual(swaputil.max_size_mb(500 * self.GB), swaputil.MAX_SIZE_MB)

	def test_recommended_size(self):
		self.assertEqual(swaputil.recommended_size_mb(926 * 1024), 512)
		self.assertEqual(swaputil.recommended_size_mb(2048 * 1024), 1024)
		# never more than the drive can take
		self.assertEqual(swaputil.recommended_size_mb(926 * 1024, 600 * 1024 * 1024), 600 - swaputil.RESERVE_MB)

	def test_size_choices(self):
		choices = swaputil.size_choices(926 * 1024, 50 * self.GB)
		self.assertIn((512, True), choices)
		self.assertEqual(sum(1 for _s, rec in choices if rec), 1)
		self.assertEqual([s for s, _r in choices], sorted(s for s, _r in choices))
		small = swaputil.size_choices(926 * 1024, 700 * 1024 * 1024)
		self.assertTrue(all(s <= 700 - swaputil.RESERVE_MB for s, _r in small))

	def test_zram_size_choices(self):
		choices = swaputil.zram_size_choices(926 * 1024)
		self.assertIn((448, True), choices)
		self.assertTrue(all(s <= 926 for s, _r in choices))


class Swapoff(unittest.TestCase):

	def test_inactive_always_ok(self):
		self.assertTrue(swaputil.can_swapoff({"active": False}))

	def test_needs_free_ram(self):
		entry = {"active": True, "used_kb": 300 * 1024}
		self.assertTrue(swaputil.can_swapoff(entry, {"MemAvailable": 500 * 1024}))
		self.assertFalse(swaputil.can_swapoff(entry, {"MemAvailable": 320 * 1024}))


class Cpu(unittest.TestCase):

	def test_read_cpu_times(self):
		stat = "cpu  100 10 50 800 40 0 0 0 0 0\ncpu0 1 1 1 1 1 0 0 0 0 0\ncpu1 1 1 1 1 1 0 0 0 0 0\n"
		with FakeSys({"/proc/stat": stat}):
			busy, total = swaputil.read_cpu_times()
			self.assertEqual((busy, total), (160, 1000))  # idle + iowait = 840
			self.assertEqual(swaputil.cpu_count(), 2)

	def test_cpu_usage(self):
		self.assertAlmostEqual(swaputil.cpu_usage((100, 1000), (150, 1100)), 0.5)
		self.assertIsNone(swaputil.cpu_usage(None, (1, 2)))
		self.assertIsNone(swaputil.cpu_usage((1, 100), (1, 100)))

	def test_freq_and_temperature(self):
		with FakeSys({"/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq": "1600000\n",
				"/proc/stb/sensors/temp0/value": "47\n"}):
			self.assertEqual(swaputil.cpu_freq_mhz(), 1600)
			self.assertEqual(swaputil.cpu_temperature(), 47)
		with FakeSys({"/sys/class/thermal/thermal_zone0/temp": "52000\n"}):
			self.assertEqual(swaputil.cpu_temperature(), 52)
		with FakeSys({}):
			self.assertEqual(swaputil.cpu_freq_mhz(), 0)
			self.assertIsNone(swaputil.cpu_temperature())

	def test_swap_io(self):
		with FakeSys({"/proc/vmstat": "nr_free_pages 1\npswpin 12\npswpout 34\n"}):
			self.assertEqual(swaputil.read_swap_io(), (12, 34))
		with FakeSys({"/proc/vmstat": "nr_free_pages 1\n"}):
			self.assertIsNone(swaputil.read_swap_io())


class DeviceKind(unittest.TestCase):
	USB = "/sys/devices/platform/soc/f9890000.ehci/usb1/1-1/1-1.3/1-1.3:1.0/host0/target0:0:0/0:0:0:0/block/sda"
	USB_DEV = "/sys/devices/platform/soc/f9890000.ehci/usb1/1-1/1-1.3"

	def test_block_name(self):
		self.assertEqual(swaputil._block_name("/dev/sda1"), "sda")
		self.assertEqual(swaputil._block_name("/dev/mmcblk0p16"), "mmcblk0")
		self.assertEqual(swaputil._block_name("/dev/nvme0n1p2"), "nvme0n1")

	def test_root_is_flash(self):
		with FakeSys():
			self.assertEqual(swaputil.device_kind("/dev/mmcblk0p16", "/"), "flash")
			self.assertEqual(swaputil.device_kind("/dev/ubi0_0", "/"), "flash")

	def test_emmc_partition_mounted_as_hdd_is_flash(self):
		with FakeSys({"/sys/block/mmcblk0/device/type": "MMC\n"}):
			self.assertEqual(swaputil.device_kind("/dev/mmcblk0p17", "/media/hdd"), "flash")

	def test_sd_card(self):
		with FakeSys({"/sys/block/mmcblk1/device/type": "SD\n"}):
			self.assertEqual(swaputil.device_kind("/dev/mmcblk1p1", "/media/hdd"), "sd")
		with FakeSys():  # no type information: old rule
			self.assertEqual(swaputil.device_kind("/dev/mmcblk0p1", "/media/x"), "flash")
			self.assertEqual(swaputil.device_kind("/dev/mmcblk1p1", "/media/x"), "sd")

	def test_sf8008_microsd_slot_is_usb_card_reader(self):
		files = {"/sys/block/sda/removable": "1\n", "/sys/block/sda/device/vendor": "Generic ",
			"/sys/block/sda/device/model": "STORAGE DEVICE  ",
			self.USB_DEV + "/idVendor": "05e3\n", self.USB_DEV + "/idProduct": "0751\n"}
		with FakeSys(files, {"/sys/block/sda": self.USB}):
			self.assertEqual(swaputil.device_kind("/dev/sda1", "/media/hdd"), "sd")

	def test_card_reader_by_name(self):
		files = {"/sys/block/sda/removable": "1\n", "/sys/block/sda/device/model": "SD/MMC Reader"}
		with FakeSys(files, {"/sys/block/sda": self.USB}):
			self.assertEqual(swaputil.device_kind("/dev/sda1", "/media/usb"), "sd")

	def test_usb_stick_and_usb_disk(self):
		files = {"/sys/block/sda/removable": "1\n", "/sys/block/sda/device/vendor": "SanDisk",
			"/sys/block/sda/device/model": "Cruzer Blade", self.USB_DEV + "/idVendor": "0781\n",
			self.USB_DEV + "/idProduct": "5567\n"}
		with FakeSys(files, {"/sys/block/sda": self.USB}):
			self.assertEqual(swaputil.device_kind("/dev/sda1", "/media/usb"), "usb")
		files["/sys/block/sda/removable"] = "0\n"  # USB hard disk
		with FakeSys(files, {"/sys/block/sda": self.USB}):
			self.assertEqual(swaputil.device_kind("/dev/sda1", "/media/hdd"), "usb")

	def test_internal_sata_disk(self):
		with FakeSys({"/sys/block/sda/removable": "0\n"},
				{"/sys/block/sda": "/sys/devices/platform/ahci/ata1/host0/target0:0:0/0:0:0:0/block/sda"}):
			self.assertEqual(swaputil.device_kind("/dev/sda1", "/media/hdd"), "hdd")


class OutOfMemory(unittest.TestCase):
	LOG = [
		(100.0, "DmxPcrAcquire 0 -1073048612"),
		# kernel 4.4 logs two lines for one kill
		(5000.1, "Out of memory: Kill process 1234 (enigma2) score 812 or sacrifice child"),
		(5000.2, "Killed process 1234 (enigma2) total-vm:612000kB, anon-rss:400000kB, file-rss:0kB"),
		# newer kernels
		(7000.5, "Out of memory: Killed process 4321 (python3) total-vm:1kB, anon-rss:1kB, oom_score_adj:0"),
	]

	def setUp(self):
		import tempfile
		self.dir = tempfile.mkdtemp()
		self.path = os.path.join(self.dir, "oom")

	def tearDown(self):
		import shutil
		shutil.rmtree(self.dir)

	def test_parse(self):
		events = swaputil.parse_oom(self.LOG)
		self.assertEqual([(e["pid"], e["name"]) for e in events], [(1234, "enigma2"), (4321, "python3")])

	def test_history_counts_each_kill_once(self):
		files = {"/proc/sys/kernel/random/boot_id": "boot-a\n", "/proc/uptime": "8000.00 100.00\n"}
		with FakeSys(files):
			h = swaputil.update_oom_history(self.path, self.LOG, now=1000000)
			self.assertEqual(h["total"], 2)
			self.assertEqual(h["events"][0]["time"], 1000000 - 3000)  # 8000 - 5000 s ago
			# the same log read again (e.g. next GUI start): nothing new
			h = swaputil.update_oom_history(self.path, self.LOG, now=1000100)
			self.assertEqual(h["total"], 2)
			self.assertEqual(len(swaputil.oom_this_boot(h)), 2)
		# after a reboot the old events are history, new ones are added
		files["/proc/sys/kernel/random/boot_id"] = "boot-b\n"
		with FakeSys(files):
			h = swaputil.update_oom_history(self.path, self.LOG[:2], now=2000000)
			self.assertEqual(h["total"], 3)
			self.assertEqual(len(swaputil.oom_this_boot(h)), 1)

	def test_history_without_kills_or_file(self):
		with FakeSys({}):
			h = swaputil.update_oom_history(self.path, [(1.0, "nothing")])
		self.assertEqual(h, {"total": 0, "events": []})
		self.assertFalse(os.path.exists(self.path))

	def test_history_is_trimmed(self):
		log = [(float(i), "Killed process %d (x) total-vm:1kB" % i) for i in range(1, 60)]
		with FakeSys({"/proc/sys/kernel/random/boot_id": "b\n", "/proc/uptime": "100.0 1\n"}):
			h = swaputil.update_oom_history(self.path, log)
		self.assertEqual(h["total"], 59)
		self.assertEqual(len(h["events"]), swaputil.OOM_KEEP)

	def test_broken_file(self):
		with open(self.path, "w") as f:
			f.write("{broken")
		self.assertEqual(swaputil.read_oom_history(self.path), {"total": 0, "events": []})


class Zram(unittest.TestCase):

	def test_best_algorithm(self):
		self.assertEqual(swaputil.zram_best_algorithm(["zstd", "lzo", "lz4"]), "lz4")
		self.assertEqual(swaputil.zram_best_algorithm(["deflate"]), "deflate")
		self.assertEqual(swaputil.zram_best_algorithm([]), "")

	def test_ratio(self):
		self.assertAlmostEqual(swaputil.zram_ratio({"orig_kb": 300, "mem_kb": 100}), 3.0)
		self.assertEqual(swaputil.zram_ratio({"orig_kb": 0, "mem_kb": 0}), 0.0)
		self.assertEqual(swaputil.zram_ratio(None), 0.0)


class UpdateCheckTest(unittest.TestCase):
	def test_parse_version(self):
		self.assertEqual(swaputil.parse_version("v1.2.3"), (1, 2, 3))
		self.assertEqual(swaputil.parse_version("1.10"), (1, 10))
		self.assertIsNone(swaputil.parse_version("v1.2.0-beta"))
		self.assertIsNone(swaputil.parse_version(""))
		self.assertIsNone(swaputil.parse_version(None))

	def test_is_newer(self):
		self.assertTrue(swaputil.is_newer("1.1.0", "1.0.0"))
		self.assertTrue(swaputil.is_newer("1.10.0", "1.9.0"))
		self.assertTrue(swaputil.is_newer("1.0.1", "1.0"))
		self.assertFalse(swaputil.is_newer("1.0", "1.0.0"))
		self.assertFalse(swaputil.is_newer("1.0.0", "1.1.0"))
		self.assertFalse(swaputil.is_newer("garbage", "1.0.0"))
		self.assertFalse(swaputil.is_newer("", "1.0.0"))

	def test_parse_latest_release(self):
		self.assertEqual(swaputil.parse_latest_release(b'{"tag_name": "v1.2.0"}'), "1.2.0")
		self.assertEqual(swaputil.parse_latest_release('{"tag_name": "1.2.0", "draft": false}'), "1.2.0")
		self.assertIsNone(swaputil.parse_latest_release(b'{"tag_name": "v1.2.0", "prerelease": true}'))
		self.assertIsNone(swaputil.parse_latest_release(b'{"tag_name": "nightly"}'))
		self.assertIsNone(swaputil.parse_latest_release(b'{"tag_name": 5}'))
		self.assertIsNone(swaputil.parse_latest_release(b'{"message": "API rate limit exceeded"}'))
		self.assertIsNone(swaputil.parse_latest_release(b'<html>'))
		self.assertIsNone(swaputil.parse_latest_release(b'[]'))

	def test_update_check_due(self):
		day = swaputil.UPDATE_INTERVAL
		self.assertTrue(swaputil.update_check_due(0, now=1000))
		self.assertFalse(swaputil.update_check_due(1000, now=1000 + day - 1))
		self.assertTrue(swaputil.update_check_due(1000, now=1000 + day))
		self.assertTrue(swaputil.update_check_due(5000, now=1000))  # clock went backwards

	def test_fetch_failure_returns_none(self):
		self.assertIsNone(swaputil.fetch_latest_version("1.0.0", timeout=1, url="http://127.0.0.1:9/"))


if __name__ == "__main__":
	unittest.main()
