# Dansk texts of the package scripts (generated)
msg_da() {
	case "$1" in
	title_install)   echo "Installation" ;;
	title_update)    echo "Opdatering fra %s til %s" ;;
	title_reinst)    echo "Geninstallation" ;;
	title_remove)    echo "Afinstallation" ;;
	files_ok)        echo "Pluginfiler installeret" ;;
	files_bad)       echo "Pluginfiler ufuldstændige - installer igen" ;;
	langs)           echo "Sprog: %s" ;;
	kept)            echo "Indstillinger og swapfiler er bevaret" ;;
	swap_active)     echo "Swap aktiv: %s (%s MB)" ;;
	swap_none)       echo "Ingen swap aktiv endnu" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (komprimeret RAM): understøttes" ;;
	zram_no)         echo "zram (komprimeret RAM): understøttes ikke af denne kerne" ;;
	restart)         echo "Genstart GUI for at indlæse pluginet:" ;;
	restart_upd)     echo "Genstart GUI for at indlæse den nye version:" ;;
	restart_rm)      echo "Genstart GUI for at fjerne pluginet fra hukommelsen:" ;;
	restart_menu)    echo "MENU > Afbryd / Genstart > Genstart GUI" ;;
	restart_cmd)     echo "eller i terminalen:" ;;
	find_it)         echo "Derefter finder du det i pluginbrowseren og under" ;;
	find_path)       echo "MENU > Opsætning > System > Lagerenheder > Simple Swap Manager" ;;
	rm_done)         echo "Plugin fjernet" ;;
	rm_swap_on)      echo "Swapfilen forbliver aktiv indtil næste genstart: %s (%s MB)" ;;
	rm_swap_kept)    echo "Swapfilen bliver på drevet: %s" ;;
	rm_no_boot)      echo "Den aktiveres ikke længere ved opstart." ;;
	rm_delete)       echo "For at slette den og frigøre diskplads:" ;;
	rm_zram)         echo "zram forbliver aktiv indtil næste genstart" ;;
	experimental)   echo "Eksperimentel version til DreamOS - rapportér venligst problemer" ;;
	esac
}
