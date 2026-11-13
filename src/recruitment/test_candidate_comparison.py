
import pandas as pd

from pathlib import Path
from src.recruitment.matching_engine import compare_candidates

PROJECT_ROOT = Path(__file__).resolve().parents[2]

candidates = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "candidates.csv"
)

jobs = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "jobs.csv"
)

# Select Python Developer job
job = jobs[
    jobs["job_id"] == "JOB001"
].iloc[0].to_dict()

# Select three candidates for comparison
selected_candidate_ids = [
    "CAND001",
    "CAND002",
    "CAND007"
]

comparison = compare_candidates(
    candidates,
    job,
    selected_candidate_ids
)

print("=" * 75)
print("CANDIDATE COMPARISON")
print("=" * 75)

print("\nJob:", job["job_title"])

for rank, candidate in enumerate(comparison, start=1):

    print("\n" + "-" * 60)
    print(f"RANK: {rank}")

    print("Candidate:", candidate["candidate_name"])
    print("Candidate ID:", candidate["candidate_id"])

    print(
        "Overall Score:",
        candidate["overall_score"]
    )

    print("\nComponent Scores:")

    for component, score in candidate["component_scores"].items():
        print(f"{component.title():20s}: {score:.2f}")

    print("\nMissing Required Skills:")

    print(
        candidate["skill_details"]["missing_required_skills"]
    )

    print("\nStrengths:")

    for strength in candidate["strengths"]:
        print("-", strength)

    print("\nGaps:")

    for gap in candidate["gaps"]:
        print("-", gap)

print("\nCandidate comparison completed.")
