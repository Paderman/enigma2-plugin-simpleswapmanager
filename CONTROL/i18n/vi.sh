# Tiếng Việt texts of the package scripts (generated)
msg_vi() {
	case "$1" in
	title_install)   echo "Cài đặt" ;;
	title_update)    echo "Cập nhật từ %s lên %s" ;;
	title_reinst)    echo "Cài đặt lại" ;;
	title_remove)    echo "Gỡ cài đặt" ;;
	files_ok)        echo "Đã cài đặt các tệp plugin" ;;
	files_bad)       echo "Tệp plugin không đầy đủ - vui lòng cài đặt lại" ;;
	langs)           echo "Ngôn ngữ: %s" ;;
	kept)            echo "Cài đặt và tệp hoán đổi được giữ nguyên" ;;
	swap_active)     echo "Hoán đổi đang hoạt động: %s (%s MB)" ;;
	swap_none)       echo "Chưa có hoán đổi nào hoạt động" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (RAM nén): được hỗ trợ" ;;
	zram_no)         echo "zram (RAM nén): kernel này không hỗ trợ" ;;
	restart)         echo "Hãy khởi động lại giao diện để nạp plugin:" ;;
	restart_upd)     echo "Hãy khởi động lại giao diện để nạp phiên bản mới:" ;;
	restart_rm)      echo "Hãy khởi động lại giao diện để dỡ plugin:" ;;
	restart_menu)    echo "MENU > Chờ / Khởi động lại > Khởi động lại GUI" ;;
	restart_cmd)     echo "hoặc trong terminal:" ;;
	find_it)         echo "Sau đó bạn sẽ thấy nó trong trình duyệt plugin và tại" ;;
	find_path)       echo "MENU > Cài đặt > Hệ thống > Thiết bị lưu trữ > Simple Swap Manager" ;;
	rm_done)         echo "Đã gỡ plugin" ;;
	rm_swap_on)      echo "Tệp hoán đổi vẫn hoạt động đến lần khởi động lại tiếp theo: %s (%s MB)" ;;
	rm_swap_kept)    echo "Tệp hoán đổi vẫn nằm trên ổ đĩa: %s" ;;
	rm_no_boot)      echo "Nó sẽ không còn được kích hoạt khi khởi động." ;;
	rm_delete)       echo "Để xóa và giải phóng dung lượng đĩa:" ;;
	rm_zram)         echo "zram vẫn hoạt động đến lần khởi động lại tiếp theo" ;;
	experimental)    echo "Phiên bản thử nghiệm cho DreamOS - vui lòng báo lỗi" ;;
	esac
}
