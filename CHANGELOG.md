# Changelog

## 1.0.0 – 2026-11-03

First public release.

- Dashboard with live RAM, swap and total usage (RAM + swap), CPU load (bar turns yellow / red
  under high load) with clock and temperature, and swap activity (in / out per second)
- Two-step wizard to create a swap file: choose drive, choose size (presets or custom size in MB)
- Real progress bar while the file is written, can be cancelled at any time
- Activate / deactivate / delete with one key, activation at startup, swappiness setting
- zram (compressed swap in RAM) as an option on kernels that support it
- System information screen (INFO): kernel, RAM, swap / zram / zswap support, usable drives;
  unsupported features are shown with the reason, and how often memory ran out (OOM kills,
  kept in a small history because the kernel log forgets them)
- Change the size of a swap file (startup setting and active state are kept)
- Safe by design: everything asynchronous, `dd` with `nice` and `O_DIRECT`, no `swapoff`
  without enough free RAM, only Linux file systems, never edits `/etc/fstab`
- Warns before using internal flash or an SD card (wear); drive type detected from the device,
  also when internal flash is mounted as `/media/hdd`; memory cards in (built-in) USB card readers
  are recognised as SD cards; after creating a swap file on an SD card the plugin offers
  swappiness 10
- Dashboard shows how much was written to swap since boot
- Wizard badges by risk: hard disk / USB recommended, SD card "not ideal", internal flash
  "not recommended" (soldered in, cannot be replaced)
- Tests for `swaputil.py` (`python3 -m unittest discover -s tests`)
- 32 languages: English, العربية, Български, Čeština, Dansk, Deutsch, Eesti, Ελληνικά, Español,
  Français, עברית, Hrvatski, Italiano, Latviešu, Lietuvių, Magyar, Nederlands, Norsk, Polski,
  Português, Română, Русский, Slovenčina, Slovenščina, Srpski, Suomi, Svenska, ไทย, Tiếng Việt,
  Türkçe, Українська, 简体中文
- Uninstall from the settings: keep or delete the swap space, then optional GUI restart
- Clear, translated messages when installing, updating and removing the package
  (colours on a terminal, plain text in the GUI)
- Python 3 and Python 2
- Packages: `.ipk` (opkg images) and an experimental, untested `.deb` for DreamOS
