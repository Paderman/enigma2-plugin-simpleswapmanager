# Slovenčina texts of the package scripts (generated)
msg_sk() {
	case "$1" in
	title_install)   echo "Inštalácia" ;;
	title_update)    echo "Aktualizácia z %s na %s" ;;
	title_reinst)    echo "Preinštalovanie" ;;
	title_remove)    echo "Odinštalovanie" ;;
	files_ok)        echo "Súbory pluginu nainštalované" ;;
	files_bad)       echo "Súbory pluginu sú neúplné - nainštalujte znova" ;;
	langs)           echo "Jazyky: %s" ;;
	kept)            echo "Nastavenia a odkladacie súbory zostali zachované" ;;
	swap_active)     echo "Swap aktívny: %s (%s MB)" ;;
	swap_none)       echo "Zatiaľ nie je aktívny žiadny swap" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (komprimovaná RAM): podporované" ;;
	zram_no)         echo "zram (komprimovaná RAM): toto jadro nepodporuje" ;;
	restart)         echo "Reštartujte GUI, aby sa plugin načítal:" ;;
	restart_upd)     echo "Reštartujte GUI, aby sa načítala nová verzia:" ;;
	restart_rm)      echo "Reštartujte GUI, aby sa plugin uvoľnil:" ;;
	restart_menu)    echo "MENU > Vypnutie / Reštart > Reštartovať GUI" ;;
	restart_cmd)     echo "alebo v termináli:" ;;
	find_it)         echo "Potom ho nájdete v prehliadači pluginov a v" ;;
	find_path)       echo "MENU > Nastavenia > Systém > Úložné zariadenia > Simple Swap Manager" ;;
	rm_done)         echo "Plugin odobraný" ;;
	rm_swap_on)      echo "Odkladací súbor zostane aktívny do ďalšieho reštartu: %s (%s MB)" ;;
	rm_swap_kept)    echo "Odkladací súbor zostáva na disku: %s" ;;
	rm_no_boot)      echo "Pri štarte sa už nebude aktivovať." ;;
	rm_delete)       echo "Na zmazanie a uvoľnenie miesta na disku:" ;;
	rm_zram)         echo "zram zostane aktívny do ďalšieho reštartu" ;;
	experimental)   echo "Experimentálna verzia pre DreamOS - hláste prosím problémy" ;;
	esac
}
