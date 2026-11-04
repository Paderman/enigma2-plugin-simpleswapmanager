# Norsk bokmål texts of the package scripts (generated)
msg_nb() {
	case "$1" in
	title_install)   echo "Installasjon" ;;
	title_update)    echo "Oppdatering fra %s til %s" ;;
	title_reinst)    echo "Reinstallasjon" ;;
	title_remove)    echo "Avinstallering" ;;
	files_ok)        echo "Programtilleggets filer installert" ;;
	files_bad)       echo "Programtilleggets filer er ufullstendige - installer på nytt" ;;
	langs)           echo "Språk: %s" ;;
	kept)            echo "Innstillinger og vekselfiler er beholdt" ;;
	swap_active)     echo "Swap aktiv: %s (%s MB)" ;;
	swap_none)       echo "Ingen swap aktiv ennå" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (komprimert RAM): støttes" ;;
	zram_no)         echo "zram (komprimert RAM): støttes ikke av denne kjernen" ;;
	restart)         echo "Start GUI på nytt for å laste programtillegget:" ;;
	restart_upd)     echo "Start GUI på nytt for å laste den nye versjonen:" ;;
	restart_rm)      echo "Start GUI på nytt for å fjerne programtillegget fra minnet:" ;;
	restart_menu)    echo "MENU > Standby / Restart > Start grafisk grensesnitt på ny" ;;
	restart_cmd)     echo "eller i terminalen:" ;;
	find_it)         echo "Deretter finner du det i programtilleggsleseren og under" ;;
	find_path)       echo "MENU > Innstilling > System > Storage Devices > Simple Swap Manager" ;;
	rm_done)         echo "Programtillegg fjernet" ;;
	rm_swap_on)      echo "Vekselfilen forblir aktiv til neste omstart: %s (%s MB)" ;;
	rm_swap_kept)    echo "Vekselfilen blir liggende på stasjonen: %s" ;;
	rm_no_boot)      echo "Den aktiveres ikke lenger ved oppstart." ;;
	rm_delete)       echo "For å slette den og frigjøre diskplass:" ;;
	rm_zram)         echo "zram forblir aktiv til neste omstart" ;;
	experimental)   echo "Eksperimentell versjon for DreamOS - meld gjerne fra om problemer" ;;
	esac
}
