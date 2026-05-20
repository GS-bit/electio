from database import Database

def get_candidates_by_score(db: Database) -> list:
    """
    It returns a list of the candidates considering the score.

    Arguments:
        database: the database

    Returns:
        a list of tuples, in which the first element of the tuple is a candidate and the second is its score (arithmetic mean). The candidate with the greatest score is the first element of the list, the
        candidate with the second greatest score is the second and so on. The candidates are in the dictionary format, containing the keys "name", "age", "sex", "current_period", "indication", "email", "phone", "github", "linkedin", "personal_description", "qualities", "defects", "why_wants_to_work", "front_end_score", "back_end_score", "english_score", "proactivity_score", "resilience_score", "communicative_skills_score", "group_work_score" and "schedules".
    """

    candidates = db.fetch_candidates()

    averages = {} # A dictionary whose keys are the indices of candidates list and the values their arithmetic means

    for i, candidate in enumerate(candidates):
        front = candidate["front_end_score"] if candidate["front_end_score"] is not None else 0.0
        back = candidate["back_end_score"] if candidate["back_end_score"] is not None else 0.0
        english = candidate["english_score"] if candidate["english_score"] is not None else 0.0
        proactivity = candidate["proactivity_score"] if candidate["proactivity_score"] is not None else 0.0
        resilience = candidate["resilience_score"] if candidate["resilience_score"] is not None else 0.0
        communication = candidate["communicative_skills_score"] if candidate["communicative_skills_score"] is not None else 0.0
        group = candidate["group_work_score"] if candidate["group_work_score"] is not None else 0.0

        average = (front + back + english + proactivity + resilience + communication + group) / 7.0

        averages[i] = average

    sorted_averages = sorted(averages, key=averages.get, reverse=True)

    result = []

    for i in sorted_averages:
        result.append((candidates[i], round(averages[i], 2)))

    return result