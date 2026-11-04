# Български texts of the package scripts (generated)
msg_bg() {
	case "$1" in
	title_install)   echo "Инсталиране" ;;
	title_update)    echo "Обновяване от %s до %s" ;;
	title_reinst)    echo "Преинсталиране" ;;
	title_remove)    echo "Деинсталиране" ;;
	files_ok)        echo "Файловете на плъгина са инсталирани" ;;
	files_bad)       echo "Файловете на плъгина са непълни - моля, инсталирайте отново" ;;
	langs)           echo "Езици: %s" ;;
	kept)            echo "Настройките и суап файловете са запазени" ;;
	swap_active)     echo "Активен суап: %s (%s MB)" ;;
	swap_none)       echo "Все още няма активен суап" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (компресирана RAM): поддържа се" ;;
	zram_no)         echo "zram (компресирана RAM): не се поддържа от това ядро" ;;
	restart)         echo "Рестартирайте графичния интерфейс, за да заредите плъгина:" ;;
	restart_upd)     echo "Рестартирайте графичния интерфейс, за да заредите новата версия:" ;;
	restart_rm)      echo "Рестартирайте графичния интерфейс, за да разтоварите плъгина:" ;;
	restart_menu)    echo "MENU > Standby / Рестарт > Рестарт графичен интерфейс" ;;
	restart_cmd)     echo "или в терминала:" ;;
	find_it)         echo "След това ще го намерите в браузъра за плъгини и в" ;;
	find_path)       echo "MENU > Настройка > Система > Устройства за съхранение > Simple Swap Manager" ;;
	rm_done)         echo "Плъгинът е премахнат" ;;
	rm_swap_on)      echo "Суап файлът остава активен до следващия рестарт: %s (%s MB)" ;;
	rm_swap_kept)    echo "Суап файлът остава на устройството: %s" ;;
	rm_no_boot)      echo "При стартиране вече няма да се активира." ;;
	rm_delete)       echo "За да го изтриете и освободите място:" ;;
	rm_zram)         echo "zram остава активен до следващия рестарт" ;;
	experimental)    echo "Експериментална версия за DreamOS - моля, съобщавайте за проблеми" ;;
	esac
}
