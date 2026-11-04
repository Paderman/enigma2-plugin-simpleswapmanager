# Latviešu texts of the package scripts (generated)
msg_lv() {
	case "$1" in
	title_install)   echo "Instalēšana" ;;
	title_update)    echo "Atjaunināšana no %s uz %s" ;;
	title_reinst)    echo "Pārinstalēšana" ;;
	title_remove)    echo "Atinstalēšana" ;;
	files_ok)        echo "Spraudņa faili instalēti" ;;
	files_bad)       echo "Spraudņa faili nav pilnīgi - lūdzu, instalējiet vēlreiz" ;;
	langs)           echo "Valodas: %s" ;;
	kept)            echo "Iestatījumi un mijmaiņas faili saglabāti" ;;
	swap_active)     echo "Mijmaiņa aktīva: %s (%s MB)" ;;
	swap_none)       echo "Mijmaiņa vēl nav aktīva" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (saspiesta RAM): atbalstīts" ;;
	zram_no)         echo "zram (saspiesta RAM): šis kodols neatbalsta" ;;
	restart)         echo "Restartējiet saskarni, lai ielādētu spraudni:" ;;
	restart_upd)     echo "Restartējiet saskarni, lai ielādētu jauno versiju:" ;;
	restart_rm)      echo "Restartējiet saskarni, lai izlādētu spraudni:" ;;
	restart_menu)    echo "MENU > Gaidstāve / Restartēt > Restart GUI" ;;
	restart_cmd)     echo "vai terminālī:" ;;
	find_it)         echo "Pēc tam to atradīsiet spraudņu pārlūkā un sadaļā" ;;
	find_path)       echo "MENU > Iestatne > Sistēma > Storage Devices > Simple Swap Manager" ;;
	rm_done)         echo "Spraudnis noņemts" ;;
	rm_swap_on)      echo "Mijmaiņas fails paliek aktīvs līdz nākamajai restartēšanai: %s (%s MB)" ;;
	rm_swap_kept)    echo "Mijmaiņas fails paliek diskā: %s" ;;
	rm_no_boot)      echo "Startējot tas vairs netiks aktivizēts." ;;
	rm_delete)       echo "Lai to dzēstu un atbrīvotu vietu diskā:" ;;
	rm_zram)         echo "zram paliek aktīvs līdz nākamajai restartēšanai" ;;
	experimental)    echo "Eksperimentāla versija DreamOS - lūdzu, ziņojiet par problēmām" ;;
	esac
}
