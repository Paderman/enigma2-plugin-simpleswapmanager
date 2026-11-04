# Español texts of the package scripts (generated)
msg_es() {
	case "$1" in
	title_install)   echo "Instalación" ;;
	title_update)    echo "Actualización de %s a %s" ;;
	title_reinst)    echo "Reinstalación" ;;
	title_remove)    echo "Desinstalación" ;;
	files_ok)        echo "Archivos del plugin instalados" ;;
	files_bad)       echo "Archivos del plugin incompletos - vuelva a instalar" ;;
	langs)           echo "Idiomas: %s" ;;
	kept)            echo "Se conservan los ajustes y los archivos de intercambio" ;;
	swap_active)     echo "Swap activo: %s (%s MB)" ;;
	swap_none)       echo "Todavía no hay swap activo" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (RAM comprimida): compatible" ;;
	zram_no)         echo "zram (RAM comprimida): este kernel no lo admite" ;;
	restart)         echo "Reinicie la GUI para cargar el plugin:" ;;
	restart_upd)     echo "Reinicie la GUI para cargar la nueva versión:" ;;
	restart_rm)      echo "Reinicie la GUI para descargar el plugin:" ;;
	restart_menu)    echo "MENU > Apagado / Reinicio > Reiniciar interfaz" ;;
	restart_cmd)     echo "o en el terminal:" ;;
	find_it)         echo "Después lo encontrará en el navegador de plugins y en" ;;
	find_path)       echo "MENU > Configuración > Sistema > Dispositivos de almacenamiento > Simple Swap Manager" ;;
	rm_done)         echo "Plugin eliminado" ;;
	rm_swap_on)      echo "El archivo de intercambio sigue activo hasta el próximo reinicio: %s (%s MB)" ;;
	rm_swap_kept)    echo "El archivo de intercambio queda en la unidad: %s" ;;
	rm_no_boot)      echo "Ya no se activará al inicio." ;;
	rm_delete)       echo "Para borrarlo y liberar el espacio en disco:" ;;
	rm_zram)         echo "zram sigue activo hasta el próximo reinicio" ;;
	experimental)   echo "Versión experimental para DreamOS - informe de los problemas" ;;
	esac
}
