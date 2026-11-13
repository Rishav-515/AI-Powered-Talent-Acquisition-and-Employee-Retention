
import pandas as pd

from pathlib import Path
from src.recruitment.matching_engine import calculate_education_match

PROJECT_ROOT = Path(__file__).resolve().parents[2]

candidates = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "candidates.csv"
)

jobs = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "jobs.csv"
)

candidate = candidates.iloc[0].to_dict()

job = jobs[jobs["job_id"] == "JOB001"].iloc[0].to_dict()

result = calculate_education_match(candidate, job)

print("=" * 55)
print("EDUCATION MATCHING TEST")
print("=" * 55)

print("\nCandidate:", candidate["candidate_name"])
print("Education:", result["candidate_education"])
print("Specialization:", result["candidate_specialization"])

print("\nJob:", job["job_title"])
print("Required Education:", result["required_education"])
print("Required Specializations:", result["required_specializations"])

print("\nEducation Matching Score:", result["score"])
print("Education Level Match:", result["education_level_match"])
print("Specialization Match:", result["specialization_match"])
