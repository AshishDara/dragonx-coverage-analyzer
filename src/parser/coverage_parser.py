import re
from typing import Dict

from models import Bin, CoverPoint, CoverGroup, CrossCoverage


def parse_coverage_report(report_text: str) -> Dict:
    result = {
        "design": None,
        "overall_coverage": None,
        "covergroups": [],
        "uncovered_bins": [],
        "cross_coverage": []
    }

    lines = report_text.splitlines()

    # -------------------------
    # Header parsing
    # -------------------------
    for line in lines:
        if line.startswith("Design:"):
            result["design"] = line.split("Design:")[1].strip()

        if line.startswith("Overall Coverage:"):
            cov = re.search(r"([\d.]+)%", line)
            if cov:
                result["overall_coverage"] = float(cov.group(1))

    # -------------------------
    # Parse covergroups
    # -------------------------
    sections = re.split(r"-{20,}", report_text)

    for section in sections:
        cg_match = re.search(r"Covergroup:\s*(\w+)", section)
        cov_match = re.search(r"Coverage:\s*([\d.]+)%", section)

        if not cg_match or not cov_match:
            continue

        covergroup = CoverGroup(
            name=cg_match.group(1),
            coverage=float(cov_match.group(1))
        )

        coverpoint_blocks = re.split(r"Coverpoint:\s*", section)[1:]

        for cp_block in coverpoint_blocks:
            cp_lines = [l.strip() for l in cp_block.splitlines() if l.strip()]
            if not cp_lines:
                continue

            cp = CoverPoint(cp_lines[0])

            for line in cp_lines[1:]:
                bin_match = re.match(
                    r"bin\s+(\w+)(\[[^\]]+\])?\s+hits:\s*(\d+)\s+(covered|UNCOVERED)",
                    line,
                    re.IGNORECASE
                )

                if not bin_match:
                    continue

                name = bin_match.group(1)
                range_ = bin_match.group(2)
                hits = int(bin_match.group(3))
                covered = bin_match.group(4).lower() == "covered"

                bin_obj = Bin(name=name, range_=range_, hits=hits, covered=covered)
                cp.bins.append(bin_obj)

                if not covered:
                    result["uncovered_bins"].append({
                        "covergroup": covergroup.name,
                        "coverpoint": cp.name,
                        "bin": f"{name}{range_ or ''}"
                    })

            covergroup.coverpoints.append(cp)

        result["covergroups"].append(covergroup.to_dict())

    # -------------------------
    # Parse cross coverage (FIXED)
    # -------------------------
    in_cross_section = False
    current_cross = None

    for line in lines:
        line = line.strip()

        # Start of cross coverage
        if line.startswith("Cross Coverage:"):
            name = line.split("Cross Coverage:")[1].strip()
            current_cross = CrossCoverage(name=name, coverage=0.0)
            in_cross_section = True
            continue

        if in_cross_section and line.startswith("Coverage:"):
            cov = re.search(r"([\d.]+)%", line)
            if cov:
                current_cross.coverage = float(cov.group(1))
            continue

        if in_cross_section and "UNCOVERED" in line:
            bin_match = re.search(r"<[^>]+>", line)
            if bin_match:
                current_cross.uncovered.append(bin_match.group(0))
            continue

        # End of cross coverage (footer)
        if in_cross_section and line.startswith("="):
            result["cross_coverage"].append(current_cross.to_dict())
            in_cross_section = False
            current_cross = None

    return result
