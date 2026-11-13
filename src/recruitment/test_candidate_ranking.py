
import pandas as pd

from pathlib import Path
from src.recruitment.matching_engine import rank_candidates

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load datasets
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

# Rank all candidates
ranked_candidates = rank_candidates(
    candidates,
    job
)

print("=" * 70)
print("CANDIDATE RANKING RESULTS")
print("=" * 70)

print("\nSelected Job:", job["job_title"])
print("Total Candidates Evaluated:", len(ranked_candidates))

print("\nTOP 10 CANDIDATES")
print("-" * 70)

for candidate in ranked_candidates[:10]:

    print(
        f"Rank: {candidate['rank']:2d} | "
        f"ID: {candidate['candidate_id']} | "
        f"Name: {candidate['candidate_name']:20s} | "
        f"Score: {candidate['overall_score']:.2f}"
    )

# Verify ranking order
scores = [
    candidate["overall_score"]
    for candidate in ranked_candidates
]

assert len(ranked_candidates) == len(candidates)
assert scores == sorted(scores, reverse=True)

print("\nAll ranking checks passed.")
