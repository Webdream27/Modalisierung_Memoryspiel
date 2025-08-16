""" 
Modul das die Hauptklasse und Logik des Memoryspiels enthaelt.

"""
# die Module importieren
from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QLabel, QMessageBox
from PyQt5.QtCore import QSize, QTimer
import random
# Das Modul für die Karten-Klasse wird importiert
import memorykarte

# eine Klasse für das Spiel
# sie erbt von QWidget
class Memoryspiel(QWidget):
    # die magische Methode __init__()
    def __init__(self):
        # die magische Methode __init__() der Uebergeordneten Klasse aufrufen
        super().__init__()
        # den Text setzen
        self.setWindowTitle("Memoryspiel")
        # die Groesse anpassen
        self.resize(394, 550)

        # den Timer erstellen
        self.timer_umdrehen = QTimer(self)
        self.timer_umdrehen.setSingleShot(True)
        self.umgedrehte_karten = 0
        self.spieler = 0
        self.mensch_punkte = 0
        self.computer_punkte = 0
        self.gemerkte_karten = [[-1] * 21 for index in range(2)]
        self.paar = [None, None]
        self.spielstaerke = 10
        self.spielfeld = QTableWidget(7, 6, self)
        self.spielfeld.horizontalHeader().hide()
        self.spielfeld.verticalHeader().hide()
        self.spielfeld.setShowGrid(False)
        self.spielfeld.setSelectionMode(QTableWidget.NoSelection)
        self.spielfeld.setEditTriggers(QAbstractItemView.NoEditTriggers)

        zeilen = range(0, 7)
        spalten = range(0, 6)
        for zeile in zeilen:
            self.spielfeld.setRowHeight(zeile, 64)
        for spalte in spalten:
            self.spielfeld.setColumnWidth(spalte, 64)

        self.timer_umdrehen.timeout.connect(self.timer_slot)
        self.spielfeld.cellClicked.connect(self.maus_klick_slot)
        self.spielfeld.resize(386, 450)

        self.label_text_mensch =  QLabel("Mensch", self)
        self.label_text_mensch.setGeometry(10, 460, 60, 25)
        self.label_mensch =  QLabel("0", self)
        self.label_mensch.setGeometry(80, 460, 60, 25)
        self.label_text_computer =  QLabel("Computer", self)
        self.label_text_computer.setGeometry(10, 480, 60, 25)
        self.label_computer =  QLabel("0", self)
        self.label_computer.setGeometry(80, 480, 60, 25)

        self.bild_namen = [
            "bilder/apfel.bmp", "bilder/birne.bmp", "bilder/blume.bmp", "bilder/blume2.bmp", 
            "bilder/ente.bmp", "bilder/fisch.bmp", "bilder/fuchs.bmp", "bilder/igel.bmp", 
            "bilder/kaenguruh.bmp", "bilder/katze.bmp", "bilder/kuh.bmp", "bilder/maus1.bmp", 
            "bilder/maus2.bmp", "bilder/maus3.bmp", "bilder/melone.bmp", "bilder/pilz.bmp", 
            "bilder/ronny.bmp", "bilder/schmetterling.bmp", "bilder/sonne.bmp", "bilder/wolke.bmp", 
            "bilder/maus4.bmp"
        ]

        self.karten = []
        bild_zaehler = 0
        schleife = 0
        while schleife < 42:
            self.karten.append(memorykarte.Memorykarte(self.bild_namen[bild_zaehler], bild_zaehler))
            if (schleife + 1) % 2 == 0:
                bild_zaehler += 1
            schleife += 1

        random.shuffle(self.karten)
        self.spielfeld.setIconSize(QSize(64, 64))

        karten_index = 0
        for zeile in zeilen:
            for spalte in spalten:
                self.spielfeld.setItem(zeile, spalte, self.karten[karten_index])
                self.karten[karten_index].set_bild_pos(karten_index)
                karten_index += 1

    def maus_klick_slot(self, zeile, spalte):
        karten_index = spalte * 7 + zeile 
        if self.zug_erlaubt():
            if not self.karten[karten_index].get_umgedreht() and self.karten[karten_index].get_noch_im_spiel():
                self.karten[karten_index].umdrehen()
                self.karte_oeffnen(self.karten[karten_index])

    def timer_slot(self):
        self.karte_schliessen()

    def karte_oeffnen(self, karte):
        self.paar[self.umgedrehte_karten] = karte
        karten_id = karte.get_bild_ID()
        karten_pos = karte.get_bild_pos()
        if self.gemerkte_karten[0][karten_id] == -1:
            self.gemerkte_karten[0][karten_id] = karten_pos
        elif self.gemerkte_karten[0][karten_id] != karten_pos:
            self.gemerkte_karten[1][karten_id] = karten_pos

        self.umgedrehte_karten += 1

        if self.umgedrehte_karten == 2:
            self.paar_pruefen(karten_id)
            self.timer_umdrehen.start(2000)
        if self.mensch_punkte + self.computer_punkte == 21:
            self.timer_umdrehen.stop()
            QMessageBox.information(self, "Spielende", "Das Spiel ist vorbei")
            self.close()

    def paar_pruefen(self, karten_id):
        if self.paar[0].get_bild_ID() == self.paar[1].get_bild_ID():
            self.paar_gefunden()
            self.gemerkte_karten[0][karten_id] = -2
            self.gemerkte_karten[1][karten_id] = -2

    def paar_gefunden(self):
        if self.spieler == 0:
            self.mensch_punkte += 1
            self.label_mensch.setNum(self.mensch_punkte)
        else:
            self.computer_punkte += 1
            self.label_computer.setNum(self.computer_punkte)

    def karte_schliessen(self):
        raus = False
        if self.paar[0].get_bild_ID() == self.paar[1].get_bild_ID():
            self.paar[0].rausnehmen()
            self.paar[1].rausnehmen()
            raus = True
        else:
            self.paar[0].umdrehen()
            self.paar[1].umdrehen()
        self.umgedrehte_karten = 0
        if not raus:
            self.spieler_wechseln()
        elif self.spieler == 1:
            self.computer_zug()

    def spieler_wechseln(self):
        if self.spieler == 0:
            self.spieler = 1
            self.computer_zug()
        else:
            self.spieler = 0

    def computer_zug(self):
        
        pass

    def zug_erlaubt(self):

        return self.spieler == 0 and self.umgedrehte_karten < 2
