
import pandas as pd

from src.recruitment.matching_engine import calculate_candidate_suitability

candidates = pd.read_csv("data/raw/candidates.csv")
jobs = pd.read_csv("data/raw/jobs.csv")

print("=" * 65)
print("CANDIDATE REVIEW STATUS TEST")
print("=" * 65)

for _, job in jobs.iterrows():

    results = []

    for _, candidate in candidates.iterrows():

        result = calculate_candidate_suitability(candidate, job)

        results.append({
            "candidate_name": result["candidate_name"],
            "overall_score": result["overall_score"],
            "meets_minimum_requirements":
                result["meets_minimum_requirements"],
            "review_status": result["review_status"]
        })

    results_df = pd.DataFrame(results)

    print(f"\nJob: {job['job_title']}")
    print("-" * 65)

    print(results_df["review_status"].value_counts().to_string())

    print("\nCandidates requiring human review:")

    print(
        results_df[
            results_df["review_status"] == "Requires human review"
        ][["candidate_name", "overall_score"]].to_string(index=False)
    )

print("\nReview status test completed.")
