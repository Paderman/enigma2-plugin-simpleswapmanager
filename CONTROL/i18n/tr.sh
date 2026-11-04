# Türkçe texts of the package scripts (generated)
msg_tr() {
	case "$1" in
	title_install)   echo "Kurulum" ;;
	title_update)    echo "%s sürümünden %s sürümüne güncelleme" ;;
	title_reinst)    echo "Yeniden kurulum" ;;
	title_remove)    echo "Kaldırma" ;;
	files_ok)        echo "Eklenti dosyaları kuruldu" ;;
	files_bad)       echo "Eklenti dosyaları eksik - lütfen yeniden kurun" ;;
	langs)           echo "Diller: %s" ;;
	kept)            echo "Ayarlar ve takas dosyaları korundu" ;;
	swap_active)     echo "Takas etkin: %s (%s MB)" ;;
	swap_none)       echo "Henüz etkin takas yok" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (sıkıştırılmış RAM): destekleniyor" ;;
	zram_no)         echo "zram (sıkıştırılmış RAM): bu çekirdek tarafından desteklenmiyor" ;;
	restart)         echo "Eklentiyi yüklemek için lütfen GUI'yi yeniden başlatın:" ;;
	restart_upd)     echo "Yeni sürümü yüklemek için lütfen GUI'yi yeniden başlatın:" ;;
	restart_rm)      echo "Eklentiyi kaldırmak için lütfen GUI'yi yeniden başlatın:" ;;
	restart_menu)    echo "MENU > Bekleme / Yeniden Başlat > Kullanıcı Arayüzünü Yeniden Başlat" ;;
	restart_cmd)     echo "veya terminalde:" ;;
	find_it)         echo "Daha sonra eklenti tarayıcısında ve şurada bulabilirsiniz:" ;;
	find_path)       echo "MENU > Kurulum > Sistem > Depolama Cihazları > Simple Swap Manager" ;;
	rm_done)         echo "Eklenti kaldırıldı" ;;
	rm_swap_on)      echo "Takas dosyası bir sonraki yeniden başlatmaya kadar etkin kalır: %s (%s MB)" ;;
	rm_swap_kept)    echo "Takas dosyası sürücüde kalır: %s" ;;
	rm_no_boot)      echo "Açılışta artık etkinleştirilmeyecek." ;;
	rm_delete)       echo "Silmek ve disk alanını boşaltmak için:" ;;
	rm_zram)         echo "zram bir sonraki yeniden başlatmaya kadar etkin kalır" ;;
	experimental)   echo "DreamOS için deneysel sürüm - lütfen sorunları bildirin" ;;
	esac
}
