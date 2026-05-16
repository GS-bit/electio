import sqlite3
import os

class Database:
    def __init__(self):
        """
        This class establishes the connection to the database and handles the necessary operations for the working of the program.
        """
        self.connection = sqlite3.connect("electio.db")
        self.cursor = self.connection.cursor()

        self.init_db()

    def init_db(self):
        """
        It creates the database with the default tables.
        """

        try:
            self.cursor.execute("PRAGMA foreign_keys = ON;")

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    sex TEXT CHECK(sex IN ('M', 'F')),
                    current_period INTEGER,
                    indication INTEGER DEFAULT 0, -- 0 = False, 1 = True
                    email TEXT,
                    phone TEXT,
                    github TEXT,
                    linkedin TEXT,
                    personal_description TEXT,
                    qualities TEXT,
                    defects TEXT,
                    why_wants_to_work TEXT,
                    front_end_score REAL,
                    back_end_score REAL,
                    english_score REAL,
                    proactivity_score REAL,
                    resilience_score REAL,
                    communicative_skills_score REAL,
                    group_work_score REAL
                );
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id INTEGER NOT NULL,
                    time_slot TEXT NOT NULL,
                    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
                );
            """)

            self.connection.commit()

        except sqlite3.Error as e:
            print(f"\nErro ao iniciar o banco de dados: {e}")
            self.connection.rollback()

    def create_candidate(self, name: str) -> int:
        """
        It creates a candidate on the database.

        Arguments:
            name: the candidate's name

        Returns:
            0 if the creation was successful,
            1 otherwise.
        """

        pass

    def read_candidate(self, _id: int) -> dict:
        """
        It gets the information about a candidate.

        Arguments:
            _id: the candidate's id

        Returns:
            a dictionary containing the keys "name", "age", "sex", "current_period", "indication", "email", "phone", "github",
            "linkedin", "personal_description", "qualities", "defects", "why_wants_to_work", "front_end_score",
            "back_end_score", "english_score", "proactivity_score", "resilience_score", "communicative_skills_score",
            "group_work_score" and "schedules",
            but None if an error occuried.
        """

        pass

    def update_candidate(self, _id: int, name: str, age: int, sex: str, current_period: int, indication: bool,
                         email: str, phone: str, github: str, linkedin: str, personal_description: str,
                         qualities: str, defects: str, why_wants_to_work: str, front_end_score: float,
                         back_end_score: float, english_score: float, proactivity_score: float,
                         resilience_score: float, communicative_skills_score: float, group_work_score: float,
                         schedules: list) -> int:
        """
        It edits the information about a candidate.

        Arguments:
            _id: the candidate's id,
            name: the candidate's name,
            age: the candidate's age,
            sex: the candidate's sex,
            current_period: the candidate's current period,
            indication: the candidate's status on indication,
            email: the candidate's email,
            phone: the candidate's phone,
            github: the candidate's github,
            linkedin: the candidate's linkedin,
            personal_description: the candidate's personal description,
            qualities: the candidate's qualities,
            defects: the candidate's defects,
            why_wants_to_work: the candidate's justification to work at the company,
            front_end_score: the candidate's front end score,
            back_end_score: the candidate's back end score,
            english_score: the candidate's English score,
            proactivity_score: the candidate's proactivity score,
            resilience_score: the candidate's resilience score,
            communicative_skills_score: the candidate's communicative skills score,
            group_work_score: the candidate's group work score,
            schedules: the candidate's list of schedules

        Returns:
            0 if the update was successful,
            1 otherwise.
        """

        pass

    def delete_candidate(self, _id: int) -> int:
        """
        It deletes a candidate.

        Arguments:
            _id: the candidate's id

        Returns:
            0 if the deletion was successful,
            1 otherwise.
        """

        pass



    def create_schedule(self, _id: int, time_slot: str) -> int:
        """
        It creates a schedule on the database.

        Arguments:
            _id: the candidate's id associated to the schedule,
            time_slot: the schedule in the format hh:mm-hh:mm

        Returns:
            0 if the creation was successful,
            1 otherwise.
        """

        pass

    def read_schedule(self, candidate_id: int, schedule_id: int) -> str:
        """
        It gets the information about a schedule.

        Arguments:
            candidate_id: the candidate's id associated to the schedule,
            schedule_id: the schedule's own id

        Returns:
            a string in the format hh:mm-hh:mm, but None if an error occurried.
        """

        pass

    def update_schedule(self, candidate_id: int, schedule_id: int) -> int:
        """
        It edits the information about a schedule.

        Arguments:
            candidate_id: the candidate's id associated to the schedule,
            schedule_id: the schedule's own id

        Returns:
            0 if the update was successful,
            1 otherwise.
        """

        pass

    def delete_schedule(self, candidate_id: int, schedule_id: int) -> int:
        """
        It deletes a schedule.

        Arguments:
            candidate_id: the candidate's id associated to the schedule,
            schedule_id: the schedule's own id

        Returns:
            0 if the deletion was successful,
            1 otherwise.
        """

        pass

    def close_connection(self) -> None:
        """
        It closes the database connection.
        """

        self.connection.close()
