from typing import List, Optional


class Bin:
    def __init__(self, name: str, hits: int, covered: bool, range_: Optional[str] = None):
        self.name = name
        self.range = range_
        self.hits = hits
        self.covered = covered

    def to_dict(self):
        return {
            "name": self.name,
            "range": self.range,
            "hits": self.hits,
            "covered": self.covered
        }


class CoverPoint:
    def __init__(self, name: str):
        self.name = name
        self.bins: List[Bin] = []

    def to_dict(self):
        return {
            "name": self.name,
            "bins": [b.to_dict() for b in self.bins]
        }


class CoverGroup:
    def __init__(self, name: str, coverage: float):
        self.name = name
        self.coverage = coverage
        self.coverpoints: List[CoverPoint] = []

    def to_dict(self):
        return {
            "name": self.name,
            "coverage": self.coverage,
            "coverpoints": [cp.to_dict() for cp in self.coverpoints]
        }


class CrossCoverage:
    def __init__(self, name: str, coverage: float):
        self.name = name
        self.coverage = coverage
        self.uncovered: List[str] = []

    def to_dict(self):
        return {
            "name": self.name,
            "coverage": self.coverage,
            "uncovered": self.uncovered
        }
