# Polski texts of the package scripts (generated)
msg_pl() {
	case "$1" in
	title_install)   echo "Instalacja" ;;
	title_update)    echo "Aktualizacja z %s do %s" ;;
	title_reinst)    echo "Ponowna instalacja" ;;
	title_remove)    echo "Odinstalowanie" ;;
	files_ok)        echo "Pliki wtyczki zainstalowane" ;;
	files_bad)       echo "Pliki wtyczki niekompletne - zainstaluj ponownie" ;;
	langs)           echo "Języki: %s" ;;
	kept)            echo "Ustawienia i pliki wymiany zostały zachowane" ;;
	swap_active)     echo "Aktywny swap: %s (%s MB)" ;;
	swap_none)       echo "Brak aktywnego swap" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (skompresowany RAM): obsługiwany" ;;
	zram_no)         echo "zram (skompresowany RAM): nieobsługiwany przez to jądro" ;;
	restart)         echo "Uruchom ponownie GUI, aby załadować wtyczkę:" ;;
	restart_upd)     echo "Uruchom ponownie GUI, aby załadować nową wersję:" ;;
	restart_rm)      echo "Uruchom ponownie GUI, aby wyładować wtyczkę:" ;;
	restart_menu)    echo "MENU > Czuwanie / Restart > Restart interfejsu" ;;
	restart_cmd)     echo "lub w terminalu:" ;;
	find_it)         echo "Potem znajdziesz ją w przeglądarce wtyczek oraz w" ;;
	find_path)       echo "MENU > Ustawienia > System > Urządzenia pamięci masowej > Simple Swap Manager" ;;
	rm_done)         echo "Wtyczka usunięta" ;;
	rm_swap_on)      echo "Plik wymiany pozostaje aktywny do następnego restartu: %s (%s MB)" ;;
	rm_swap_kept)    echo "Plik wymiany pozostaje na dysku: %s" ;;
	rm_no_boot)      echo "Nie będzie już aktywowany przy starcie." ;;
	rm_delete)       echo "Aby go usunąć i zwolnić miejsce na dysku:" ;;
	rm_zram)         echo "zram pozostaje aktywny do następnego restartu" ;;
	experimental)   echo "Wersja eksperymentalna dla DreamOS - prosimy zgłaszać problemy" ;;
	esac
}
