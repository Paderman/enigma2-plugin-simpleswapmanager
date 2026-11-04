# Eesti texts of the package scripts (generated)
msg_et() {
	case "$1" in
	title_install)   echo "Paigaldamine" ;;
	title_update)    echo "Uuendamine versioonilt %s versioonile %s" ;;
	title_reinst)    echo "Uuesti paigaldamine" ;;
	title_remove)    echo "Eemaldamine" ;;
	files_ok)        echo "Plugina failid paigaldatud" ;;
	files_bad)       echo "Plugina failid on puudulikud - palun paigalda uuesti" ;;
	langs)           echo "Keeled: %s" ;;
	kept)            echo "Seaded ja saalefailid jäävad alles" ;;
	swap_active)     echo "Saale aktiivne: %s (%s MB)" ;;
	swap_none)       echo "Saale pole veel aktiivne" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (pakitud RAM): toetatud" ;;
	zram_no)         echo "zram (pakitud RAM): see tuum ei toeta" ;;
	restart)         echo "Plugina laadimiseks taaskäivita kasutajaliides:" ;;
	restart_upd)     echo "Uue versiooni laadimiseks taaskäivita kasutajaliides:" ;;
	restart_rm)      echo "Plugina mälust eemaldamiseks taaskäivita kasutajaliides:" ;;
	restart_menu)    echo "MENU > Seiskamine > Enigma2 taaskäivitus" ;;
	restart_cmd)     echo "või terminalis:" ;;
	find_it)         echo "Seejärel leiad selle pluginate brauserist ja menüüst" ;;
	find_path)       echo "MENU > Seadistamine > Süsteem > Andmekandjad > Simple Swap Manager" ;;
	rm_done)         echo "Plugin eemaldatud" ;;
	rm_swap_on)      echo "Saalefail jääb aktiivseks järgmise taaskäivituseni: %s (%s MB)" ;;
	rm_swap_kept)    echo "Saalefail jääb andmekandjale: %s" ;;
	rm_no_boot)      echo "Käivitamisel seda enam ei aktiveerita." ;;
	rm_delete)       echo "Kustutamiseks ja kettaruumi vabastamiseks:" ;;
	rm_zram)         echo "zram jääb aktiivseks järgmise taaskäivituseni" ;;
	experimental)    echo "Eksperimentaalne versioon DreamOS-i jaoks - palun teata probleemidest" ;;
	esac
}
