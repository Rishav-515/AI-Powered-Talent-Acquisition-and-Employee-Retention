
import pandas as pd

from src.recommendations.retention_engine import (
    generate_recommendation_summary
)

# Load IBM HR dataset
DATA_PATH = "data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv"

df = pd.read_csv(DATA_PATH)

# Select one employee for testing
employee = df.iloc[0]

# Generate recommendations
result = generate_recommendation_summary(employee)

print("=" * 65)
print("REAL EMPLOYEE RETENTION RECOMMENDATION TEST")
print("=" * 65)

print("Employee Number:", employee["EmployeeNumber"])
print("Department:", employee["Department"])
print("Job Role:", employee["JobRole"])
print("Overtime:", employee["OverTime"])
print("Job Satisfaction:", employee["JobSatisfaction"])
print("Work-Life Balance:", employee["WorkLifeBalance"])

print("\nRecommendation Status:", result["status"])
print("Total Recommendations:", result["total_recommendations"])

for index, recommendation in enumerate(
    result["recommendations"], start=1
):
    print(f"\nRecommendation {index}")
    print("Category:", recommendation["category"])
    print("Risk Indicator:", recommendation["risk_indicator"])
    print("Priority:", recommendation["priority"])
    print("Action:", recommendation["recommendation"])
    print("Reason:", recommendation["reason"])
