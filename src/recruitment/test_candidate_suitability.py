
import pandas as pd

from pathlib import Path
from src.recruitment.matching_engine import calculate_candidate_suitability

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load datasets
candidates = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "candidates.csv"
)

jobs = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "jobs.csv"
)

# Select candidate and job
candidate = candidates.iloc[0].to_dict()

job = jobs[jobs["job_id"] == "JOB001"].iloc[0].to_dict()

# Calculate overall suitability
result = calculate_candidate_suitability(
    candidate,
    job
)

# Display results
print("=" * 60)
print("CANDIDATE SUITABILITY EVALUATION")
print("=" * 60)

print("\nCandidate:", result["candidate_name"])
print("Candidate ID:", result["candidate_id"])

print("\nJob:", result["job_title"])
print("Job ID:", result["job_id"])

print("\nCOMPONENT SCORES")

for component, score in result["component_scores"].items():
    print(f"{component.title():20s}: {score:.2f}/100")

print("\nOVERALL SUITABILITY SCORE:")
print(f"{result['overall_score']:.2f}/100")

print("\nSTRENGTHS:")

for strength in result["strengths"]:
    print("-", strength)

print("\nGAPS:")

for gap in result["gaps"]:
    print("-", gap)

print("\nELIGIBILITY INDICATORS:")
print(
    "Experience requirement:",
    result["meets_experience_requirement"]
)

print(
    "Education requirement:",
    result["meets_education_requirement"]
)

print(
    "Certification requirement:",
    result["meets_certification_requirement"]
)
