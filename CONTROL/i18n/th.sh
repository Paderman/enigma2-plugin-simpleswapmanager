# ไทย texts of the package scripts (generated)
msg_th() {
	case "$1" in
	title_install)   echo "การติดตั้ง" ;;
	title_update)    echo "อัปเดตจาก %s เป็น %s" ;;
	title_reinst)    echo "ติดตั้งใหม่" ;;
	title_remove)    echo "ถอนการติดตั้ง" ;;
	files_ok)        echo "ติดตั้งไฟล์ปลั๊กอินแล้ว" ;;
	files_bad)       echo "ไฟล์ปลั๊กอินไม่ครบ - โปรดติดตั้งใหม่" ;;
	langs)           echo "ภาษา: %s" ;;
	kept)            echo "การตั้งค่าและไฟล์สว็อปยังคงอยู่" ;;
	swap_active)     echo "สว็อปทำงานอยู่: %s (%s MB)" ;;
	swap_none)       echo "ยังไม่มีสว็อปที่ทำงาน" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (RAM แบบบีบอัด): รองรับ" ;;
	zram_no)         echo "zram (RAM แบบบีบอัด): เคอร์เนลนี้ไม่รองรับ" ;;
	restart)         echo "โปรดรีสตาร์ท GUI เพื่อโหลดปลั๊กอิน:" ;;
	restart_upd)     echo "โปรดรีสตาร์ท GUI เพื่อโหลดเวอร์ชันใหม่:" ;;
	restart_rm)      echo "โปรดรีสตาร์ท GUI เพื่อนำปลั๊กอินออกจากหน่วยความจำ:" ;;
	restart_menu)    echo "MENU > ปิดเครื่อง > Restart GUI" ;;
	restart_cmd)     echo "หรือในเทอร์มินัล:" ;;
	find_it)         echo "จากนั้นจะพบได้ในเบราว์เซอร์ปลั๊กอินและที่" ;;
	find_path)       echo "MENU > ตั้งค่า > ระบบ > Storage Devices > Simple Swap Manager" ;;
	rm_done)         echo "ลบปลั๊กอินแล้ว" ;;
	rm_swap_on)      echo "ไฟล์สว็อปยังทำงานจนกว่าจะรีสตาร์ทครั้งถัดไป: %s (%s MB)" ;;
	rm_swap_kept)    echo "ไฟล์สว็อปยังอยู่บนไดรฟ์: %s" ;;
	rm_no_boot)      echo "จะไม่ถูกเปิดใช้งานเมื่อเริ่มระบบอีก" ;;
	rm_delete)       echo "หากต้องการลบและคืนพื้นที่ดิสก์:" ;;
	rm_zram)         echo "zram ยังทำงานจนกว่าจะรีสตาร์ทครั้งถัดไป" ;;
	experimental)    echo "เวอร์ชันทดลองสำหรับ DreamOS - โปรดแจ้งปัญหา" ;;
	esac
}
