# Українська texts of the package scripts (generated)
msg_uk() {
	case "$1" in
	title_install)   echo "Встановлення" ;;
	title_update)    echo "Оновлення з %s до %s" ;;
	title_reinst)    echo "Перевстановлення" ;;
	title_remove)    echo "Видалення" ;;
	files_ok)        echo "Файли плагіна встановлено" ;;
	files_bad)       echo "Файли плагіна неповні — встановіть знову" ;;
	langs)           echo "Мови: %s" ;;
	kept)            echo "Налаштування та файли підкачки збережено" ;;
	swap_active)     echo "Підкачка активна: %s (%s МБ)" ;;
	swap_none)       echo "Підкачка ще не активна" ;;
	ram)             echo "ОЗП: %s МБ" ;;
	zram_yes)        echo "zram (стиснена ОЗП): підтримується" ;;
	zram_no)         echo "zram (стиснена ОЗП): не підтримується цим ядром" ;;
	restart)         echo "Перезапустіть GUI, щоб завантажити плагін:" ;;
	restart_upd)     echo "Перезапустіть GUI, щоб завантажити нову версію:" ;;
	restart_rm)      echo "Перезапустіть GUI, щоб вивантажити плагін:" ;;
	restart_menu)    echo "MENU > Вимкнення > Перезавантаження GUI" ;;
	restart_cmd)     echo "або в терміналі:" ;;
	find_it)         echo "Потім ви знайдете його в браузері плагінів і в розділі" ;;
	find_path)       echo "MENU > Налаштування > Система > Пристрої зберігання > Simple Swap Manager" ;;
	rm_done)         echo "Плагін видалено" ;;
	rm_swap_on)      echo "Файл підкачки залишається активним до наступного перезавантаження: %s (%s МБ)" ;;
	rm_swap_kept)    echo "Файл підкачки залишається на накопичувачі: %s" ;;
	rm_no_boot)      echo "Під час запуску він більше не вмикатиметься." ;;
	rm_delete)       echo "Щоб видалити його та звільнити місце на диску:" ;;
	rm_zram)         echo "zram залишається активним до наступного перезавантаження" ;;
	experimental)   echo "Експериментальна версія для DreamOS — повідомляйте про проблеми" ;;
	esac
}
