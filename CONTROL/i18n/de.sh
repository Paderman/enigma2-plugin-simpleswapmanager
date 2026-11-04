# German texts of the package scripts
msg_de() {
	case "$1" in
	title_install)  echo "Installation" ;;
	title_update)   echo "Update von %s auf %s" ;;
	title_reinst)   echo "Neuinstallation" ;;
	title_remove)   echo "Deinstallation" ;;
	files_ok)       echo "Plugin-Dateien installiert" ;;
	files_bad)      echo "Plugin-Dateien unvollständig - bitte erneut installieren" ;;
	langs)          echo "Sprachen: %s" ;;
	kept)           echo "Einstellungen und Swap-Dateien bleiben erhalten" ;;
	swap_active)    echo "Swap aktiv: %s (%s MB)" ;;
	swap_none)      echo "Noch kein Swap aktiv" ;;
	ram)            echo "Arbeitsspeicher: %s MB" ;;
	zram_yes)       echo "zram (komprimierter RAM): unterstützt" ;;
	zram_no)        echo "zram (komprimierter RAM): von diesem Kernel nicht unterstützt" ;;
	restart)        echo "Bitte die GUI neu starten, um das Plugin zu laden:" ;;
	restart_upd)    echo "Bitte die GUI neu starten, um die neue Version zu laden:" ;;
	restart_rm)     echo "Bitte die GUI neu starten, damit das Plugin entladen wird:" ;;
	restart_menu)   echo "MENU > Standby / Neu starten > Bedienoberfläche neu starten" ;;
	restart_cmd)    echo "oder im Terminal:" ;;
	find_it)        echo "Danach findest du es im Plugin-Browser und unter" ;;
	find_path)      echo "MENU > Einstellungen > System > Datenträger > Simple Swap Manager" ;;
	rm_done)        echo "Plugin entfernt" ;;
	rm_swap_on)     echo "Swap-Datei bleibt bis zum nächsten Neustart aktiv: %s (%s MB)" ;;
	rm_swap_kept)   echo "Swap-Datei bleibt auf dem Laufwerk: %s" ;;
	rm_no_boot)     echo "Beim Start wird sie nicht mehr aktiviert." ;;
	rm_delete)      echo "Zum Löschen und Freigeben des Speicherplatzes:" ;;
	rm_zram)        echo "zram bleibt bis zum nächsten Neustart aktiv" ;;
	experimental)   echo "Experimentelle Version für DreamOS - bitte Probleme melden" ;;
	esac
}
