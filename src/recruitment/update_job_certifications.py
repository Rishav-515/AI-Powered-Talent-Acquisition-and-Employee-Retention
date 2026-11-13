
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

JOBS_PATH = PROJECT_ROOT / "data" / "raw" / "jobs.csv"

jobs = pd.read_csv(JOBS_PATH, keep_default_na=False)

preferred_certifications = {
    "JOB001": "Python Programming Certification;Flask Certification",
    "JOB002": "Python Programming Certification;API Development Certification",
    "JOB003": "Python Programming Certification;Data Analytics Certification;Power BI Certification",
    "JOB004": "Machine Learning Certification;Deep Learning Certification",
    "JOB005": "Web Development Certification;JavaScript Certification"
}

jobs["preferred_certifications"] = jobs["job_id"].map(
    preferred_certifications
)

if jobs["preferred_certifications"].isnull().any():
    raise ValueError("Some jobs are missing preferred certification data.")

jobs.to_csv(JOBS_PATH, index=False)

print("Preferred certifications added successfully.")
print("\nUpdated job certification data:")

print(
    jobs[
        [
            "job_id",
            "job_title",
            "required_certifications",
            "preferred_certifications"
        ]
    ].to_string(index=False)
)
