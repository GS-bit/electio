"""
In Electio, the time, from the beginning of Sunday until the end of Saturday, is viewed as a discrete set of tuples,
called universe, in the format (d, h, m), in which d is the day, going from 0 (Sunday) to 6 (Saturday), h is the hour, going from 0 to 23, always an int, and m are the minutes, going from 0 to 59, always an int too.
"""

from database import Database


def get_schedules(db: Database) -> dict:
    """
    It returns the current general status of schedules, considering the candidates' schedules.

    Arguments:
        database: the database

    Returns:
        a dictionary containing all the elements of universe set as keys and, as their values, the number of candidates that
        have these parts of time available.
    """

    result = {(i, j, k): 0 for i in range(7) for j in range(24) for k in range(60)}

    candidates = db.fetch_candidates()

    for candidate in candidates:
        schedules = candidate["schedules"]

        for schedule in schedules:
            all_tuples = str_schedule_to_list(schedule)
            for tuple in all_tuples:
                result[tuple] += 1

    return result

def get_candidates_by_availability(db: Database) -> list:
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

def get_candidates_by_insufficient_availability(db: Database) -> list:
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

def str_schedule_to_list(schedule_str: str) -> list:
    """
    It converts a schedule string in the format "day hh:mm-hh:mm" and returns a list of tuples (d, h, m).

    Arguments:
        schedule_str: the schedule string to be parsed

    Returns:
        a list of tuples (d, h, m) representing the schedule
    """

    day = schedule_str.split()[0]

    time_range = schedule_str.split()[1]
    time1 = time_range.split("-")[0]
    time2 = time_range.split("-")[1]
    
    h_initial = time1.split(":")[0]
    m_initial = time1.split(":")[1]
    h_final = time2.split(":")[0]
    m_final = time2.split(":")[1]

    day_mapping = {
        "Domingo": 0, "Segunda-feira": 1, "Terça-feira": 2,
        "Quarta-feira": 3, "Quinta-feira": 4, "Sexta-feira": 5, "Sábado": 6
    }

    d = day_mapping.get(day, 0)  # Default to 0 (Domingo) if the day is not recognized

    result = []

    for h in range(int(h_initial), int(h_final) + 1):
        for m in range(0, 60):
            if h == int(h_initial) and m < int(m_initial):
                continue

            if h == int(h_final) and m > int(m_final):
                continue
            
            result.append((d, h, m))

    return result

def list_schedule_to_str(schedule_list: list) -> str:
    """
    It converts a list of tuples (d, m, h) to a string in the format "day hh:mm-hh:mm".

    Arguments:
        schedule_list: the schedule list to be parsed

    Returns:
        a string in the format "day hh:mm-hh:mm" representing the schedule
    """

    if not schedule_list:
        return ""

    day = schedule_list[0][0]
    day_names = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]
    day_name = day_names[day]

    # Extract the start and end times
    h_initial = schedule_list[0][1]
    m_initial = schedule_list[0][2]
    h_final = schedule_list[-1][1]
    m_final = schedule_list[-1][2]

    return f"{day_name} {h_initial:02d}:{m_initial:02d}-{h_final:02d}:{m_final:02d}"

def format_intervals_by_day(db: Database, target_day_name: str) -> str:
    """
    It groups the minute-by-minute universe tuples into continuous time blocks and displays how many candidates are available in each range.

    Arguments:
        database: the database
        target_day_name: the name of the day (example: Friday)

    Returns:
        a string containing the schedules and their counts on the given day
    """

    day_mapping = {
        "Domingo": 0, "Segunda-feira": 1, "Terça-feira": 2,
        "Quarta-feira": 3, "Quinta-feira": 4, "Sexta-feira": 5, "Sábado": 6
    }

    d = day_mapping.get(target_day_name, 0)  # Default to 0 (Domingo) if the day is not recognized

    schedules = get_schedules(db)

    result = ""

    i = 0
    j = 0

    while i < 24:
        list_of_tuples = []     
        cur_value = schedules[(d, i, j)]

        while schedules[(d, i, j)] == cur_value:
            list_of_tuples.append((d, i, j))

            j += 1
            if j == 60:
                j = 0
                i += 1

                if i == 24:
                    break

        if cur_value != 0:
            result += f"{list_schedule_to_str(list_of_tuples).split()[1]}: {cur_value}<br />"

    return result