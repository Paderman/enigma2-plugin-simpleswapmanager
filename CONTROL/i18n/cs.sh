# Čeština texts of the package scripts (generated)
msg_cs() {
	case "$1" in
	title_install)   echo "Instalace" ;;
	title_update)    echo "Aktualizace z %s na %s" ;;
	title_reinst)    echo "Přeinstalace" ;;
	title_remove)    echo "Odinstalace" ;;
	files_ok)        echo "Soubory pluginu nainstalovány" ;;
	files_bad)       echo "Soubory pluginu jsou neúplné - nainstalujte znovu" ;;
	langs)           echo "Jazyky: %s" ;;
	kept)            echo "Nastavení a odkládací soubory zůstaly zachovány" ;;
	swap_active)     echo "Swap aktivní: %s (%s MB)" ;;
	swap_none)       echo "Zatím není aktivní žádný swap" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (komprimovaná RAM): podporováno" ;;
	zram_no)         echo "zram (komprimovaná RAM): toto jádro nepodporuje" ;;
	restart)         echo "Restartujte GUI, aby se plugin načetl:" ;;
	restart_upd)     echo "Restartujte GUI, aby se načetla nová verze:" ;;
	restart_rm)      echo "Restartujte GUI, aby se plugin uvolnil:" ;;
	restart_menu)    echo "MENU > Vypnutí / Restart > Restartovat Enigmu" ;;
	restart_cmd)     echo "nebo v terminálu:" ;;
	find_it)         echo "Poté ho najdete v prohlížeči pluginů a v" ;;
	find_path)       echo "MENU > Nastavení > Systém > Zařízení pro ukládání dat > Simple Swap Manager" ;;
	rm_done)         echo "Plugin odebrán" ;;
	rm_swap_on)      echo "Odkládací soubor zůstane aktivní do příštího restartu: %s (%s MB)" ;;
	rm_swap_kept)    echo "Odkládací soubor zůstává na disku: %s" ;;
	rm_no_boot)      echo "Při startu se už nebude aktivovat." ;;
	rm_delete)       echo "Pro smazání a uvolnění místa na disku:" ;;
	rm_zram)         echo "zram zůstane aktivní do příštího restartu" ;;
	experimental)   echo "Experimentální verze pro DreamOS - hlaste prosím problémy" ;;
	esac
}
