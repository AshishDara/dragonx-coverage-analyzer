from typing import Dict, List


DIFFICULTY_MAP = {
    "easy": 1,
    "medium": 2,
    "hard": 3
}


def compute_priority_score(
    coverage_impact: float,
    difficulty: str,
    dependencies: List[str]
) -> float:
    """
    Priority Score = (Coverage Impact × 0.4)
                   + (Inverse Difficulty × 0.3)
                   + (Dependency Score × 0.3)
    """

    # Inverse difficulty
    diff_value = DIFFICULTY_MAP.get(difficulty, 2)
    inverse_difficulty = 1 / diff_value

    # Dependency score
    dependency_score = 1.0 if not dependencies else 0.5

    score = (
        (coverage_impact * 0.4)
        + (inverse_difficulty * 0.3)
        + (dependency_score * 0.3)
    )

    return round(score, 3)


def prioritize_suggestions(
    llm_output: Dict,
    analysis_output: List[Dict]
) -> List[Dict]:
    """
    Merge analyzer data with LLM suggestions and compute priority scores
    """

    # Build lookup from analyzer
    impact_lookup = {
        a["target_bin"]: a["coverage_impact"]
        for a in analysis_output
    }

    prioritized = []

    for s in llm_output.get("suggestions", []):
        target_bin = s["target_bin"]

        coverage_impact = impact_lookup.get(target_bin, 0.02)

        score = compute_priority_score(
            coverage_impact=coverage_impact,
            difficulty=s["difficulty"],
            dependencies=s.get("dependencies", [])
        )

        s["coverage_impact"] = coverage_impact
        s["priority_score"] = score

        prioritized.append(s)

    prioritized.sort(key=lambda x: x["priority_score"], reverse=True)
    return prioritized
