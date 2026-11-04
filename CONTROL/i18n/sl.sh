# Slovenščina texts of the package scripts (generated)
msg_sl() {
	case "$1" in
	title_install)   echo "Namestitev" ;;
	title_update)    echo "Posodobitev s %s na %s" ;;
	title_reinst)    echo "Ponovna namestitev" ;;
	title_remove)    echo "Odstranitev" ;;
	files_ok)        echo "Datoteke vtičnika so nameščene" ;;
	files_bad)       echo "Datoteke vtičnika niso popolne - namestite znova" ;;
	langs)           echo "Jeziki: %s" ;;
	kept)            echo "Nastavitve in izmenjalne datoteke so ohranjene" ;;
	swap_active)     echo "Izmenjava aktivna: %s (%s MB)" ;;
	swap_none)       echo "Izmenjava še ni aktivna" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (stisnjen RAM): podprto" ;;
	zram_no)         echo "zram (stisnjen RAM): to jedro ne podpira" ;;
	restart)         echo "Znova zaženite vmesnik, da se vtičnik naloži:" ;;
	restart_upd)     echo "Znova zaženite vmesnik, da se naloži nova različica:" ;;
	restart_rm)      echo "Znova zaženite vmesnik, da se vtičnik odstrani iz pomnilnika:" ;;
	restart_menu)    echo "MENU > Možnosti izklopa sprejemnika > Restart GUI" ;;
	restart_cmd)     echo "ali v terminalu:" ;;
	find_it)         echo "Nato ga najdete v brskalniku vtičnikov in pod" ;;
	find_path)       echo "MENU > Nastavitve > Sistem > Storage Devices > Simple Swap Manager" ;;
	rm_done)         echo "Vtičnik odstranjen" ;;
	rm_swap_on)      echo "Izmenjalna datoteka ostane aktivna do naslednjega ponovnega zagona: %s (%s MB)" ;;
	rm_swap_kept)    echo "Izmenjalna datoteka ostane na pogonu: %s" ;;
	rm_no_boot)      echo "Ob zagonu se ne bo več aktivirala." ;;
	rm_delete)       echo "Za brisanje in sprostitev prostora na disku:" ;;
	rm_zram)         echo "zram ostane aktiven do naslednjega ponovnega zagona" ;;
	experimental)    echo "Preizkusna različica za DreamOS - prosimo, sporočite težave" ;;
	esac
}
