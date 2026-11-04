# Svenska texts of the package scripts (generated)
msg_sv() {
	case "$1" in
	title_install)   echo "Installation" ;;
	title_update)    echo "Uppdatering från %s till %s" ;;
	title_reinst)    echo "Ominstallation" ;;
	title_remove)    echo "Avinstallation" ;;
	files_ok)        echo "Tilläggets filer installerade" ;;
	files_bad)       echo "Tilläggets filer är ofullständiga - installera igen" ;;
	langs)           echo "Språk: %s" ;;
	kept)            echo "Inställningar och växlingsfiler har behållits" ;;
	swap_active)     echo "Swap aktiv: %s (%s MB)" ;;
	swap_none)       echo "Ingen swap aktiv ännu" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (komprimerat RAM): stöds" ;;
	zram_no)         echo "zram (komprimerat RAM): stöds inte av den här kärnan" ;;
	restart)         echo "Starta om GUI för att ladda tillägget:" ;;
	restart_upd)     echo "Starta om GUI för att ladda den nya versionen:" ;;
	restart_rm)      echo "Starta om GUI för att avlasta tillägget:" ;;
	restart_menu)    echo "MENU > Standby / Omstart > Starta om gränssnitt" ;;
	restart_cmd)     echo "eller i terminalen:" ;;
	find_it)         echo "Därefter hittar du det i tilläggsbläddraren och under" ;;
	find_path)       echo "MENU > Setup > System > Lagringsenheter > Simple Swap Manager" ;;
	rm_done)         echo "Tillägget borttaget" ;;
	rm_swap_on)      echo "Växlingsfilen är aktiv till nästa omstart: %s (%s MB)" ;;
	rm_swap_kept)    echo "Växlingsfilen finns kvar på enheten: %s" ;;
	rm_no_boot)      echo "Den aktiveras inte längre vid start." ;;
	rm_delete)       echo "För att radera den och frigöra diskutrymme:" ;;
	rm_zram)         echo "zram är aktivt till nästa omstart" ;;
	experimental)   echo "Experimentell version för DreamOS - rapportera gärna problem" ;;
	esac
}
