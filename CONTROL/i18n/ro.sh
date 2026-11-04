# Română texts of the package scripts (generated)
msg_ro() {
	case "$1" in
	title_install)   echo "Instalare" ;;
	title_update)    echo "Actualizare de la %s la %s" ;;
	title_reinst)    echo "Reinstalare" ;;
	title_remove)    echo "Dezinstalare" ;;
	files_ok)        echo "Fișierele pluginului au fost instalate" ;;
	files_bad)       echo "Fișierele pluginului sunt incomplete - reinstalați" ;;
	langs)           echo "Limbi: %s" ;;
	kept)            echo "Setările și fișierele swap au fost păstrate" ;;
	swap_active)     echo "Swap activ: %s (%s MB)" ;;
	swap_none)       echo "Încă nu există swap activ" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (RAM comprimată): suportat" ;;
	zram_no)         echo "zram (RAM comprimată): nesuportat de acest kernel" ;;
	restart)         echo "Reporniți GUI pentru a încărca pluginul:" ;;
	restart_upd)     echo "Reporniți GUI pentru a încărca noua versiune:" ;;
	restart_rm)      echo "Reporniți GUI pentru a descărca pluginul:" ;;
	restart_menu)    echo "MENU > Asteptare / Restart > Restart GUI" ;;
	restart_cmd)     echo "sau în terminal:" ;;
	find_it)         echo "Apoi îl găsiți în navigatorul de pluginuri și în" ;;
	find_path)       echo "MENU > Configurare > Sistem > Storage Devices > Simple Swap Manager" ;;
	rm_done)         echo "Plugin eliminat" ;;
	rm_swap_on)      echo "Fișierul swap rămâne activ până la următoarea repornire: %s (%s MB)" ;;
	rm_swap_kept)    echo "Fișierul swap rămâne pe unitate: %s" ;;
	rm_no_boot)      echo "Nu va mai fi activat la pornire." ;;
	rm_delete)       echo "Pentru a-l șterge și a elibera spațiul pe disc:" ;;
	rm_zram)         echo "zram rămâne activ până la următoarea repornire" ;;
	experimental)   echo "Versiune experimentală pentru DreamOS - raportați problemele" ;;
	esac
}
