# Lietuvių texts of the package scripts (generated)
msg_lt() {
	case "$1" in
	title_install)   echo "Diegimas" ;;
	title_update)    echo "Atnaujinimas iš %s į %s" ;;
	title_reinst)    echo "Pakartotinis diegimas" ;;
	title_remove)    echo "Šalinimas" ;;
	files_ok)        echo "Įskiepio failai įdiegti" ;;
	files_bad)       echo "Įskiepio failai nepilni - įdiekite iš naujo" ;;
	langs)           echo "Kalbos: %s" ;;
	kept)            echo "Nustatymai ir mainų failai išsaugoti" ;;
	swap_active)     echo "Mainai aktyvūs: %s (%s MB)" ;;
	swap_none)       echo "Mainai dar neaktyvūs" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (suspausta RAM): palaikoma" ;;
	zram_no)         echo "zram (suspausta RAM): šis branduolys nepalaiko" ;;
	restart)         echo "Paleiskite sąsają iš naujo, kad įskiepis būtų įkeltas:" ;;
	restart_upd)     echo "Paleiskite sąsają iš naujo, kad būtų įkelta nauja versija:" ;;
	restart_rm)      echo "Paleiskite sąsają iš naujo, kad įskiepis būtų iškrautas:" ;;
	restart_menu)    echo "MENU > Išjungimo meniu > Paleisti iš naujo grafinę aplinką" ;;
	restart_cmd)     echo "arba terminale:" ;;
	find_it)         echo "Tada jį rasite įskiepių naršyklėje ir skiltyje" ;;
	find_path)       echo "MENU > Nustatymai > Sistema > Saugojimo įrenginiai > Simple Swap Manager" ;;
	rm_done)         echo "Įskiepis pašalintas" ;;
	rm_swap_on)      echo "Mainų failas lieka aktyvus iki kito paleidimo iš naujo: %s (%s MB)" ;;
	rm_swap_kept)    echo "Mainų failas lieka diske: %s" ;;
	rm_no_boot)      echo "Paleidžiant jis nebebus įjungiamas." ;;
	rm_delete)       echo "Norėdami jį ištrinti ir atlaisvinti vietą:" ;;
	rm_zram)         echo "zram lieka aktyvus iki kito paleidimo iš naujo" ;;
	experimental)    echo "Eksperimentinė versija DreamOS - praneškite apie problemas" ;;
	esac
}
