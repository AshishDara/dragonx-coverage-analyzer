from typing import List, Dict


DIFFICULTY_TIME_MAP = {
    "easy": 0.5,
    "medium": 1.5,
    "hard": 3.0
}

DIFFICULTY_PROB_MAP = {
    "easy": 0.9,
    "medium": 0.7,
    "hard": 0.5
}


def predict_closure(prioritized_suggestions: List[Dict]) -> List[Dict]:
    """
    Add closure time, probability, and blockers to each suggestion
    """

    results = []

    for s in prioritized_suggestions:
        difficulty = s.get("difficulty", "medium")
        dependencies = s.get("dependencies", [])
        bin_type = "cross" if "cross_" in s["target_bin"] else "single"

        # ---- Time estimation ----
        base_time = DIFFICULTY_TIME_MAP.get(difficulty, 1.5)
        if dependencies:
            base_time += 1.0

        # ---- Probability estimation ----
        probability = DIFFICULTY_PROB_MAP.get(difficulty, 0.7)
        if dependencies:
            probability -= 0.1
        if bin_type == "cross":
            probability -= 0.1

        probability = max(0.1, min(probability, 0.95))

        s["estimated_time_days"] = round(base_time, 1)
        s["closure_probability"] = round(probability, 2)
        s["blockers"] = dependencies if dependencies else ["None"]

        results.append(s)

    return results
