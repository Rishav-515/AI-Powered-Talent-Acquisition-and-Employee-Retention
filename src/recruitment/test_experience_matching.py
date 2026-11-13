
import pandas as pd

from pathlib import Path
from src.recruitment.matching_engine import calculate_experience_match

# Load datasets
PROJECT_ROOT = Path(__file__).resolve().parents[2]

candidates = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "candidates.csv"
)

jobs = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "jobs.csv"
)

# Select candidate and job
candidate = candidates.iloc[0].to_dict()

job = jobs[jobs["job_id"] == "JOB004"].iloc[0].to_dict()

# Calculate experience matching
result = calculate_experience_match(candidate, job)

print("=" * 55)
print("EXPERIENCE MATCHING TEST")
print("=" * 55)

print("\nCandidate:", candidate["candidate_name"])
print("Candidate Experience:", result["candidate_experience"])

print("\nJob:", job["job_title"])
print("Required Experience:", result["required_experience"])

print("\nExperience Matching Score:", result["score"])

print("Meets Requirement:", result["meets_requirement"])

print("Experience Gap:", result["experience_gap"], "years")
