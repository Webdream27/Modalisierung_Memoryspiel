""" ************************************************
Eine Klasse fuer Memorykarten
************************************************"""
# die Module importieren
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon

# die Klasse für die Spielkarten
# sie erbt von QTableWidgetItem
class Memorykarte(QTableWidgetItem):
    # die magische Methode __init__()
    def __init__(self, vorne, nummer):
        # die magische Methode __init__() der Übergeordneten Klasse aufrufen
        super().__init__()
        # die Vorderseite
        # der Dateiname des Bildes wird übergeben
        self.bild_vorne = QIcon(vorne)
        # die Rückseite ist festgesetzt
        self.bild_hinten = QIcon("bilder/back.bmp")
        # die Rückseite wird angezeigt
        self.setIcon(self.bild_hinten)

        # die Karte ist nicht umgedreht
        self.umgedreht = False
        # die Karte ist noch im Spiel
        self.noch_im_spiel = True
        # die Nummer setzen
        self.bild_ID = nummer
        # die Bildposition ist erst einmal 0
        self.bild_pos = 0

    # die Methoden
    # zum umdrehen
    def umdrehen(self):
        # ist die Karte schon umgedreht?
        # dann die Rückseite anzeigen, aber nur dann, wenn die Karte noch im Spiel ist
        if self.noch_im_spiel == True:
            if self.umgedreht == True:
                self.setIcon(self.bild_hinten)
                self.umgedreht = False
            # sonst die Vorderseite zeigen
            else:
                self.setIcon(self.bild_vorne)
                self.umgedreht = True

    # die Karte aus dem Spiel nehmen
    def rausnehmen(self):
        # die Grafik für aufgedeckt zeigen
        self.setIcon(QIcon("bilder/aufgedeckt.bmp"))
        self.noch_im_spiel = False

    # die Bild-ID liefern
    def get_bild_ID(self):
        return self.bild_ID

    # die Position liefern
    def get_bild_pos(self):
        return self.bild_pos

    # die Position setzen
    def set_bild_pos(self, position):
        self.bild_pos = position

    # den Status von noch_im_spiel liefern
    def get_noch_im_spiel(self):
        return self.noch_im_spiel

    # den Status von umgedreht liefern
    def get_umgedreht(self):
        return self.umgedreht

