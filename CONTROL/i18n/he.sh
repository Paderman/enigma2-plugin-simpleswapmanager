# עברית texts of the package scripts (generated)
msg_he() {
	case "$1" in
	title_install)   echo "התקנה" ;;
	title_update)    echo "עדכון מ-%s ל-%s" ;;
	title_reinst)    echo "התקנה מחדש" ;;
	title_remove)    echo "הסרה" ;;
	files_ok)        echo "קובצי התוסף הותקנו" ;;
	files_bad)       echo "קובצי התוסף אינם שלמים - נא להתקין מחדש" ;;
	langs)           echo "שפות: %s" ;;
	kept)            echo "ההגדרות וקובצי ההחלפה נשמרו" ;;
	swap_active)     echo "החלפה פעילה: %s (%s MB)" ;;
	swap_none)       echo "עדיין אין החלפה פעילה" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (RAM דחוס): נתמך" ;;
	zram_no)         echo "zram (RAM דחוס): לא נתמך בליבה זו" ;;
	restart)         echo "הפעילו מחדש את הממשק כדי לטעון את התוסף:" ;;
	restart_upd)     echo "הפעילו מחדש את הממשק כדי לטעון את הגרסה החדשה:" ;;
	restart_rm)      echo "הפעילו מחדש את הממשק כדי לפרוק את התוסף:" ;;
	restart_menu)    echo "MENU > איתחול / המתנה > Restart GUI" ;;
	restart_cmd)     echo "או במסוף:" ;;
	find_it)         echo "לאחר מכן תמצאו אותו בדפדפן התוספים ותחת" ;;
	find_path)       echo "MENU > הגדרות > מערכת > Storage Devices > Simple Swap Manager" ;;
	rm_done)         echo "התוסף הוסר" ;;
	rm_swap_on)      echo "קובץ ההחלפה נשאר פעיל עד ההפעלה מחדש הבאה: %s (%s MB)" ;;
	rm_swap_kept)    echo "קובץ ההחלפה נשאר בכונן: %s" ;;
	rm_no_boot)      echo "הוא לא יופעל עוד בהפעלה." ;;
	rm_delete)       echo "כדי למחוק אותו ולשחרר שטח דיסק:" ;;
	rm_zram)         echo "zram נשאר פעיל עד ההפעלה מחדש הבאה" ;;
	experimental)    echo "גרסה ניסיונית ל-DreamOS - נא לדווח על בעיות" ;;
	esac
}
