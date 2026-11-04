# Русский texts of the package scripts (generated)
msg_ru() {
	case "$1" in
	title_install)   echo "Установка" ;;
	title_update)    echo "Обновление с %s до %s" ;;
	title_reinst)    echo "Переустановка" ;;
	title_remove)    echo "Удаление" ;;
	files_ok)        echo "Файлы плагина установлены" ;;
	files_bad)       echo "Файлы плагина неполные — установите заново" ;;
	langs)           echo "Языки: %s" ;;
	kept)            echo "Настройки и файлы подкачки сохранены" ;;
	swap_active)     echo "Подкачка активна: %s (%s МБ)" ;;
	swap_none)       echo "Подкачка пока не активна" ;;
	ram)             echo "ОЗУ: %s МБ" ;;
	zram_yes)        echo "zram (сжатая ОЗУ): поддерживается" ;;
	zram_no)         echo "zram (сжатая ОЗУ): не поддерживается этим ядром" ;;
	restart)         echo "Перезапустите GUI, чтобы загрузить плагин:" ;;
	restart_upd)     echo "Перезапустите GUI, чтобы загрузить новую версию:" ;;
	restart_rm)      echo "Перезапустите GUI, чтобы выгрузить плагин:" ;;
	restart_menu)    echo "MENU > Выключение > Перезагрузить в GUI" ;;
	restart_cmd)     echo "или в терминале:" ;;
	find_it)         echo "Затем вы найдёте его в браузере плагинов и в разделе" ;;
	find_path)       echo "MENU > Настройка > Система > Устройства хранения > Simple Swap Manager" ;;
	rm_done)         echo "Плагин удалён" ;;
	rm_swap_on)      echo "Файл подкачки остаётся активным до следующей перезагрузки: %s (%s МБ)" ;;
	rm_swap_kept)    echo "Файл подкачки остаётся на накопителе: %s" ;;
	rm_no_boot)      echo "При запуске он больше не будет включаться." ;;
	rm_delete)       echo "Чтобы удалить его и освободить место на диске:" ;;
	rm_zram)         echo "zram остаётся активным до следующей перезагрузки" ;;
	experimental)   echo "Экспериментальная версия для DreamOS — сообщайте о проблемах" ;;
	esac
}
