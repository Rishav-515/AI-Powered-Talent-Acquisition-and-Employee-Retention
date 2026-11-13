
import pandas as pd

from src.recruitment.matching_engine import calculate_candidate_suitability

candidates = pd.read_csv("data/raw/candidates.csv")
jobs = pd.read_csv("data/raw/jobs.csv")

print("=" * 75)
print("MINIMUM REQUIREMENT FLAGS TEST")
print("=" * 75)

for _, job in jobs.iterrows():

    results = []

    for _, candidate in candidates.iterrows():

        result = calculate_candidate_suitability(candidate, job)

        results.append({
            "candidate_name": result["candidate_name"],
            "overall_score": result["overall_score"],
            "meets_experience": result["meets_experience_requirement"],
            "meets_education_level": result["meets_education_requirement"],
            "meets_certification": result["meets_certification_requirement"],
            "specialization_match":
                result["education_details"]["specialization_match"]
        })

    results_df = pd.DataFrame(results)

    print(f"\nJOB: {job['job_title']}")
    print("-" * 75)

    print("Total candidates:", len(results_df))
    print(
        "Meet experience requirement:",
        results_df["meets_experience"].sum()
    )
    print(
        "Do not meet experience requirement:",
        (~results_df["meets_experience"]).sum()
    )
    print(
        "Meet minimum education level:",
        results_df["meets_education_level"].sum()
    )
    print(
        "Do not meet minimum education level:",
        (~results_df["meets_education_level"]).sum()
    )
    print(
        "Meet specialization requirement:",
        results_df["specialization_match"].sum()
    )
    print(
        "Meet mandatory certification requirements:",
        results_df["meets_certification"].sum()
    )

    print("\nCandidates failing minimum experience:")

    print(
        results_df[
            ~results_df["meets_experience"]
        ][["candidate_name", "overall_score"]].to_string(index=False)
    )

    print("\nCandidates failing minimum education level:")

    print(
        results_df[
            ~results_df["meets_education_level"]
        ][["candidate_name", "overall_score"]].to_string(index=False)
    )

print("\nRequirement flags test completed.")
