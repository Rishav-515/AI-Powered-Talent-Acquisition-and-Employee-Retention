
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "recruitment"))

from matching_engine import (
    calculate_skill_match,
    calculate_experience_match,
    calculate_education_match,
    calculate_certification_match,
    calculate_project_relevance,
    calculate_candidate_suitability,
    rank_candidates,
    compare_candidates
)


# Load synthetic datasets
candidates = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "candidates.csv"
)

jobs = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "jobs.csv"
)

candidate = candidates.iloc[0]
job = jobs.iloc[0]


def test_skill_matching():
    result = calculate_skill_match(candidate, job)

    assert 0 <= result["score"] <= 100
    assert isinstance(result["matched_required_skills"], list)
    assert isinstance(result["missing_required_skills"], list)


def test_experience_matching():
    result = calculate_experience_match(candidate, job)

    assert 0 <= result["score"] <= 100
    assert isinstance(result["meets_requirement"], bool)


def test_education_matching():
    result = calculate_education_match(candidate, job)

    assert 0 <= result["score"] <= 100
    assert "education_level_match" in result


def test_certification_matching():
    result = calculate_certification_match(candidate, job)

    assert 0 <= result["score"] <= 100
    assert "matched_preferred_certifications" in result
    assert "missing_preferred_certifications" in result
    assert isinstance(result["has_required_certifications"], bool)


def test_project_relevance():
    result = calculate_project_relevance(candidate, job)

    assert 0 <= result["score"] <= 100


def test_candidate_suitability():
    result = calculate_candidate_suitability(candidate, job)

    assert 0 <= result["overall_score"] <= 100
    assert "component_scores" in result
    assert "review_status" in result
    assert "meets_minimum_requirements" in result


def test_ranking():
    results = rank_candidates(candidates, job)

    assert len(results) == len(candidates)

    scores = [result["overall_score"] for result in results]

    assert scores == sorted(scores, reverse=True)

    assert all(result["rank"] == i + 1
               for i, result in enumerate(results))


def test_candidate_comparison():
    selected_ids = candidates["candidate_id"].head(3).tolist()

    results = compare_candidates(
        candidates,
        job,
        selected_ids
    )

    assert len(results) == 3

    scores = [result["overall_score"] for result in results]

    assert scores == sorted(scores, reverse=True)


if __name__ == "__main__":

    tests = [
        test_skill_matching,
        test_experience_matching,
        test_education_matching,
        test_certification_matching,
        test_project_relevance,
        test_candidate_suitability,
        test_ranking,
        test_candidate_comparison
    ]

    passed = 0

    print("=" * 65)
    print("RECRUITMENT ENGINE AUTOMATED TESTS")
    print("=" * 65)

    for test in tests:

        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1

        except Exception as error:
            print(f"FAIL: {test.__name__}")
            print(f"Reason: {error}")

    print("\n" + "=" * 65)
    print(f"Tests passed: {passed}/{len(tests)}")
    print("=" * 65)

    if passed != len(tests):
        raise SystemExit("Some recruitment engine tests failed.")

    print("\nAll recruitment engine tests passed.")
