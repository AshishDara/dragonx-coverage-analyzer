from parser.coverage_parser import parse_coverage_report
from analyzer.coverage_analyzer import analyze_coverage
from llm.suggestion_agent import generate_test_suggestions
from prioritizer.prioritizer import prioritize_suggestions
from predictor.closure_predictor import predict_closure
import json


def pretty_print(title: str, data):
    print(f"\n{'=' * 20} {title} {'=' * 20}\n")
    print(json.dumps(data, indent=2))


def main():
    # -------------------------
    # Step 0: Read input report
    # -------------------------
    with open("examples/sample_report.txt", "r") as f:
        report_text = f.read()

    # -------------------------
    # Step 1: Parse coverage
    # -------------------------
    parsed_report = parse_coverage_report(report_text)
    pretty_print("PARSED COVERAGE REPORT", parsed_report)

    # -------------------------
    # Step 2: Coverage analysis
    # -------------------------
    analysis_report = analyze_coverage(parsed_report)
    pretty_print("COVERAGE ANALYSIS REPORT", analysis_report)

    # -------------------------
    # Step 3: LLM suggestions
    # -------------------------
    llm_output = generate_test_suggestions(parsed_report, analysis_report)
    pretty_print("LLM RAW TEST SUGGESTIONS", llm_output)

    # -------------------------
    # Step 4: Prioritization
    # -------------------------
    prioritized_plan = prioritize_suggestions(llm_output, analysis_report)
    pretty_print("PRIORITIZED TEST PLAN", prioritized_plan)

    # -------------------------
    # Step 5: Closure prediction
    # -------------------------
    final_closure_plan = predict_closure(prioritized_plan)
    pretty_print("FINAL COVERAGE CLOSURE PLAN WITH PREDICTIONS", final_closure_plan)


if __name__ == "__main__":
    main()
