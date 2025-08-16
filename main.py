"""
Hauptprogramm zum Starten des Memory-Spiels.
"""
import sys
from PyQt5.QtWidgets import QApplication
# Die Klasse für das Spielfeld wird aus dem Modul spielfeld importiert
from spielfeld import Memoryspiel

# eine Instanz der Klasse QApplication erzeugen
app = QApplication(sys.argv)
# eine Instanz unseres Fensters erzeugen
fenster = Memoryspiel()
# das Fenster anzeigen
fenster.show()
# die Anwendung ausführen und auf ein sauberes Beenden warten
sys.exit(app.exec_())

