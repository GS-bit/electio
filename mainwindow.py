from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QInputDialog, QLineEdit, QListWidgetItem, QMainWindow, QMessageBox, QPushButton
)
from PyQt6 import uic, QtCore

from database import Database
from scores import get_candidates_by_score

class MainWindow(QMainWindow):
    def __init__(self, db: Database):
        """
        This class represents the main window of the program.
        """

        super().__init__()

        self.db = db

        uic.loadUi("electio.ui", self)

        candidates = self.db.fetch_candidates()

        for candidate in candidates:
            item = QListWidgetItem(candidate["name"])
            item.setData(QtCore.Qt.ItemDataRole.UserRole, candidate["id"])

            self.candidates_list.addItem(item)

        if self.candidates_list.count() > 0:
            self.candidates_list.setCurrentRow(0)

        self.handle_candidate_selection()

        self.setup_signals()

    def setup_signals(self) -> None:
        """
        It process the signals of the window.
        """

        self.new_candidate_btn.clicked.connect(self.handle_new_candidate)
        self.candidates_list.itemSelectionChanged.connect(self.handle_candidate_selection)
        self.save_btn.clicked.connect(self.handle_update_candidate)
        self.delete_btn.clicked.connect(self.handle_delete_candidate)

        self.add_schedule_btn.clicked.connect(self.handle_new_schedule)

        self.tab_widget.currentChanged.connect(self.handle_tab_changed)

        self.action_about.triggered.connect(self.show_about_dialog)
        self.action_exit.triggered.connect(self.close)

    def refresh_candidates_list(self) -> None:
        """
        It refreshes the UI list of candidates.
        """

        self.candidates_list.clear()
        candidates = self.db.fetch_candidates()

        if candidates is not None:
            for candidate in candidates:
                item = QListWidgetItem(candidate["name"])
                item.setData(QtCore.Qt.ItemDataRole.UserRole, candidate["id"])
                self.candidates_list.addItem(item)

    def refresh_schedules_list(self) -> None:
        """
        It refreshes the UI list of schedules.
        """

        self.schedules_list.clear()
        """
        candidates = self.db.fetch_candidates()

        if candidates is not None:
            for candidate in candidates:
                item = QListWidgetItem(candidate["name"])
                item.setData(QtCore.Qt.ItemDataRole.UserRole, candidate["id"])
                self.schedules_list.addItem(item)
        """

    def handle_new_candidate(self) -> None:
        """
        It handles the creation of a new candidate.
        """

        name, is_okay = QInputDialog.getText(self, "Novo candidato", "Nome do candidato:")

        if name and is_okay:
            self.db.create_candidate(name)

        self.refresh_candidates_list()

    def handle_candidate_selection(self) -> None:
        """
        It handles the candidate selection.
        """

        selected_item = self.candidates_list.selectedItems()

        if not selected_item:
            return

        candidate = self.db.read_candidate(selected_item[0].data(QtCore.Qt.ItemDataRole.UserRole))

        if candidate is not None:
            self.name_lineedit.setText(str(candidate["name"] or ""))
            self.age_lineedit.setText(str(candidate["age"] or ""))
            self.email_lineedit.setText(str(candidate["email"] or ""))
            self.phone_lineedit.setText(str(candidate["phone"] or ""))
            self.github_lineedit.setText(str(candidate["github"] or ""))
            self.linkedin_lineedit.setText(str(candidate["linkedin"] or ""))
            sex_text = "Masculino" if candidate["sex"] == "M" else "Feminino"
            self.sex_cmbbox.setCurrentText(sex_text)
            self.period_cmbbox.setCurrentText(str(candidate["current_period"] or ""))
            self.indication_checkbox.setChecked(bool(candidate["indication"]))
            self.personal_desc_txtedit.setPlainText(str(candidate["personal_description"] or ""))
            self.qualities_txtedit.setPlainText(str(candidate["qualities"] or ""))
            self.defects_txtedit.setPlainText(str(candidate["defects"] or ""))
            self.why_work_txtedit.setPlainText(str(candidate["why_wants_to_work"] or ""))
            self.frontend_lineedit.setText(str(candidate["front_end_score"] or ""))
            self.backend_lineedit.setText(str(candidate["back_end_score"] or ""))
            self.english_lineedit.setText(str(candidate["english_score"] or ""))
            self.proactivity_lineedit.setText(str(candidate["proactivity_score"] or ""))
            self.resilience_lineedit.setText(str(candidate["resilience_score"] or ""))
            self.communication_lineedit.setText(str(candidate["communicative_skills_score"] or ""))
            self.group_work_lineedit.setText(str(candidate["group_work_score"] or ""))

    def handle_update_candidate(self) -> None:
        """
        It handles the update of a candidate.
        """

        selected_item = self.candidates_list.selectedItems()

        if not selected_item:
            return

        _id = selected_item[0].data(QtCore.Qt.ItemDataRole.UserRole)

        name = self.name_lineedit.text()
        age = self.age_lineedit.text()
        sex = "M" if self.sex_cmbbox.currentText() == "Masculino" else "F"
        current_period = self.period_cmbbox.currentText()
        indication = "1" if hasattr(self.indication_checkbox, 'isChecked') and self.indication_checkbox.isChecked() else "0"
        email = self.email_lineedit.text()
        phone = self.phone_lineedit.text()
        github = self.github_lineedit.text()
        linkedin = self.linkedin_lineedit.text()
        personal_description = self.personal_desc_txtedit.toPlainText()
        qualities = self.qualities_txtedit.toPlainText()
        defects = self.defects_txtedit.toPlainText()
        why_wants_to_work = self.why_work_txtedit.toPlainText()
        front_end_score = self.frontend_lineedit.text()
        back_end_score = self.backend_lineedit.text()
        english_score = self.english_lineedit.text()
        proactivity_score = self.proactivity_lineedit.text()
        resilience_score = self.resilience_lineedit.text()
        communicative_skills_score = self.communication_lineedit.text()
        group_work_score = self.group_work_lineedit.text()

        schedules = ["10:00-11:00"]

        self.db.update_candidate(_id, name, age, sex, current_period, indication, email, phone, github, linkedin, personal_description, qualities, defects, why_wants_to_work, front_end_score, back_end_score,
                                english_score, proactivity_score, resilience_score, communicative_skills_score, group_work_score, schedules)

        self.refresh_candidates_list()

    def handle_delete_candidate(self) -> None:
        """
        It handles the deletion of a candidate.
        """

        selected_item = self.candidates_list.selectedItems()

        if not selected_item:
            return

        _id = selected_item[0].data(QtCore.Qt.ItemDataRole.UserRole)

        self.db.delete_candidate(_id)

        if self.candidates_list.count() > 0:
            self.candidates_list.setCurrentRow(0)

        self.refresh_candidates_list()

    def handle_new_candidate(self) -> None:
        """
        It handles the creation of a new candidate.
        """

        name, is_okay = QInputDialog.getText(self, "Novo candidato", "Nome do candidato:")

        if name and is_okay:
            self.db.create_candidate(name)

        self.refresh_candidates_list()

    def handle_new_schedule(self) -> None:
        """
        It handles the creation of a new schedule.
        """

        dialog = QDialog()
        dialog.setWindowTitle("Adicionar horário")

        hour_start = QLineEdit()
        hour_start.setInputMask("99:99")
        hour_end = QLineEdit()
        hour_end.setInputMask("99:99")

        confirm_btn = QPushButton("OK")

        selected_candidate = self.candidates_list.selectedItems()

        if not selected_candidate:
            return None

        _id = selected_candidate[0].data(QtCore.Qt.ItemDataRole.UserRole)

        confirm_btn.clicked.connect(lambda: [
                self.db.create_schedule(_id, f"{hour_start.text()}-{hour_end.text()}"),
                dialog.accept()
            ]
        )

        layout = QFormLayout()
        layout.addRow("Horário inicial:", hour_start)
        layout.addRow("Horário final:", hour_end)
        layout.addWidget(confirm_btn)

        dialog.setLayout(layout)

        dialog.show()

        #self.refresh_schedules_list()

    def handle_schedule_selection(self) -> None:
        """
        It handles the schedule selection.
        """

        selected_item = self.candidates_list.selectedItems()

        if not selected_item:
            return

        candidate = self.db.read_candidate(selected_item[0].data(QtCore.Qt.ItemDataRole.UserRole))

        if candidate is not None:
            self.name_lineedit.setText(str(candidate["name"] or ""))
            self.age_lineedit.setText(str(candidate["age"] or ""))
            self.email_lineedit.setText(str(candidate["email"] or ""))
            self.phone_lineedit.setText(str(candidate["phone"] or ""))
            self.github_lineedit.setText(str(candidate["github"] or ""))
            self.linkedin_lineedit.setText(str(candidate["linkedin"] or ""))
            sex_text = "Masculino" if candidate["sex"] == "M" else "Feminino"
            self.sex_cmbbox.setCurrentText(sex_text)
            self.period_cmbbox.setCurrentText(str(candidate["current_period"] or ""))
            self.indication_checkbox.setChecked(bool(candidate["indication"]))
            self.personal_desc_txtedit.setPlainText(str(candidate["personal_description"] or ""))
            self.qualities_txtedit.setPlainText(str(candidate["qualities"] or ""))
            self.defects_txtedit.setPlainText(str(candidate["defects"] or ""))
            self.why_work_txtedit.setPlainText(str(candidate["why_wants_to_work"] or ""))
            self.frontend_lineedit.setText(str(candidate["front_end_score"] or ""))
            self.backend_lineedit.setText(str(candidate["back_end_score"] or ""))
            self.english_lineedit.setText(str(candidate["english_score"] or ""))
            self.proactivity_lineedit.setText(str(candidate["proactivity_score"] or ""))
            self.resilience_lineedit.setText(str(candidate["resilience_score"] or ""))
            self.communication_lineedit.setText(str(candidate["communicative_skills_score"] or ""))
            self.group_work_lineedit.setText(str(candidate["group_work_score"] or ""))

    def handle_update_schedule(self) -> None:
        """
        It handles the update of a candidate.
        """

        selected_item = self.candidates_list.selectedItems()

        if not selected_item:
            return

        _id = selected_item[0].data(QtCore.Qt.ItemDataRole.UserRole)

        name = self.name_lineedit.text()
        age = self.age_lineedit.text()
        sex = "M" if self.sex_cmbbox.currentText() == "Masculino" else "F"
        current_period = self.period_cmbbox.currentText()
        indication = "1" if hasattr(self.indication_checkbox, 'isChecked') and self.indication_checkbox.isChecked() else "0"
        email = self.email_lineedit.text()
        phone = self.phone_lineedit.text()
        github = self.github_lineedit.text()
        linkedin = self.linkedin_lineedit.text()
        personal_description = self.personal_desc_txtedit.toPlainText()
        qualities = self.qualities_txtedit.toPlainText()
        defects = self.defects_txtedit.toPlainText()
        why_wants_to_work = self.why_work_txtedit.toPlainText()
        front_end_score = self.frontend_lineedit.text()
        back_end_score = self.backend_lineedit.text()
        english_score = self.english_lineedit.text()
        proactivity_score = self.proactivity_lineedit.text()
        resilience_score = self.resilience_lineedit.text()
        communicative_skills_score = self.communication_lineedit.text()
        group_work_score = self.group_work_lineedit.text()

        schedules = ["10:00-11:00"]

        self.db.update_candidate(_id, name, age, sex, current_period, indication, email, phone, github, linkedin, personal_description, qualities, defects, why_wants_to_work, front_end_score, back_end_score,
                                english_score, proactivity_score, resilience_score, communicative_skills_score, group_work_score, schedules)

        self.refresh_candidates_list()

    def handle_delete_schedule(self) -> None:
        """
        It handles the deletion of a schedule.
        """

        selected_item = self.candidates_list.selectedItems()

        if not selected_item:
            return

        _id = selected_item[0].data(QtCore.Qt.ItemDataRole.UserRole)

        self.db.delete_candidate(_id)

        if self.candidates_list.count() > 0:
            self.candidates_list.setCurrentRow(0)

        self.refresh_candidates_list()


    def handle_tab_changed(self, index: int) -> None:
        """
        It handles the change of tab on the QTabWidget.
        """

        candidates = get_candidates_by_score(self.db)

        scores = ""

        for candidate in candidates:
            scores += f"<p><span style='font-size: 16px'><b>{candidate[0]["name"]}: </b><br />{candidate[1]}<br /><br /></span><span style='font-size: 16px; color: #8A2BE2'>[front-end: {candidate[0]["front_end_score"]}]&nbsp;&nbsp;&nbsp; [back-end: {candidate[0]["back_end_score"]}]&nbsp;&nbsp;&nbsp; [inglês: {candidate[0]["english_score"]}]&nbsp;&nbsp;&nbsp; [proatividade: {candidate[0]["proactivity_score"]}]<br />[resiliência: {candidate[0]["resilience_score"]}]&nbsp;&nbsp;&nbsp; [comunicação: {candidate[0]["communicative_skills_score"]}]&nbsp;&nbsp;&nbsp; [trabalho em equipe: {candidate[0]["group_work_score"]}]</span><br /><br /></p>"

        self.scores_label.setText(scores)

    def show_about_dialog(self) -> None:
        """
        It shows the about dialog.
        """

        QMessageBox.information(
            self,
            "Sobre o Electio",
            "Electio - Programa para gerenciamento de processos seletivos.\nVersão 1.0\n"
        )

