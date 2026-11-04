# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 Paderman
#
# Simple Swap Manager - system helpers
#
# Pure Python, no enigma2 imports, so this module can be tested anywhere.
# Everything here is fast and non-blocking; long running jobs (dd, swapoff)
# are executed asynchronously by the UI.

from __future__ import absolute_import, division

import errno
import json
import os
import re
import time

# File systems that support swap files
ALLOWED_FS = ("ext2", "ext3", "ext4", "xfs", "jfs", "f2fs")
SWAP_SIGNATURES = (b"SWAPSPACE2", b"SWAP-SPACE")
SWAP_FILE_NAME = "swapfile"
# Space that must stay free on the target device after creating a swap file
RESERVE_MB = 256
# Minimum / maximum swap file size offered (MB)
MIN_SIZE_MB = 32
MAX_SIZE_MB = 8192
# Keep at least this much RAM available after swapoff (kB)
SWAPOFF_RAM_RESERVE_KB = 64 * 1024


def _unescape(s):
	"""Decode the octal escapes (\\040 = space) used in /proc/mounts and /proc/swaps."""
	if "\\" not in s:
		return s
	out = []
	i = 0
	while i < len(s):
		if s[i] == "\\" and i + 4 <= len(s) and s[i + 1:i + 4].isdigit():
			try:
				out.append(chr(int(s[i + 1:i + 4], 8)))
				i += 4
				continue
			except ValueError:
				pass
		out.append(s[i])
		i += 1
	return "".join(out)


def _read(path, default=""):
	try:
		with open(path, "r") as f:
			return f.read()
	except (IOError, OSError):
		return default


def page_size():
	try:
		return os.sysconf("SC_PAGE_SIZE")
	except (ValueError, OSError, AttributeError):
		return 4096


def read_meminfo():
	"""Return /proc/meminfo as dict of kB values."""
	info = {}
	for line in _read("/proc/meminfo").splitlines():
		parts = line.split()
		if len(parts) >= 2:
			try:
				info[parts[0].rstrip(":")] = int(parts[1])
			except ValueError:
				pass
	if "MemAvailable" not in info:
		info["MemAvailable"] = info.get("MemFree", 0) + info.get("Buffers", 0) + info.get("Cached", 0)
	return info


def read_cpu_times():
	"""(busy, total) jiffies of all CPUs from /proc/stat, or None."""
	try:
		fields = [int(v) for v in _read("/proc/stat").splitlines()[0].split()[1:]]
	except (IndexError, ValueError):
		return None
	if len(fields) < 4:
		return None
	idle = fields[3] + (fields[4] if len(fields) > 4 else 0)  # idle + iowait
	total = sum(fields[:8])  # guest time is already part of user time
	return total - idle, total


def cpu_usage(prev, cur):
	"""CPU usage 0.0-1.0 between two read_cpu_times() samples, or None."""
	if not prev or not cur:
		return None
	dt = cur[1] - prev[1]
	if dt <= 0:
		return None
	return max(0.0, min(1.0, float(cur[0] - prev[0]) / dt))


def cpu_count():
	n = 0
	for line in _read("/proc/stat").splitlines():
		if line.startswith("cpu") and line[3:4].isdigit():
			n += 1
	return n


def cpu_freq_mhz():
	"""Current clock of CPU 0 in MHz, or 0 if unknown."""
	try:
		return int(_read("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq").strip()) // 1000
	except ValueError:
		return 0


def cpu_temperature():
	"""Temperature in degrees C, or None if the receiver has no sensor."""
	for path in ("/sys/class/thermal/thermal_zone0/temp", "/proc/stb/sensors/temp0/value",
			"/proc/stb/fp/temp_sensor_avs", "/proc/stb/fp/temp_sensor"):
		try:
			v = int(_read(path).strip().split()[0])
		except (IndexError, ValueError):
			continue
		if v > 1000:  # millidegrees
			v //= 1000
		if 0 < v < 150:
			return v
	return None


def read_swap_io():
	"""(pages swapped in, pages swapped out) since boot, or None."""
	vals = {}
	for line in _read("/proc/vmstat").splitlines():
		parts = line.split()
		if len(parts) == 2 and parts[0] in ("pswpin", "pswpout"):
			try:
				vals[parts[0]] = int(parts[1])
			except ValueError:
				pass
	if len(vals) != 2:
		return None
	return vals["pswpin"], vals["pswpout"]


def human_rate_kb(kb):
	"""Rate in KB/s or MB/s (the caller adds the per-second unit)."""
	if kb >= 1024:
		return "%.1f MB" % (kb / 1024.0)
	return "%d KB" % int(round(kb))


# ---------------------------------------------------------------- out of memory
#
# When RAM and swap are full, the kernel ends a program (OOM killer) and logs it.
# The kernel log is a ring buffer that forgets old lines, so events are copied into
# a small history file whenever the plugin looks (enigma2 start, system info).

OOM_FILE = "/etc/enigma2/simpleswapmanager.oom"
OOM_KEEP = 20
_OOM_RE = re.compile(r"(?:Killed process|Kill process) (\d+) \(([^)]*)\)")


def read_kernel_log(path="/dev/kmsg"):
	"""Kernel log records as (seconds since boot, text). Non-blocking, [] if not readable."""
	records = []
	try:
		fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
	except (IOError, OSError):
		return records
	try:
		for _i in range(100000):
			try:
				raw = os.read(fd, 8192)
			except (IOError, OSError) as e:
				if e.errno == errno.EPIPE:  # record was overwritten while reading
					continue
				break  # EAGAIN: no more records
			if not raw:
				break
			line = raw.decode("utf-8", "replace")
			head, _sep, text = line.partition(";")
			fields = head.split(",")
			try:
				records.append((int(fields[2]) / 1000000.0, text.split("\n")[0]))
			except (IndexError, ValueError):
				pass
	finally:
		os.close(fd)
	return records


def parse_oom(records):
	"""OOM kills in kernel log records: list of dict(uptime, pid, name)."""
	events = []
	for ts, text in records:
		m = _OOM_RE.search(text)
		if not m:
			continue
		pid, name = int(m.group(1)), m.group(2)
		# older kernels log "Kill process" and "Killed process" for the same kill
		if events and events[-1]["pid"] == pid and ts - events[-1]["uptime"] < 10:
			continue
		events.append({"uptime": ts, "pid": pid, "name": name})
	return events


def read_oom_history(path=OOM_FILE):
	try:
		with open(path, "r") as f:
			data = json.load(f)
		if isinstance(data, dict) and isinstance(data.get("events"), list):
			return data
	except (IOError, OSError, ValueError):
		pass
	return {"total": 0, "events": []}


def update_oom_history(path=OOM_FILE, records=None, now=None):
	"""Add new OOM kills from the kernel log to the history file and return the history:
	dict(total, events=[dict(key, time, name, boot)]). Never raises."""
	try:
		history = read_oom_history(path)
		events = parse_oom(read_kernel_log() if records is None else records)
		if not events:
			return history
		boot = _read("/proc/sys/kernel/random/boot_id").strip() or "?"
		now = time.time() if now is None else now
		try:
			up = float(_read("/proc/uptime").split()[0])
		except (IndexError, ValueError):
			up = 0.0
		known = set(e.get("key") for e in history["events"])
		changed = False
		for ev in events:
			key = "%s:%.3f" % (boot, ev["uptime"])
			if key in known:
				continue
			history["events"].append({"key": key, "boot": boot, "name": ev["name"],
				"time": int(now - max(0.0, up - ev["uptime"]))})
			history["total"] = int(history.get("total", 0)) + 1
			known.add(key)
			changed = True
		if changed:
			history["events"] = history["events"][-OOM_KEEP:]
			tmp = path + ".tmp"
			with open(tmp, "w") as f:
				json.dump(history, f)
			os.rename(tmp, path)
		return history
	except Exception as e:
		print("[SimpleSwapManager] OOM history: %s" % e)
		return {"total": 0, "events": []}


def oom_this_boot(history):
	boot = _read("/proc/sys/kernel/random/boot_id").strip() or "?"
	return [e for e in history.get("events", []) if e.get("boot") == boot]


def read_swaps():
	"""Return list of active swap areas from /proc/swaps."""
	result = []
	lines = _read("/proc/swaps").splitlines()
	for line in lines[1:]:
		parts = line.split()
		if len(parts) < 5:
			continue
		try:
			result.append({
				"path": _unescape(parts[0]),
				"type": parts[1],
				"size_kb": int(parts[2]),
				"used_kb": int(parts[3]),
				"prio": int(parts[4]),
			})
		except ValueError:
			pass
	return result


def active_paths():
	return [s["path"] for s in read_swaps()]


def read_mounts():
	result = []
	for line in _read("/proc/mounts").splitlines():
		parts = line.split()
		if len(parts) < 4:
			continue
		result.append({
			"device": _unescape(parts[0]),
			"mount": _unescape(parts[1]),
			"fstype": parts[2],
			"options": parts[3].split(","),
		})
	return result


def get_swappiness():
	try:
		return int(_read("/proc/sys/vm/swappiness", "-1").strip())
	except ValueError:
		return -1


def set_swappiness(value):
	try:
		value = max(0, min(100, int(value)))
		with open("/proc/sys/vm/swappiness", "w") as f:
			f.write("%d\n" % value)
		return True
	except (IOError, OSError, ValueError):
		return False


def is_swap_file(path):
	"""True if path is a regular file carrying a Linux swap signature."""
	try:
		if not os.path.isfile(path) or os.path.islink(path):
			return False
		ps = page_size()
		if os.path.getsize(path) < ps * 10:
			return False
		with open(path, "rb") as f:
			f.seek(ps - 10)
			return f.read(10) in SWAP_SIGNATURES
	except (IOError, OSError):
		return False


def _block_name(device):
	"""/dev/sda1 -> sda, /dev/mmcblk0p16 -> mmcblk0"""
	name = os.path.basename(os.path.realpath(device))
	if name.startswith("mmcblk") or name.startswith("nvme"):
		return name.split("p")[0] if "p" in name[6:] else name
	return name.rstrip("0123456789")


def device_kind(device, mount):
	"""Classify a block device: 'flash', 'sd', 'usb' or 'hdd'."""
	blk = _block_name(device)
	if mount == "/" or blk.startswith("mtd") or blk.startswith("ubi"):
		return "flash"
	if blk.startswith("mmcblk"):
		# the kernel knows: "MMC" = soldered eMMC (internal flash, also when a partition of it
		# is mounted as /media/hdd), "SD" = memory card
		mmc_type = _read("/sys/block/%s/device/type" % blk).strip().upper()
		if mmc_type == "MMC":
			return "flash"
		if mmc_type.startswith("SD"):
			return "sd"
		return "flash" if blk == "mmcblk0" else "sd"
	removable = _read("/sys/block/%s/removable" % blk, "0").strip()
	# USB sticks report removable=1; USB hard disks often not, check the bus
	try:
		link = os.path.realpath("/sys/block/%s" % blk)
	except OSError:
		link = ""
	if "/usb" in link and _is_card_reader(blk, link):
		return "sd"  # e.g. the internal microSD slot of the SF8008 is a USB card reader
	if removable == "1":
		return "usb"
	if "/usb" in link:
		return "usb"
	return "hdd"


# USB vendor:product IDs of common card reader chips (Genesys, Realtek, Alcor, Transcend, ...)
CARD_READER_IDS = frozenset((
	"05e3:0723", "05e3:0727", "05e3:0731", "05e3:0736", "05e3:0743", "05e3:0748", "05e3:0749",
	"05e3:0751", "05e3:0760", "05e3:0761",
	"0bda:0109", "0bda:0119", "0bda:0129", "0bda:0138", "0bda:0139", "0bda:0151", "0bda:0153",
	"0bda:0158", "0bda:0159", "0bda:0161", "0bda:0169", "0bda:0177", "0bda:0184", "0bda:0186",
	"058f:6331", "058f:6332", "058f:6335", "058f:6360", "058f:6361", "058f:6362", "058f:6364",
	"058f:6366", "058f:6377", "058f:8468",
	"14cd:121c", "14cd:125c", "14cd:125d", "14cd:6116", "8564:4000", "1908:0226", "0dda:2026",
))
CARD_READER_WORDS = ("SD", "MMC", "SD/MMC", "SDXC", "SDHC", "MICROSD", "CARD", "READER", "CARDREADER")


def _is_card_reader(blk, link):
	"""True if a USB block device is a memory card in a (possibly built-in) USB card reader."""
	name = "%s %s" % (_read("/sys/block/%s/device/vendor" % blk), _read("/sys/block/%s/device/model" % blk))
	words = name.upper().replace("-", " ").replace("_", " ").split()
	if any(w in CARD_READER_WORDS for w in words):
		return True
	path = link
	while path and path != "/" and "/usb" in path:
		vid = _read(os.path.join(path, "idVendor")).strip()
		if vid:
			pid = _read(os.path.join(path, "idProduct")).strip()
			return ("%s:%s" % (vid, pid)).lower() in CARD_READER_IDS
		path = os.path.dirname(path)
	return False


def disk_space(mount):
	"""Return (free_bytes, total_bytes) for a mount point."""
	try:
		st = os.statvfs(mount)
		return st.f_bavail * st.f_frsize, st.f_blocks * st.f_frsize
	except OSError:
		return 0, 0


def _mount_rank(mount):
	# prefer the classic names when one device is mounted several times
	for i, pref in enumerate(("/media/hdd", "/media/usb", "/media/sdcard", "/media/mmc")):
		if mount == pref:
			return (0, i, len(mount))
	if mount.startswith("/media/autofs"):
		return (2, 0, len(mount))
	return (1, 0, len(mount))


def find_locations():
	"""Return the mount points where a swap file may be created.

	Each entry: dict(mount, device, fstype, kind, free, total, path)
	Sorted: hdd/usb/sd first, internal flash last.
	"""
	seen = {}
	for m in read_mounts():
		dev, mnt, fs = m["device"], m["mount"], m["fstype"]
		if not dev.startswith("/dev/") or dev.startswith("/dev/loop"):
			continue
		if fs not in ALLOWED_FS or "ro" in m["options"]:
			continue
		if not (mnt == "/" or mnt.startswith("/media/") or mnt.startswith("/mnt/")):
			continue
		if not os.path.isdir(mnt):
			continue
		key = os.path.realpath(dev)
		if key in seen and _mount_rank(seen[key]["mount"]) <= _mount_rank(mnt):
			continue
		free, total = disk_space(mnt)
		seen[key] = {
			"mount": mnt,
			"device": dev,
			"fstype": fs,
			"kind": device_kind(dev, mnt),
			"free": free,
			"total": total,
			"path": os.path.join(mnt, SWAP_FILE_NAME),
		}
	order = {"hdd": 0, "usb": 1, "sd": 2, "flash": 3}
	return sorted(seen.values(), key=lambda l: (order.get(l["kind"], 9), l["mount"]))


def mount_of(path):
	"""Return the mount entry containing path (longest prefix match)."""
	best = None
	real = os.path.realpath(path)
	for m in read_mounts():
		mnt = m["mount"]
		if real == mnt or real.startswith(mnt.rstrip("/") + "/"):
			if best is None or len(mnt) > len(best["mount"]):
				best = m
	return best


def _candidate_files(directory):
	try:
		names = os.listdir(directory)
	except OSError:
		return []
	return [os.path.join(directory, n) for n in names if "swap" in n.lower()]


def list_swaps(extra_paths=(), zram_size_mb=0):
	"""Return all known swap spaces: active ones and swap files found on disk.

	zram_size_mb: size of the configured (maybe inactive) zram swap, 0 = none.
	Each entry: dict(path, type, size_kb, used_kb, active, prio); type is file, partition or zram
	"""
	entries = {}
	for s in read_swaps():
		if is_zram(s["path"]):
			kind = "zram"
		elif s["type"] == "partition":
			kind = "partition"
		else:
			kind = "file"
		entries[s["path"]] = {
			"path": s["path"],
			"type": kind,
			"size_kb": s["size_kb"],
			"used_kb": s["used_kb"],
			"prio": s["prio"],
			"active": True,
		}
	dirs = set()
	for m in read_mounts():
		if m["device"].startswith("/dev/") and (m["mount"] == "/" or m["mount"].startswith("/media/") or m["mount"].startswith("/mnt/")):
			dirs.add(m["mount"])
	candidates = set(extra_paths)
	for d in dirs:
		candidates.update(_candidate_files(d))
	for path in candidates:
		if path in entries or not path:
			continue
		if is_swap_file(path):
			entries[path] = {
				"path": path,
				"type": "file",
				"size_kb": os.path.getsize(path) // 1024,
				"used_kb": 0,
				"prio": 0,
				"active": False,
			}
	zpath = zram_path()
	if zram_size_mb and zpath not in entries:
		entries[zpath] = {
			"path": zpath,
			"type": "zram",
			"size_kb": int(zram_size_mb) * 1024,
			"used_kb": 0,
			"prio": ZRAM_PRIORITY,
			"active": False,
		}
	# zram first, then active, then by path
	return sorted(entries.values(), key=lambda e: (e["type"] != "zram", not e["active"], e["path"]))


def recommended_size_mb(mem_total_kb, free_bytes=None):
	"""Recommended swap size: about half the RAM, at least 256 MB, at most 1 GB."""
	ram_mb = mem_total_kb // 1024
	if ram_mb <= 512:
		rec = 512
	elif ram_mb <= 2048:
		rec = 512 if ram_mb <= 1024 else 1024
	else:
		rec = 1024
	if free_bytes is not None:
		rec = min(rec, max_size_mb(free_bytes))
	return rec


def max_size_mb(free_bytes):
	return max(0, min(MAX_SIZE_MB, int(free_bytes // (1024 * 1024)) - RESERVE_MB))


def size_choices(mem_total_kb, free_bytes):
	"""Return list of (size_mb, recommended) the user can pick for a device."""
	limit = max_size_mb(free_bytes)
	rec = recommended_size_mb(mem_total_kb, free_bytes)
	sizes = [s for s in (128, 256, 512, 768, 1024, 1536, 2048, 4096) if s <= limit]
	if rec >= MIN_SIZE_MB and rec not in sizes:
		sizes.append(rec)
		sizes.sort()
	return [(s, s == rec) for s in sizes]


def can_swapoff(entry, meminfo=None):
	"""Check whether enough RAM is available to take back the used swap pages."""
	if not entry.get("active"):
		return True
	mi = meminfo or read_meminfo()
	return mi.get("MemAvailable", 0) - SWAPOFF_RAM_RESERVE_KB > entry.get("used_kb", 0)


def human_kb(kb):
	mb = kb / 1024.0
	if mb >= 1024:
		return "%.1f GB" % (mb / 1024.0)
	return "%d MB" % int(round(mb))


def human_bytes(b):
	return human_kb(b // 1024)


def shell_quote(s):
	return "'" + s.replace("'", "'\\''") + "'"


# ---------------------------------------------------------------- zram
#
# zram = compressed swap inside the RAM. Pages are compressed (about 2-3:1),
# so the box can keep more data in memory without touching any drive.
# Only offered when the kernel supports it. The plugin manages /dev/zram0.

SYSFS = "/sys"
ZRAM_DEV = "zram0"
ZRAM_PRIORITY = 100  # higher than swap files (-1), so zram is used first
# preferred algorithms: fast ones first (receiver CPUs are weak)
ZRAM_ALGO_PREFERENCE = ("lz4", "lzo-rle", "lzo", "zstd", "lz4hc", "842")
ZRAM_ALGOS_DEFAULT = ("lz4", "lzo-rle", "lzo", "zstd")


def _kernel_release():
	try:
		return os.uname()[2]
	except (AttributeError, OSError):
		return ""


_zram_module_cache = []


def zram_module_available():
	"""True if zram is built in or available as kernel module (cached, the kernel does not change)."""
	if not _zram_module_cache:
		found = False
		base = "/lib/modules/%s" % _kernel_release()
		for name in ("modules.builtin", "modules.dep"):
			for line in _read(os.path.join(base, name)).splitlines():
				if "/zram.ko" in line.split(":")[0]:
					found = True
					break
			if found:
				break
		_zram_module_cache.append(found)
	return _zram_module_cache[0]


def zram_supported():
	return zram_status()[0]


def zram_path(dev=ZRAM_DEV):
	return "/dev/%s" % dev


def is_zram(path):
	return os.path.basename(path).startswith("zram")


def zram_algorithms(dev=ZRAM_DEV):
	"""Return (available, current). Falls back to common names if the device is not loaded yet."""
	text = _read(os.path.join(SYSFS, "block", dev, "comp_algorithm")).strip()
	if not text:
		return list(ZRAM_ALGOS_DEFAULT), ""
	algos, current = [], ""
	for a in text.split():
		if a.startswith("[") and a.endswith("]"):
			a = a[1:-1]
			current = a
		algos.append(a)
	return algos, current


def zram_best_algorithm(available):
	for a in ZRAM_ALGO_PREFERENCE:
		if a in available:
			return a
	return available[0] if available else ""


def zram_stats(dev=ZRAM_DEV):
	"""Return dict(disksize_kb, orig_kb, compr_kb, mem_kb, algo) or None if the device does not exist."""
	base = os.path.join(SYSFS, "block", dev)
	if not os.path.isdir(base):
		return None

	def num(name):
		try:
			return int(_read(os.path.join(base, name), "0").split()[0])
		except (ValueError, IndexError):
			return 0

	orig = compr = mem = 0
	mm = _read(os.path.join(base, "mm_stat")).split()
	if len(mm) >= 3:
		try:
			orig, compr, mem = int(mm[0]), int(mm[1]), int(mm[2])
		except ValueError:
			pass
	else:  # old kernels (< 4.2)
		orig, compr, mem = num("orig_data_size"), num("compr_data_size"), num("mem_used_total")
	return {
		"disksize_kb": num("disksize") // 1024,
		"orig_kb": orig // 1024,
		"compr_kb": compr // 1024,
		"mem_kb": mem // 1024,
		"algo": zram_algorithms(dev)[1],
	}


def zram_ratio(stats):
	if not stats or not stats["mem_kb"] or not stats["orig_kb"]:
		return 0.0
	return float(stats["orig_kb"]) / stats["mem_kb"]


def zram_size_choices(mem_total_kb):
	"""Sizes (uncompressed capacity, MB) for zram; recommended is about half the RAM."""
	ram_mb = mem_total_kb // 1024
	rec = max(64, (ram_mb // 2) // 64 * 64)
	sizes = [s for s in (128, 256, 384, 512, 768, 1024, 1536, 2048) if s <= ram_mb]
	if rec not in sizes:
		sizes.append(rec)
		sizes.sort()
	return [(s, s == rec) for s in sizes]


def zram_setup_cmd(size_mb, algo="", dev=ZRAM_DEV, sysfs=None):
	"""Shell script that (re)creates the zram swap device and activates it."""
	sysfs = sysfs or SYSFS
	z = "%s/block/%s" % (sysfs, dev)
	lines = [
		"Z=%s" % z,
		"D=/dev/%s" % dev,
		# load the module if needed and wait for the device node
		'if [ ! -d "$Z" ]; then modprobe zram num_devices=1 || exit 1; fi',
		'i=0; while [ ! -d "$Z" ] || [ ! -e "$D" ]; do i=$((i+1)); [ $i -gt 10 ] && echo "zram device not found" && exit 1; sleep 1; done',
		# reconfigure: swapoff + reset (frees the memory)
		'if grep -q "^$D " /proc/swaps; then swapoff "$D" || exit 1; fi',
		'echo 1 > "$Z/reset" || exit 1',
	]
	if algo:
		lines.append('echo %s > "$Z/comp_algorithm" 2>/dev/null || echo "algorithm %s not supported, using default"' % (algo, algo))
	lines += [
		'if [ -w "$Z/max_comp_streams" ]; then grep -c ^processor /proc/cpuinfo > "$Z/max_comp_streams" 2>/dev/null; fi',
		'echo %dM > "$Z/disksize" || exit 1' % int(size_mb),
		'mkswap "$D" || exit 1',
		'swapon -p %d "$D" || swapon "$D" || exit 1' % ZRAM_PRIORITY,
		"exit 0",
	]
	return "; ".join(lines)


def zram_stop_cmd(dev=ZRAM_DEV, sysfs=None):
	sysfs = sysfs or SYSFS
	return ('D=/dev/%s; if grep -q "^$D " /proc/swaps; then swapoff "$D" || exit 1; fi; '
		'echo 1 > %s/block/%s/reset 2>/dev/null; exit 0') % (dev, sysfs, dev)


# ---------------------------------------------------------------- capabilities

_kconfig_cache = []


def kernel_config():
	"""Parsed /proc/config.gz as dict {CONFIG_X: 'y'|'m'|'n'|value}, or None if not available."""
	if not _kconfig_cache:
		cfg = None
		try:
			import gzip
			with gzip.open("/proc/config.gz", "rb") as f:
				data = f.read().decode("utf-8", "ignore")
			cfg = {}
			for line in data.splitlines():
				line = line.strip()
				if line.startswith("# CONFIG_") and line.endswith(" is not set"):
					cfg[line[2:-11]] = "n"
				elif line.startswith("CONFIG_") and "=" in line:
					k, v = line.split("=", 1)
					cfg[k] = v.strip('"')
		except (IOError, OSError, ImportError, EOFError):
			cfg = None
		_kconfig_cache.append(cfg)
	return _kconfig_cache[0]


def zram_status():
	"""Return (supported, reason). reason is one of:
	loaded, builtin, module, not_in_kernel, module_missing, unknown
	"""
	if os.path.isdir(os.path.join(SYSFS, "block", ZRAM_DEV)) or os.path.isdir(os.path.join(SYSFS, "module", "zram")):
		return True, "loaded"
	kc = kernel_config()
	value = kc.get("CONFIG_ZRAM", "n") if kc is not None else None
	module = zram_module_available()
	if value == "y":
		return True, "builtin"
	if module:
		return True, "module"
	if value == "m":
		return False, "module_missing"
	if value == "n":
		return False, "not_in_kernel"
	return False, "unknown"


def zswap_status():
	"""Return dict(available, enabled, compressor) for zswap (compressed cache in front of swap)."""
	base = os.path.join(SYSFS, "module", "zswap", "parameters")
	if os.path.isdir(base):
		return {
			"available": True,
			"enabled": _read(os.path.join(base, "enabled")).strip() in ("Y", "1"),
			"compressor": _read(os.path.join(base, "compressor")).strip(),
		}
	kc = kernel_config() or {}
	return {"available": kc.get("CONFIG_ZSWAP") == "y", "enabled": False, "compressor": ""}


def _key_value_file(path):
	result = {}
	for line in _read(path).splitlines():
		if "=" in line:
			k, v = line.split("=", 1)
			result[k.strip()] = v.strip()
	return result


def system_info():
	"""Box, image and kernel facts for the information screen."""
	iv = _key_value_file("/etc/image-version")
	model = " ".join(x for x in (iv.get("machine_brand", ""), iv.get("machine_name", "")) if x)
	if not model:
		model = _read("/proc/stb/info/boxtype").strip() or _read("/proc/stb/info/vumodel").strip()
	try:
		uname = os.uname()
		hostname, release, machine = uname[1], uname[2], uname[4]
	except (AttributeError, OSError):
		hostname = release = machine = ""
	if not model:
		model = hostname
	image = " ".join(x for x in (iv.get("comment") or iv.get("creator", ""), iv.get("version", "")) if x)
	if not image:
		for line in _read("/etc/issue").splitlines():
			line = line.replace("\\n", "").replace("\\l", "").strip()
			if line and not line.lower().startswith("welcome"):
				image = line
				break
	kc = kernel_config()
	return {
		"model": model,
		"image": image,
		"kernel": release,
		"arch": machine,
		"python": "%d.%d.%d" % tuple(__import__("sys").version_info[:3]),
		"ram_kb": read_meminfo().get("MemTotal", 0),
		"page_size": page_size(),
		"swap_kernel": os.path.exists("/proc/swaps") and (kc is None or kc.get("CONFIG_SWAP", "y") == "y"),
		"kconfig": kc is not None,
	}


# ---------------------------------------------------------------- uninstall

PACKAGE = "enigma2-plugin-systemplugins-simpleswapmanager"


def uninstall_cmd(plugin_dir, package=PACKAGE):
	"""Shell command that removes the plugin with the package manager of the image
	(opkg, or dpkg on DreamOS). Copied-in installations are removed directly."""
	plugin_dir = os.path.normpath(plugin_dir)
	if os.path.basename(plugin_dir) != "SimpleSwapManager":
		raise ValueError("unexpected plugin directory: %s" % plugin_dir)
	q = shell_quote(plugin_dir)
	return ("if command -v opkg >/dev/null 2>&1; then opkg remove %(p)s; "
		"elif command -v dpkg >/dev/null 2>&1; then dpkg -r %(p)s; fi; "
		"rm -rf %(d)s; [ ! -e %(d)s ]") % {"p": package, "d": q}


# ---------------------------------------------------------------- update check

RELEASES_URL = "https://github.com/Paderman/enigma2-plugin-simpleswapmanager/releases"
LATEST_RELEASE_API = "https://api.github.com/repos/Paderman/enigma2-plugin-simpleswapmanager/releases/latest"
UPDATE_INTERVAL = 24 * 3600


def parse_version(text):
	"""'v1.2.3' -> (1, 2, 3); None if it is not a plain release version."""
	m = re.match(r"^\s*v?(\d+(?:\.\d+){0,3})\s*$", text or "")
	if not m:
		return None
	return tuple(int(x) for x in m.group(1).split("."))


def is_newer(latest, current):
	"""True if version string latest is newer than current (missing parts count as 0)."""
	a, b = parse_version(latest), parse_version(current)
	if a is None or b is None:
		return False
	n = max(len(a), len(b))
	return a + (0,) * (n - len(a)) > b + (0,) * (n - len(b))


def parse_latest_release(data):
	"""Version from a GitHub 'latest release' JSON answer, or None."""
	try:
		info = json.loads(data.decode("utf-8") if isinstance(data, bytes) else data)
	except (ValueError, UnicodeDecodeError):
		return None
	if not isinstance(info, dict) or info.get("draft") or info.get("prerelease"):
		return None
	tag = info.get("tag_name")
	# json returns text as unicode on Python 2 and str on Python 3
	if not isinstance(tag, type(u"")) or parse_version(tag) is None:
		return None
	return str(tag.strip().lstrip("v"))


def update_check_due(last_check, now=None, interval=UPDATE_INTERVAL):
	"""Check again once the interval has passed (or the clock jumped backwards)."""
	now = time.time() if now is None else now
	return not last_check or now - last_check >= interval or now < last_check


def fetch_latest_version(current, timeout=5, url=LATEST_RELEASE_API):
	"""Ask GitHub for the latest release (blocking, run it in a thread).

	Only a plain HTTPS GET with a generic User-Agent; returns the version or None.
	"""
	try:
		from urllib.request import Request, urlopen
	except ImportError:  # Python 2
		from urllib2 import Request, urlopen
	req = Request(url, headers={
		"User-Agent": "SimpleSwapManager/%s" % current,
		"Accept": "application/vnd.github+json",
	})
	try:
		resp = urlopen(req, timeout=timeout)
		try:
			return parse_latest_release(resp.read(65536))
		finally:
			resp.close()
	except Exception:
		return None
