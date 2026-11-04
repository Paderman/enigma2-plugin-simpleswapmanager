# العربية texts of the package scripts (generated)
msg_ar() {
	case "$1" in
	title_install)   echo "التثبيت" ;;
	title_update)    echo "التحديث من %s إلى %s" ;;
	title_reinst)    echo "إعادة التثبيت" ;;
	title_remove)    echo "إلغاء التثبيت" ;;
	files_ok)        echo "تم تثبيت ملفات الإضافة" ;;
	files_bad)       echo "ملفات الإضافة غير مكتملة - يرجى إعادة التثبيت" ;;
	langs)           echo "اللغات: %s" ;;
	kept)            echo "تم الاحتفاظ بالإعدادات وملفات التبديل" ;;
	swap_active)     echo "التبديل نشط: %s (%s MB)" ;;
	swap_none)       echo "لا يوجد تبديل نشط بعد" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (ذاكرة مضغوطة): مدعوم" ;;
	zram_no)         echo "zram (ذاكرة مضغوطة): غير مدعوم في هذه النواة" ;;
	restart)         echo "أعد تشغيل الواجهة لتحميل الإضافة:" ;;
	restart_upd)     echo "أعد تشغيل الواجهة لتحميل الإصدار الجديد:" ;;
	restart_rm)      echo "أعد تشغيل الواجهة لإزالة الإضافة من الذاكرة:" ;;
	restart_menu)    echo "MENU > وضع الاستعداد/إعاده التشغيل > إعادة تشغيل الواجهة الرسومية (GUI)" ;;
	restart_cmd)     echo "أو في الطرفية:" ;;
	find_it)         echo "بعد ذلك تجدها في متصفح الإضافات وفي" ;;
	find_path)       echo "MENU > الضبط > النظام > Storage Devices > Simple Swap Manager" ;;
	rm_done)         echo "تمت إزالة الإضافة" ;;
	rm_swap_on)      echo "يبقى ملف التبديل نشطًا حتى إعادة التشغيل التالية: %s (%s MB)" ;;
	rm_swap_kept)    echo "يبقى ملف التبديل على وحدة التخزين: %s" ;;
	rm_no_boot)      echo "لن يتم تفعيله عند بدء التشغيل بعد الآن." ;;
	rm_delete)       echo "لحذفه وتحرير مساحة القرص:" ;;
	rm_zram)         echo "يبقى zram نشطًا حتى إعادة التشغيل التالية" ;;
	experimental)    echo "إصدار تجريبي لـ DreamOS - يرجى الإبلاغ عن المشاكل" ;;
	esac
}
