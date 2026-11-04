# Shared part of the package scripts (preinst/postinst/prerm/postrm).
# build.sh inserts this file at the "# @COMMON@" line of each script.
#
# - talks in the language of the enigma2 GUI (English fallback)
# - colours and Unicode symbols only on a real terminal (SSH/telnet);
#   plain ASCII when installed from the GUI or with redirected output
#
# Translations: CONTROL/i18n/<code>.sh defines msg_<code> (same keys as
# msg_en below). build.sh inserts them in front of this file.

PKG_VERSION="@VERSION@"
PLUGIN_DIR="${PKG_ROOT:-/}usr/lib/enigma2/python/Plugins/SystemPlugins/SimpleSwapManager"
SETTINGS=/etc/enigma2/settings
LANG_FILE=/etc/enigma2/simpleswapmanager.lang
OOM_FILE=/etc/enigma2/simpleswapmanager.oom
STATE_FILE=/tmp/.simpleswapmanager-install

# ---------------------------------------------------------------- texts

msg_en() {
	case "$1" in
	title_install)  echo "Installation" ;;
	title_update)   echo "Update from %s to %s" ;;
	title_reinst)   echo "Reinstallation" ;;
	title_remove)   echo "Removal" ;;
	files_ok)       echo "Plugin files installed" ;;
	files_bad)      echo "Plugin files incomplete - please install again" ;;
	langs)          echo "Languages: %s" ;;
	kept)           echo "Settings and swap files have been kept" ;;
	swap_active)    echo "Swap active: %s (%s MB)" ;;
	swap_none)      echo "No swap active yet" ;;
	ram)            echo "RAM: %s MB" ;;
	zram_yes)       echo "zram (compressed RAM): supported" ;;
	zram_no)        echo "zram (compressed RAM): not supported by this kernel" ;;
	restart)        echo "Please restart the GUI to load the plugin:" ;;
	restart_upd)    echo "Please restart the GUI to load the new version:" ;;
	restart_rm)     echo "Please restart the GUI to unload the plugin:" ;;
	restart_menu)   echo "MENU > Standby / Restart > Restart GUI" ;;
	restart_cmd)    echo "or in the terminal:" ;;
	find_it)        echo "Afterwards you find it in the plugin browser and under" ;;
	find_path)      echo "MENU > Setup > System > Storage Devices > Simple Swap Manager" ;;
	rm_done)        echo "Plugin removed" ;;
	rm_swap_on)     echo "Swap file stays active until the next reboot: %s (%s MB)" ;;
	rm_swap_kept)   echo "Swap file kept on the drive: %s" ;;
	rm_no_boot)     echo "It will no longer be activated at startup." ;;
	rm_delete)      echo "To delete it and free the disk space:" ;;
	rm_zram)        echo "zram stays active until the next reboot" ;;
	experimental)   echo "Experimental build for DreamOS - please report problems" ;;
	esac
}

lang_name() {
	case "$1" in
	en) echo "English" ;;    de) echo "Deutsch" ;;     fr) echo "Français" ;;
	it) echo "Italiano" ;;   es) echo "Español" ;;     nl) echo "Nederlands" ;;
	pl) echo "Polski" ;;     tr) echo "Türkçe" ;;      ru) echo "Русский" ;;
	uk) echo "Українська" ;; cs) echo "Čeština" ;;     sk) echo "Slovenčina" ;;
	hu) echo "Magyar" ;;     el) echo "Ελληνικά" ;;    pt) echo "Português" ;;
	ro) echo "Română" ;;     sv) echo "Svenska" ;;     da) echo "Dansk" ;;
	fi) echo "Suomi" ;;      nb) echo "Norsk" ;;       bg) echo "Български" ;;
	hr) echo "Hrvatski" ;;   sr) echo "Srpski" ;;      sl) echo "Slovenščina" ;;
	et) echo "Eesti" ;;      lv) echo "Latviešu" ;;    lt) echo "Lietuvių" ;;
	vi) echo "Tiếng Việt" ;; zh|zh_CN) echo "简体中文" ;; th) echo "ไทย" ;;
	ar) echo "العربية" ;;    he) echo "עברית" ;;
	*)  echo "$1" ;;
	esac
}

# ------------------------------------------------------------- language

detect_lang() {
	l=""
	# 1. written by the plugin itself = the language the GUI really uses
	[ -r "$LANG_FILE" ] && l=$(head -n 1 "$LANG_FILE")
	# 2. explicitly chosen GUI language (openATV 7.x: misc.locale, older images: osd.language)
	[ -z "$l" ] && [ -r "$SETTINGS" ] && l=$(sed -n 's/^config\.misc\.locale=//p' "$SETTINGS" | head -n 1)
	[ -z "$l" ] && [ -r "$SETTINGS" ] && l=$(sed -n 's/^config\.osd\.language=//p' "$SETTINGS" | head -n 1)
	# 3. image default (openATV does not store its default de_DE)
	if [ -z "$l" ]; then
		if grep -qi '^distro=openatv' /etc/image-version 2>/dev/null; then
			l=de_DE
		else
			l=${LC_ALL:-${LC_MESSAGES:-$LANG}}
		fi
	fi
	l=${l%%_*}
	l=${l%%.*}
	if [ -n "$l" ] && command -v "msg_$l" >/dev/null 2>&1; then
		echo "$l"
	else
		echo en
	fi
}
UI_LANG=$(detect_lang)

# T key [args...]  - translated text, printf style
T() {
	_k=$1; shift
	_f=$("msg_$UI_LANG" "$_k")
	[ -z "$_f" ] && _f=$(msg_en "$_k")
	# shellcheck disable=SC2059
	printf "$_f" "$@"
}

# ---------------------------------------------------------------- output

if [ -t 1 ] && [ "${TERM:-dumb}" != "dumb" ]; then
	E=$(printf '\033')
	C_BAR="$E[38;5;39m"; C_TITLE="$E[1;97m"; C_SUB="$E[37m"; C_DIM="$E[90m"
	C_OK="$E[1;32m"; C_INFO="$E[1;36m"; C_WARN="$E[1;33m"; C_ERR="$E[1;31m"
	C_CMD="$E[1;97m"; C_RST="$E[0m"
	S_OK="✔ "; S_INFO="● "; S_WARN="▲ "; S_ERR="✖ "; S_GO="➜ "
	IND="      "
	LINE="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	THIN="──────────────────────────────────────────────────────────"
else
	C_BAR=""; C_TITLE=""; C_SUB=""; C_DIM=""; C_OK=""; C_INFO=""; C_WARN=""
	C_ERR=""; C_CMD=""; C_RST=""
	S_OK="[OK]"; S_INFO="[i] "; S_WARN="[!] "; S_ERR="[X] "; S_GO="->  "
	IND="        "
	LINE="=========================================================="
	THIN="----------------------------------------------------------"
fi

ui_header() {  # subtitle
	printf '\n  %s%s%s\n' "$C_BAR" "$LINE" "$C_RST"
	printf '   %sSimple Swap Manager %s%s\n' "$C_TITLE" "$PKG_VERSION" "$C_RST"
	printf '   %s%s%s\n' "$C_SUB" "$1" "$C_RST"
	printf '  %s%s%s\n' "$C_BAR" "$LINE" "$C_RST"
}
ui_ok()    { printf '   %s%s%s %s\n' "$C_OK" "$S_OK" "$C_RST" "$1"; }
ui_info()  { printf '   %s%s%s %s\n' "$C_INFO" "$S_INFO" "$C_RST" "$1"; }
ui_warn()  { printf '   %s%s%s %s\n' "$C_WARN" "$S_WARN" "$C_RST" "$1"; }
ui_err()   { printf '   %s%s%s %s\n' "$C_ERR" "$S_ERR" "$C_RST" "$1"; }
ui_text()  { printf '%s%s\n' "$IND" "$1"; }
ui_cmd()   { printf '%s%s%s%s\n' "$IND" "$C_CMD" "$1" "$C_RST"; }
ui_dim()   { printf '%s%s%s%s\n' "$IND" "$C_DIM" "$1" "$C_RST"; }
ui_sep()   { printf '  %s%s%s\n' "$C_DIM" "$THIN" "$C_RST"; }
ui_go()    { printf '   %s%s%s %s%s%s\n' "$C_WARN" "$S_GO" "$C_RST" "$C_TITLE" "$1" "$C_RST"; }
ui_end()   { printf '  %s%s%s\n\n' "$C_BAR" "$LINE" "$C_RST"; }

ui_restart_hint() {  # restart | restart_upd | restart_rm
	ui_sep
	ui_go "$(T "$1")"
	ui_text "$(T restart_menu)"
	ui_dim "$(T restart_cmd)"
	if [ -d /run/systemd/system ] && command -v systemctl >/dev/null 2>&1; then
		ui_cmd "systemctl restart enigma2"
	else
		ui_cmd "init 4; sleep 3; init 3"
	fi
}

# ---------------------------------------------------------- system state

# active swap spaces: "path size_mb type" per line
active_swaps() {
	awk 'NR > 1 { printf "%s %d %s\n", $1, ($3 + 512) / 1024, $2 }' /proc/swaps 2>/dev/null
}

boot_swapfile() {
	sed -n 's/^config\.plugins\.simpleswapmanager\.bootfile=//p' "$SETTINGS" 2>/dev/null | head -n 1
}

ram_mb() {
	awk '/^MemTotal:/ { printf "%d", $2 / 1024 }' /proc/meminfo 2>/dev/null
}

zram_supported() {
	[ -e /sys/block/zram0 ] && return 0
	m=/lib/modules/$(uname -r)
	grep -qs '/zram\.ko' "$m/modules.builtin" "$m/modules.dep"
}
