# Suomi texts of the package scripts (generated)
msg_fi() {
	case "$1" in
	title_install)   echo "Asennus" ;;
	title_update)    echo "Päivitys versiosta %s versioon %s" ;;
	title_reinst)    echo "Uudelleenasennus" ;;
	title_remove)    echo "Asennuksen poisto" ;;
	files_ok)        echo "Laajennuksen tiedostot asennettu" ;;
	files_bad)       echo "Laajennuksen tiedostot puutteelliset - asenna uudelleen" ;;
	langs)           echo "Kielet: %s" ;;
	kept)            echo "Asetukset ja sivutustiedostot säilytettiin" ;;
	swap_active)     echo "Swap aktiivinen: %s (%s Mt)" ;;
	swap_none)       echo "Swap ei ole vielä käytössä" ;;
	ram)             echo "RAM: %s Mt" ;;
	zram_yes)        echo "zram (pakattu RAM): tuettu" ;;
	zram_no)         echo "zram (pakattu RAM): tämä ydin ei tue" ;;
	restart)         echo "Käynnistä GUI uudelleen laajennuksen lataamiseksi:" ;;
	restart_upd)     echo "Käynnistä GUI uudelleen uuden version lataamiseksi:" ;;
	restart_rm)      echo "Käynnistä GUI uudelleen laajennuksen poistamiseksi muistista:" ;;
	restart_menu)    echo "MENU > Sammutusvalikko > Käynnistä järjestelmä uudelleen" ;;
	restart_cmd)     echo "tai päätteessä:" ;;
	find_it)         echo "Sen jälkeen löydät sen laajennusselaimesta ja kohdasta" ;;
	find_path)       echo "MENU > Asetukset > Järjestelmä > Tallennusvälineet > Simple Swap Manager" ;;
	rm_done)         echo "Laajennus poistettu" ;;
	rm_swap_on)      echo "Sivutustiedosto pysyy käytössä seuraavaan uudelleenkäynnistykseen asti: %s (%s Mt)" ;;
	rm_swap_kept)    echo "Sivutustiedosto jää asemalle: %s" ;;
	rm_no_boot)      echo "Sitä ei enää oteta käyttöön käynnistyksessä." ;;
	rm_delete)       echo "Poistaaksesi sen ja vapauttaaksesi levytilaa:" ;;
	rm_zram)         echo "zram pysyy käytössä seuraavaan uudelleenkäynnistykseen asti" ;;
	experimental)   echo "Kokeellinen versio DreamOS:lle - ilmoita ongelmista" ;;
	esac
}
