"""
In Electio, the time, from the beginning of Sunday until the end of Saturday, is viewed as a discrete set of tuples,
called universe, in the format (d, h, m), in which d is the day, going from 0 (Sunday) to 6 (Saturday), h is the hour, going from 0 to 23, always an int, and m are the minutes, going from 0 to 59, always an int too.
"""

def get_schedules(database: Database) -> dict:
    """
    It returns the current general status of schedules, considering the candidates' schedules.

    Arguments:
        database: the database

    Returns:
        a dictionary containing all the elements of universe set as keys and, as their values, the number of candidates that
        have these parts of time available.
    """

    pass

def get_candidates_by_availability(database: Database) -> list:
    """
    It returns a list of the candidates considering the availability.

    Arguments:
        database: the database

    Returns:
        a list in which the first element is the candidate with the greatest availability, the second element is the
        candidate with the second greatest availability and so on. The candidates are in the dictionary format, containing the keys "name", "age", "sex", "current_period", "indication", "email", "phone", "github",
        "linkedin", "personal_description", "qualities", "defects", "why_wants_to_work", "front_end_score",
        "back_end_score", "english_score", "proactivity_score", "resilience_score", "communicative_skills_score",
        "group_work_score" and "schedules".
    """

    pass

def get_candidates_by_insufficient_availability(database: Database) -> list:
    """
    It returns a list of the candidates with insufficient availability.

    Arguments:
        database: the database

    Returns:
        a list of candidates with insufficient availability. The candidates are in the dictionary format, containing the keys "name", "age", "sex", "current_period", "indication", "email", "phone", "github",
        "linkedin", "personal_description", "qualities", "defects", "why_wants_to_work", "front_end_score",
        "back_end_score", "english_score", "proactivity_score", "resilience_score", "communicative_skills_score",
        "group_work_score" and "schedules".
    """

    pass
