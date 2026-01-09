from typing import Dict, List


def analyze_coverage(parsed_report: Dict) -> List[Dict]:
    """
    Analyze parsed coverage report and generate enriched insights
    for each uncovered bin.
    """

    analysis_results = []

    # -------------------------
    # Build quick lookup maps
    # -------------------------
    covered_lookup = {}

    for cg in parsed_report["covergroups"]:
        for cp in cg["coverpoints"]:
            key = (cg["name"], cp["name"])
            covered_lookup[key] = [
                b["name"] for b in cp["bins"] if b["covered"]
            ]

    # -------------------------
    # Analyze uncovered bins
    # -------------------------
    for ub in parsed_report["uncovered_bins"]:
        cg = ub["covergroup"]
        cp = ub["coverpoint"]
        bin_name = ub["bin"]

        related_covered = covered_lookup.get((cg, cp), [])

        # -------------------------
        # Pattern detection
        # -------------------------
        pattern = "unknown"
        likely_cause = "unknown"
        difficulty = "medium"
        bin_type = "single"
        coverage_impact = 0.02

        # Mode-specific gaps
        if "wrap" in bin_name and ("single" in related_covered or "incr" in related_covered):
            pattern = "mode_specific_gap"
            likely_cause = "requires specific configuration or alignment"
            difficulty = "medium"
            coverage_impact = 0.04

        # High concurrency gaps
        elif "four" in bin_name or "eight" in bin_name:
            pattern = "high_concurrency_gap"
            likely_cause = "requires stress or parallel activity"
            difficulty = "hard"
            coverage_impact = 0.06

        # Error injection gaps
        elif "error" in bin_name or "timeout" in bin_name:
            pattern = "error_injection_gap"
            likely_cause = "requires explicit error injection in testbench"
            difficulty = "hard"
            coverage_impact = 0.05

        # Default config gaps
        else:
            pattern = "configuration_gap"
            likely_cause = "missing specific parameter combination"
            difficulty = "easy"
            coverage_impact = 0.02

        analysis_results.append({
            "target_bin": f"{cg}.{cp}.{bin_name}",
            "bin_type": bin_type,
            "related_covered_bins": related_covered,
            "pattern": pattern,
            "likely_cause": likely_cause,
            "estimated_difficulty": difficulty,
            "coverage_impact": coverage_impact
        })

    # -------------------------
    # Analyze cross coverage
    # -------------------------
    for cross in parsed_report["cross_coverage"]:
        for uc in cross["uncovered"]:
            analysis_results.append({
                "target_bin": f"{cross['name']}.{uc}",
                "bin_type": "cross",
                "related_covered_bins": [],
                "pattern": "cross_coverage_gap",
                "likely_cause": "rare or untested combination of legal values",
                "estimated_difficulty": "medium",
                "coverage_impact": 0.03
            })

    return analysis_results
