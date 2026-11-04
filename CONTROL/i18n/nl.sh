# Nederlands texts of the package scripts (generated)
msg_nl() {
	case "$1" in
	title_install)   echo "Installatie" ;;
	title_update)    echo "Update van %s naar %s" ;;
	title_reinst)    echo "Herinstallatie" ;;
	title_remove)    echo "Verwijdering" ;;
	files_ok)        echo "Pluginbestanden geïnstalleerd" ;;
	files_bad)       echo "Pluginbestanden onvolledig - installeer opnieuw" ;;
	langs)           echo "Talen: %s" ;;
	kept)            echo "Instellingen en swapbestanden zijn behouden" ;;
	swap_active)     echo "Swap actief: %s (%s MB)" ;;
	swap_none)       echo "Nog geen swap actief" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (gecomprimeerd RAM): ondersteund" ;;
	zram_no)         echo "zram (gecomprimeerd RAM): niet ondersteund door deze kernel" ;;
	restart)         echo "Herstart de GUI om de plugin te laden:" ;;
	restart_upd)     echo "Herstart de GUI om de nieuwe versie te laden:" ;;
	restart_rm)      echo "Herstart de GUI om de plugin te ontladen:" ;;
	restart_menu)    echo "MENU > Afsluiten > Herstart Enigma2" ;;
	restart_cmd)     echo "of in de terminal:" ;;
	find_it)         echo "Daarna vindt u het in de pluginbrowser en onder" ;;
	find_path)       echo "MENU > Instellingen > Systeem > Opslagmedia > Simple Swap Manager" ;;
	rm_done)         echo "Plugin verwijderd" ;;
	rm_swap_on)      echo "Het swapbestand blijft actief tot de volgende herstart: %s (%s MB)" ;;
	rm_swap_kept)    echo "Het swapbestand blijft op de schijf: %s" ;;
	rm_no_boot)      echo "Het wordt bij het opstarten niet meer geactiveerd." ;;
	rm_delete)       echo "Om het te verwijderen en schijfruimte vrij te maken:" ;;
	rm_zram)         echo "zram blijft actief tot de volgende herstart" ;;
	experimental)   echo "Experimentele versie voor DreamOS - meld problemen a.u.b." ;;
	esac
}
