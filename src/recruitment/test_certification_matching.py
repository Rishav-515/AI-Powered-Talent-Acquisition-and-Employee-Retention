
import pandas as pd

from src.recruitment.matching_engine import calculate_certification_match


candidate = {
    "certifications": (
        "Python Programming Certification; "
        "Machine Learning Certification"
    )
}

jobs = pd.read_csv("data/raw/jobs.csv")

print("=" * 65)
print("CERTIFICATION MATCHING TEST")
print("=" * 65)

for _, job in jobs.iterrows():

    result = calculate_certification_match(candidate, job)

    print(f"\nJob: {job['job_title']}")
    print(f"Certification Score: {result['score']}")
    print(f"Matched Required: {result['matched_certifications']}")
    print(f"Missing Required: {result['missing_certifications']}")
    print(
        "Matched Preferred:",
        result["matched_preferred_certifications"]
    )
    print(
        "Missing Preferred:",
        result["missing_preferred_certifications"]
    )
    print(
        "Meets Mandatory Requirements:",
        result["has_required_certifications"]
    )

print("\nCertification matching test completed.")
