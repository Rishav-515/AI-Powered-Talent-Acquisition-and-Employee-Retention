
import pandas as pd

from pathlib import Path
from src.recruitment.matching_engine import calculate_project_relevance

PROJECT_ROOT = Path(__file__).resolve().parents[2]

candidates = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "candidates.csv"
)

jobs = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "jobs.csv"
)

candidate = candidates.iloc[0].to_dict()

job = jobs[jobs["job_id"] == "JOB001"].iloc[0].to_dict()

result = calculate_project_relevance(candidate, job)

print("=" * 55)
print("PROJECT RELEVANCE MATCHING TEST")
print("=" * 55)

print("\nCandidate:", candidate["candidate_name"])
print("Projects:", candidate["projects"])
print("Project Domain:", candidate["project_domains"])

print("\nJob:", job["job_title"])

print("\nProject Relevance Score:", result["score"])
print("Relevance:", result["relevance"])
print("Domain Match:", result["domain_match"])
print("Keyword Match:", result["title_keyword_match"])
