# Magyar texts of the package scripts (generated)
msg_hu() {
	case "$1" in
	title_install)   echo "Telepítés" ;;
	title_update)    echo "Frissítés: %s -> %s" ;;
	title_reinst)    echo "Újratelepítés" ;;
	title_remove)    echo "Eltávolítás" ;;
	files_ok)        echo "Bővítményfájlok telepítve" ;;
	files_bad)       echo "Hiányos bővítményfájlok - telepítse újra" ;;
	langs)           echo "Nyelvek: %s" ;;
	kept)            echo "A beállítások és lapozófájlok megmaradtak" ;;
	swap_active)     echo "Aktív swap: %s (%s MB)" ;;
	swap_none)       echo "Még nincs aktív swap" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (tömörített RAM): támogatott" ;;
	zram_no)         echo "zram (tömörített RAM): ez a kernel nem támogatja" ;;
	restart)         echo "A bővítmény betöltéséhez indítsa újra a GUI-t:" ;;
	restart_upd)     echo "Az új verzió betöltéséhez indítsa újra a GUI-t:" ;;
	restart_rm)      echo "A bővítmény eltávolításához indítsa újra a GUI-t:" ;;
	restart_menu)    echo "MENU > Készenlét / Újraindítás > Kezelőfelület (GUI) újraindítása" ;;
	restart_cmd)     echo "vagy a terminálban:" ;;
	find_it)         echo "Ezután megtalálja a bővítményböngészőben és itt:" ;;
	find_path)       echo "MENU > Beállítások > Rendszer > Tárolóeszközök > Simple Swap Manager" ;;
	rm_done)         echo "Bővítmény eltávolítva" ;;
	rm_swap_on)      echo "A lapozófájl a következő újraindításig aktív marad: %s (%s MB)" ;;
	rm_swap_kept)    echo "A lapozófájl a meghajtón marad: %s" ;;
	rm_no_boot)      echo "Indításkor többé nem aktiválódik." ;;
	rm_delete)       echo "Törléshez és a lemezterület felszabadításához:" ;;
	rm_zram)         echo "A zram a következő újraindításig aktív marad" ;;
	experimental)   echo "Kísérleti változat DreamOS-hez - kérjük, jelezze a hibákat" ;;
	esac
}
