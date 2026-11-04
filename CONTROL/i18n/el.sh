# Ελληνικά texts of the package scripts (generated)
msg_el() {
	case "$1" in
	title_install)   echo "Εγκατάσταση" ;;
	title_update)    echo "Ενημέρωση από %s σε %s" ;;
	title_reinst)    echo "Επανεγκατάσταση" ;;
	title_remove)    echo "Απεγκατάσταση" ;;
	files_ok)        echo "Τα αρχεία του πρόσθετου εγκαταστάθηκαν" ;;
	files_bad)       echo "Ελλιπή αρχεία πρόσθετου - εγκαταστήστε ξανά" ;;
	langs)           echo "Γλώσσες: %s" ;;
	kept)            echo "Οι ρυθμίσεις και τα αρχεία swap διατηρήθηκαν" ;;
	swap_active)     echo "Ενεργό swap: %s (%s MB)" ;;
	swap_none)       echo "Δεν υπάρχει ακόμη ενεργό swap" ;;
	ram)             echo "RAM: %s MB" ;;
	zram_yes)        echo "zram (συμπιεσμένη RAM): υποστηρίζεται" ;;
	zram_no)         echo "zram (συμπιεσμένη RAM): δεν υποστηρίζεται από αυτόν τον πυρήνα" ;;
	restart)         echo "Επανεκκινήστε το GUI για να φορτωθεί το πρόσθετο:" ;;
	restart_upd)     echo "Επανεκκινήστε το GUI για να φορτωθεί η νέα έκδοση:" ;;
	restart_rm)      echo "Επανεκκινήστε το GUI για να αποφορτωθεί το πρόσθετο:" ;;
	restart_menu)    echo "MENU > Αναμονή / Επανεκκίνηση > Επανεκκίνηση διεπαφής χρήστη" ;;
	restart_cmd)     echo "ή στο τερματικό:" ;;
	find_it)         echo "Μετά θα το βρείτε στον περιηγητή πρόσθετων και στο" ;;
	find_path)       echo "MENU > Ρυθμίσεις > Σύστημα > Συσκευές αποθήκευσης > Simple Swap Manager" ;;
	rm_done)         echo "Το πρόσθετο αφαιρέθηκε" ;;
	rm_swap_on)      echo "Το αρχείο swap μένει ενεργό έως την επόμενη επανεκκίνηση: %s (%s MB)" ;;
	rm_swap_kept)    echo "Το αρχείο swap παραμένει στον δίσκο: %s" ;;
	rm_no_boot)      echo "Δεν θα ενεργοποιείται πλέον στην εκκίνηση." ;;
	rm_delete)       echo "Για διαγραφή και απελευθέρωση χώρου:" ;;
	rm_zram)         echo "Το zram μένει ενεργό έως την επόμενη επανεκκίνηση" ;;
	experimental)   echo "Πειραματική έκδοση για DreamOS - αναφέρετε τυχόν προβλήματα" ;;
	esac
}
