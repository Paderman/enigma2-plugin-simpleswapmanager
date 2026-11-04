# Português texts of the package scripts (generated)
msg_pt() {
	case "$1" in
	title_install)   echo "Instalação" ;;
	title_update)    echo "Atualização de %s para %s" ;;
	title_reinst)    echo "Reinstalação" ;;
	title_remove)    echo "Desinstalação" ;;
	files_ok)        echo "Ficheiros do plugin instalados" ;;
	files_bad)       echo "Ficheiros do plugin incompletos - instale novamente" ;;
	langs)           echo "Idiomas: %s" ;;
	kept)            echo "As definições e os ficheiros de swap foram mantidos" ;;
	swap_active)     echo "Swap ativo: %s (%s MB)" ;;
	swap_none)       echo "Ainda não há swap ativo" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (RAM comprimida): suportado" ;;
	zram_no)         echo "zram (RAM comprimida): não suportado por este kernel" ;;
	restart)         echo "Reinicie a GUI para carregar o plugin:" ;;
	restart_upd)     echo "Reinicie a GUI para carregar a nova versão:" ;;
	restart_rm)      echo "Reinicie a GUI para descarregar o plugin:" ;;
	restart_menu)    echo "MENU > Standby / Reiniciar > Reiniciar interface" ;;
	restart_cmd)     echo "ou no terminal:" ;;
	find_it)         echo "Depois encontra-o no navegador de plugins e em" ;;
	find_path)       echo "MENU > Definições > Sistema > Dispositivos de armazenamento > Simple Swap Manager" ;;
	rm_done)         echo "Plugin removido" ;;
	rm_swap_on)      echo "O ficheiro de swap fica ativo até ao próximo reinício: %s (%s MB)" ;;
	rm_swap_kept)    echo "O ficheiro de swap fica na unidade: %s" ;;
	rm_no_boot)      echo "Deixará de ser ativado no arranque." ;;
	rm_delete)       echo "Para o apagar e libertar espaço em disco:" ;;
	rm_zram)         echo "O zram fica ativo até ao próximo reinício" ;;
	experimental)   echo "Versão experimental para DreamOS - comunique os problemas" ;;
	esac
}
