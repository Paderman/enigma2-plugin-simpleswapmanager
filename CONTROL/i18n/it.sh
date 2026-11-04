# Italiano texts of the package scripts (generated)
msg_it() {
	case "$1" in
	title_install)   echo "Installazione" ;;
	title_update)    echo "Aggiornamento da %s a %s" ;;
	title_reinst)    echo "Reinstallazione" ;;
	title_remove)    echo "Disinstallazione" ;;
	files_ok)        echo "File del plugin installati" ;;
	files_bad)       echo "File del plugin incompleti - reinstallare" ;;
	langs)           echo "Lingue: %s" ;;
	kept)            echo "Impostazioni e file di swap sono stati mantenuti" ;;
	swap_active)     echo "Swap attivo: %s (%s MB)" ;;
	swap_none)       echo "Nessuno swap ancora attivo" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (RAM compressa): supportato" ;;
	zram_no)         echo "zram (RAM compressa): non supportato da questo kernel" ;;
	restart)         echo "Riavvia la GUI per caricare il plugin:" ;;
	restart_upd)     echo "Riavvia la GUI per caricare la nuova versione:" ;;
	restart_rm)      echo "Riavvia la GUI per scaricare il plugin:" ;;
	restart_menu)    echo "MENU > Standby, riavvio o spegnimento > Riavvio grafica" ;;
	restart_cmd)     echo "oppure nel terminale:" ;;
	find_it)         echo "Poi lo trovi nel browser dei plugin e in" ;;
	find_path)       echo "MENU > Impostazioni > Sistema > Dispositivi di archiviazione > Simple Swap Manager" ;;
	rm_done)         echo "Plugin rimosso" ;;
	rm_swap_on)      echo "Il file di swap resta attivo fino al prossimo riavvio: %s (%s MB)" ;;
	rm_swap_kept)    echo "Il file di swap resta sul disco: %s" ;;
	rm_no_boot)      echo "Non verrà più attivato all'avvio." ;;
	rm_delete)       echo "Per eliminarlo e liberare lo spazio su disco:" ;;
	rm_zram)         echo "zram resta attivo fino al prossimo riavvio" ;;
	experimental)   echo "Versione sperimentale per DreamOS - segnala eventuali problemi" ;;
	esac
}
