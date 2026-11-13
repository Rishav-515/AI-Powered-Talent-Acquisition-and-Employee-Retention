
import pandas as pd
from pathlib import Path

from matching_engine import rank_candidates


# ---------------------------------------------------------
# 1. DEFINE PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CANDIDATES_PATH = PROJECT_ROOT / "data" / "raw" / "candidates.csv"
JOBS_PATH = PROJECT_ROOT / "data" / "raw" / "jobs.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 2. LOAD DATASETS
# ---------------------------------------------------------

print("=" * 70)
print("CANDIDATE RANKING EXPORT")
print("=" * 70)

candidates = pd.read_csv(CANDIDATES_PATH)
jobs = pd.read_csv(JOBS_PATH)

print(f"\nCandidates loaded: {len(candidates)}")
print(f"Jobs loaded: {len(jobs)}")


# ---------------------------------------------------------
# 3. EVALUATE CANDIDATES FOR EACH JOB
# ---------------------------------------------------------

all_results = []

for _, job in jobs.iterrows():

    print(f"\nEvaluating candidates for: {job['job_title']}")

    ranked_results = rank_candidates(candidates, job)

    for result in ranked_results:

        component_scores = result["component_scores"]

        record = {
            "job_id": result["job_id"],
            "job_title": result["job_title"],
            "candidate_id": result["candidate_id"],
            "candidate_name": result["candidate_name"],
            "rank": result["rank"],
            "overall_score": result["overall_score"],

            "skills_score": component_scores["skills"],
            "experience_score": component_scores["experience"],
            "education_score": component_scores["education"],
            "certifications_score": component_scores["certifications"],
            "matched_required_certifications":
                "; ".join(
                    result["certification_details"]["matched_certifications"]
                ),

            "missing_required_certifications":
                "; ".join(
                    result["certification_details"]["missing_certifications"]
                ),

            "matched_preferred_certifications":
                "; ".join(
                    result["certification_details"]["matched_preferred_certifications"]
                ),

            "missing_preferred_certifications":
                "; ".join(
                    result["certification_details"]["missing_preferred_certifications"]
                ),
            "projects_score": component_scores["projects"],

            "meets_experience_requirement":
                result["meets_experience_requirement"],

            "meets_education_requirement":
                result["meets_education_requirement"],

            "meets_certification_requirement":
                result["meets_certification_requirement"],

            "meets_minimum_requirements":
                result["meets_minimum_requirements"],

            "review_status":
                result["review_status"],

            "missing_required_skills":
                "; ".join(
                    result["skill_details"]["missing_required_skills"]
                ),

            "strengths": "; ".join(result["strengths"]),
            "gaps": "; ".join(result["gaps"])
        }

        all_results.append(record)


# ---------------------------------------------------------
# 4. CREATE MASTER RESULTS DATAFRAME
# ---------------------------------------------------------

results_df = pd.DataFrame(all_results)

results_df = results_df.sort_values(
    by=["job_id", "rank"]
).reset_index(drop=True)


# ---------------------------------------------------------
# 5. EXPORT MASTER RESULTS
# ---------------------------------------------------------

master_output = OUTPUT_DIR / "candidate_job_rankings.csv"

results_df.to_csv(
    master_output,
    index=False,
    na_rep=""
)

print("\nMaster ranking file saved:")
print(master_output)


# ---------------------------------------------------------
# 6. EXPORT SEPARATE RANKING FILE FOR EACH JOB
# ---------------------------------------------------------

for _, job in jobs.iterrows():

    job_results = results_df[
        results_df["job_id"] == job["job_id"]
    ].copy()

    filename = f"{job['job_id']}_candidate_rankings.csv"
    output_path = OUTPUT_DIR / filename

    job_results.to_csv(
    output_path,
    index=False,
    na_rep=""
    )

    print(f"Saved: {filename}")


# ---------------------------------------------------------
# 7. FINAL VALIDATION
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("EXPORT VALIDATION")
print("=" * 70)

print(f"Total evaluation records: {len(results_df)}")
print(f"Expected evaluation records: {len(candidates) * len(jobs)}")
print(f"Unique candidates: {results_df['candidate_id'].nunique()}")
print(f"Unique jobs: {results_df['job_id'].nunique()}")

print("\nRecords per job:")
print(results_df.groupby("job_title").size())

assert len(results_df) == len(candidates) * len(jobs)

assert results_df.groupby("job_id")["candidate_id"].nunique().eq(
    len(candidates)
).all()

assert not results_df.duplicated(
    subset=["job_id", "candidate_id"]
).any()

print("\nAll export validation checks passed.")


# ---------------------------------------------------------
# 8. DISPLAY TOP 3 CANDIDATES FOR EACH JOB
# ---------------------------------------------------------

print("\nTop 3 candidates for each job:")

for job_title, group in results_df.groupby("job_title"):

    print(f"\n{job_title}")

    print(
        group.head(3)[
            ["rank", "candidate_name", "overall_score"]
        ].to_string(index=False)
    )

print("\nCandidate ranking export completed.")
