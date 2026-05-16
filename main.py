import sys

from PyQt6.QtWidgets import QApplication

from database import Database
from mainwindow import MainWindow

def main() -> None:
    """
    It begins the execution of the program.
    """

    db = Database()

    app = QApplication(sys.argv)

    window = MainWindow(db=db)
    window.show()

    sys.exit_code = app.exec()

    db.close_connection()

if __name__ == "__main__":
    main()
