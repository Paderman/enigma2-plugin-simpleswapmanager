# Français texts of the package scripts (generated)
msg_fr() {
	case "$1" in
	title_install)   echo "Installation" ;;
	title_update)    echo "Mise à jour de %s vers %s" ;;
	title_reinst)    echo "Réinstallation" ;;
	title_remove)    echo "Désinstallation" ;;
	files_ok)        echo "Fichiers du plugin installés" ;;
	files_bad)       echo "Fichiers du plugin incomplets - veuillez réinstaller" ;;
	langs)           echo "Langues : %s" ;;
	kept)            echo "Les paramètres et fichiers d'échange sont conservés" ;;
	swap_active)     echo "Swap actif : %s (%s Mo)" ;;
	swap_none)       echo "Aucun swap actif pour l'instant" ;;
	ram)             echo "Mémoire vive : %s Mo" ;;
	zram_yes)        echo "zram (RAM compressée) : pris en charge" ;;
	zram_no)         echo "zram (RAM compressée) : non pris en charge par ce noyau" ;;
	restart)         echo "Veuillez redémarrer l'interface pour charger le plugin :" ;;
	restart_upd)     echo "Veuillez redémarrer l'interface pour charger la nouvelle version :" ;;
	restart_rm)      echo "Veuillez redémarrer l'interface pour décharger le plugin :" ;;
	restart_menu)    echo "MENU > Veille / Redémarrage > Relancer l'IGU" ;;
	restart_cmd)     echo "ou dans le terminal :" ;;
	find_it)         echo "Vous le trouverez ensuite dans le navigateur de plugins et sous" ;;
	find_path)       echo "MENU > Paramétrer > Système > Liste des Périphériques de Stockage > Simple Swap Manager" ;;
	rm_done)         echo "Plugin supprimé" ;;
	rm_swap_on)      echo "Le fichier d'échange reste actif jusqu'au prochain redémarrage : %s (%s Mo)" ;;
	rm_swap_kept)    echo "Le fichier d'échange reste sur le disque : %s" ;;
	rm_no_boot)      echo "Il ne sera plus activé au démarrage." ;;
	rm_delete)       echo "Pour le supprimer et libérer l'espace disque :" ;;
	rm_zram)         echo "zram reste actif jusqu'au prochain redémarrage" ;;
	experimental)   echo "Version expérimentale pour DreamOS - merci de signaler les problèmes" ;;
	esac
}
