
import pandas as pd

from pathlib import Path
from src.recruitment.matching_engine import calculate_skill_match

# Load datasets
PROJECT_ROOT = Path(__file__).resolve().parents[2]

candidates = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "candidates.csv"
)

jobs = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "jobs.csv"
)

# Select one candidate and one job
candidate = candidates.iloc[0].to_dict()

job = jobs[jobs["job_id"] == "JOB001"].iloc[0].to_dict()

# Calculate skill matching
result = calculate_skill_match(candidate, job)

# Display results
print("=" * 55)
print("CANDIDATE SKILL MATCHING TEST")
print("=" * 55)

print("\nCandidate:", candidate["candidate_name"])
print("Preferred Role:", candidate["preferred_role"])

print("\nJob:", job["job_title"])

print("\nSkill Matching Score:", result["score"])

print("\nMatched Required Skills:")
print(result["matched_required_skills"])

print("\nMissing Required Skills:")
print(result["missing_required_skills"])

print("\nMatched Preferred Skills:")
print(result["matched_preferred_skills"])

print("\nMissing Preferred Skills:")
print(result["missing_preferred_skills"])

print("\nRequired Skill Score:", result["required_score"])
print("Preferred Skill Score:", result["preferred_score"])
