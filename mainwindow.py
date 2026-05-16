from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from database import Database

class MainWindow(QMainWindow):
    def __init__(self, db: Database):
        """
        This class represents the main window of the program.
        """

        super().__init__()

        self.db = db

        uic.loadUi("electio.ui", self)

        self.setup_signals()

    def setup_signals(self) -> None:
        """
        It process the signals of the window.
        """

        pass


