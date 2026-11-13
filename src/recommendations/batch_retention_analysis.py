
import pandas as pd
import joblib
import json

from pathlib import Path

from src.recommendations.retention_engine import (
    generate_employee_retention_report
)

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT / "data" / "raw" /
    "WA_Fn-UseC_-HR-Employee-Attrition.csv"
)

MODEL_DIR = PROJECT_ROOT / "models"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# LOAD DATA AND MODEL
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

with open(
    MODEL_DIR / "attrition_model_config.json",
    "r"
) as file:
    config = json.load(file)

rf_model = joblib.load(
    MODEL_DIR / config["primary_model"]["file"]
)

preprocessor = joblib.load(
    MODEL_DIR / config["preprocessor"]
)

# --------------------------------------------------
# PREPROCESS ALL EMPLOYEES
# --------------------------------------------------

excluded_columns = [
    "Attrition",
    "EmployeeNumber",
    "EmployeeCount",
    "Over18",
    "StandardHours"
]

X = df.drop(columns=excluded_columns)

X_processed = preprocessor.transform(X)

probabilities = rf_model.predict_proba(
    X_processed
)[:, 1]

# --------------------------------------------------
# GENERATE RETENTION REPORTS
# --------------------------------------------------

results = []

for position, (_, employee) in enumerate(df.iterrows()):

    probability = float(probabilities[position])

    report = generate_employee_retention_report(
        employee,
        probability
    )

    results.append({
        "EmployeeNumber": employee["EmployeeNumber"],
        "Department": employee["Department"],
        "JobRole": employee["JobRole"],
        "AttritionProbability": report["attrition_probability"],
        "RiskCategory": report["risk_category"],
        "ReviewPriority": report["review_priority"],
        "RecommendationCount": report["total_recommendations"],
        "RecommendationCategories": "; ".join(
            item["category"]
            for item in report["recommendations"]
        )
    })

# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

results_df = pd.DataFrame(results)

output_path = (
    OUTPUT_DIR / "employee_retention_analysis.csv"
)

results_df.to_csv(output_path, index=False)

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("=" * 65)
print("BATCH EMPLOYEE RETENTION ANALYSIS")
print("=" * 65)

print("Employees processed:", len(results_df))

print("\nRisk distribution:")
print(
    results_df["RiskCategory"].value_counts()
    .reindex(["Low", "Moderate", "High"], fill_value=0)
)

print("\nDepartment-wise average predicted risk:")
print(
    results_df.groupby("Department")[
        "AttritionProbability"
    ].mean().round(2)
)

print("\nTotal recommendations generated:")
print(results_df["RecommendationCount"].sum())

print("\nOutput saved to:")
print(output_path)
