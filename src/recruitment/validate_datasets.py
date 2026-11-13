
import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Load datasets
candidates = pd.read_csv(RAW_DATA_DIR / "candidates.csv")
jobs = pd.read_csv(RAW_DATA_DIR / "jobs.csv")

# 1. Dataset dimensions
print("=" * 55)
print("DATASET DIMENSIONS")
print("=" * 55)

print("Candidates:", candidates.shape)
print("Jobs:", jobs.shape)

# 2. Candidate columns
print("\nCANDIDATE COLUMNS:")
print(candidates.columns.tolist())

# 3. Job columns
print("\nJOB COLUMNS:")
print(jobs.columns.tolist())

# 4. Missing values
print("\nMISSING VALUES IN CANDIDATES:")
print(candidates.isnull().sum())

print("\nMISSING VALUES IN JOBS:")
print(jobs.isnull().sum())

# 5. Duplicate records
print("\nDUPLICATE RECORDS:")
print("Candidates:", candidates.duplicated().sum())
print("Jobs:", jobs.duplicated().sum())

# 6. Candidate experience distribution
print("\nEXPERIENCE DISTRIBUTION:")
print(candidates["experience_years"].value_counts().sort_index())

# 7. Candidate role distribution
print("\nPREFERRED ROLE DISTRIBUTION:")
print(candidates["preferred_role"].value_counts())

# 8. Candidate preview
print("\nFIRST FIVE CANDIDATES:")
print(candidates.head().to_string(index=False))

# 9. Job preview
print("\nJOB DESCRIPTIONS:")
print(jobs[["job_id", "job_title", "minimum_experience"]].to_string(index=False))

# 10. Basic validation checks
assert len(candidates) == 50, "Expected 50 candidates"
assert len(jobs) == 5, "Expected 5 jobs"
assert candidates["candidate_id"].is_unique, "Duplicate candidate IDs"
assert jobs["job_id"].is_unique, "Duplicate job IDs"
assert candidates["experience_years"].between(0, 5).all()

print("\nAll basic validation checks passed.")
