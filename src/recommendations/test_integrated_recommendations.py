
import pandas as pd
import joblib
import json

from pathlib import Path

from src.recommendations.retention_engine import (
    generate_employee_retention_report
)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT / "data" / "raw" /
    "WA_Fn-UseC_-HR-Employee-Attrition.csv"
)

MODEL_DIR = PROJECT_ROOT / "models"

# Load dataset
df = pd.read_csv(DATA_PATH)

# Load model configuration
with open(
    MODEL_DIR / "attrition_model_config.json",
    "r"
) as file:
    config = json.load(file)

# Load trained Random Forest
rf_model = joblib.load(
    MODEL_DIR / config["primary_model"]["file"]
)

# Load preprocessing pipeline
preprocessor = joblib.load(
    MODEL_DIR / config["preprocessor"]
)

# Select employee
employee = df.iloc[0]

# Prepare employee features
excluded_columns = [
    "Attrition",
    "EmployeeNumber",
    "EmployeeCount",
    "Over18",
    "StandardHours"
]

employee_features = employee.drop(
    labels=excluded_columns
)

# Transform employee data
employee_processed = preprocessor.transform(
    pd.DataFrame([employee_features])
)

# Predict attrition probability
attrition_probability = rf_model.predict_proba(
    employee_processed
)[0, 1]

# Generate combined retention report
report = generate_employee_retention_report(
    employee,
    float(attrition_probability)
)

# Display results
print("=" * 70)
print("INTEGRATED EMPLOYEE RETENTION ANALYSIS")
print("=" * 70)

print("Employee Number:", employee["EmployeeNumber"])
print("Department:", employee["Department"])
print("Job Role:", employee["JobRole"])

print("\nATTRITION RISK")
print("-" * 70)

print(
    "Attrition Probability:",
    f'{report["attrition_probability"]}%'
)

print("Risk Category:", report["risk_category"])
print("HR Review Priority:", report["review_priority"])

print("\nRETENTION RECOMMENDATIONS")
print("-" * 70)

print("Status:", report["recommendation_status"])

print(
    "Total Recommendations:",
    report["total_recommendations"]
)

for index, item in enumerate(
    report["recommendations"],
    start=1
):
    print(f"\n{index}. {item['category']}")
    print("Risk Indicator:", item["risk_indicator"])
    print("Priority:", item["priority"])
    print("Action:", item["recommendation"])

print("\n" + "=" * 70)
