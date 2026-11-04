# Srpski texts of the package scripts (generated)
msg_sr() {
	case "$1" in
	title_install)   echo "Instalacija" ;;
	title_update)    echo "Ažuriranje sa %s na %s" ;;
	title_reinst)    echo "Ponovna instalacija" ;;
	title_remove)    echo "Deinstalacija" ;;
	files_ok)        echo "Datoteke dodatka instalirane" ;;
	files_bad)       echo "Datoteke dodatka nisu potpune - instalirajte ponovo" ;;
	langs)           echo "Jezici: %s" ;;
	kept)            echo "Podešavanja i swap datoteke su zadržani" ;;
	swap_active)     echo "Swap aktivan: %s (%s MB)" ;;
	swap_none)       echo "Swap još nije aktivan" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (sažeti RAM): podržano" ;;
	zram_no)         echo "zram (sažeti RAM): ovo jezgro ne podržava" ;;
	restart)         echo "Ponovo pokrenite interfejs da bi se dodatak učitao:" ;;
	restart_upd)     echo "Ponovo pokrenite interfejs da bi se učitala nova verzija:" ;;
	restart_rm)      echo "Ponovo pokrenite interfejs da bi se dodatak uklonio iz memorije:" ;;
	restart_menu)    echo "MENU > Pripravnost / Ponovno Pokretanje > Ponovo pokreni GUI" ;;
	restart_cmd)     echo "ili u terminalu:" ;;
	find_it)         echo "Zatim ćete ga naći u pregledaču dodataka i pod" ;;
	find_path)       echo "MENU > Podešavanje > Sistem > Uređaj za Skladištenje > Simple Swap Manager" ;;
	rm_done)         echo "Dodatak uklonjen" ;;
	rm_swap_on)      echo "Swap datoteka ostaje aktivna do sledećeg ponovnog pokretanja: %s (%s MB)" ;;
	rm_swap_kept)    echo "Swap datoteka ostaje na disku: %s" ;;
	rm_no_boot)      echo "Pri pokretanju se više neće aktivirati." ;;
	rm_delete)       echo "Za brisanje i oslobađanje prostora na disku:" ;;
	rm_zram)         echo "zram ostaje aktivan do sledećeg ponovnog pokretanja" ;;
	experimental)    echo "Eksperimentalna verzija za DreamOS - prijavite probleme" ;;
	esac
}
