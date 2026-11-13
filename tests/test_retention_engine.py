
import pandas as pd

from src.recommendations.retention_engine import (
    generate_retention_recommendations,
    generate_recommendation_summary
)


def test_overtime_recommendation():

    employee = pd.Series({
        "OverTime": "Yes",
        "JobSatisfaction": 3,
        "WorkLifeBalance": 3
    })

    results = generate_retention_recommendations(employee)

    assert any(
        item["category"] == "Workload Management"
        for item in results
    )


def test_low_satisfaction_recommendation():

    employee = pd.Series({
        "JobSatisfaction": 1
    })

    results = generate_retention_recommendations(employee)

    assert any(
        item["category"] == "Employee Engagement"
        for item in results
    )


def test_multiple_recommendations():

    employee = pd.Series({
        "OverTime": "Yes",
        "JobSatisfaction": 1,
        "WorkLifeBalance": 1,
        "YearsSinceLastPromotion": 6
    })

    results = generate_retention_recommendations(employee)

    assert len(results) == 4


def test_no_recommendations():

    employee = pd.Series({
        "OverTime": "No",
        "JobSatisfaction": 4,
        "WorkLifeBalance": 4,
        "EnvironmentSatisfaction": 4,
        "RelationshipSatisfaction": 4,
        "YearsSinceLastPromotion": 1,
        "YearsWithCurrManager": 2,
        "JobInvolvement": 4
    })

    results = generate_recommendation_summary(employee)

    assert results["total_recommendations"] == 0


def test_recommendation_priority():

    employee = pd.Series({
        "OverTime": "Yes",
        "JobSatisfaction": 1,
        "YearsSinceLastPromotion": 6
    })

    results = generate_recommendation_summary(employee)

    priorities = [
        item["priority"]
        for item in results["recommendations"]
    ]

    assert priorities == sorted(
        priorities,
        key=lambda p: {"High": 1, "Medium": 2, "Low": 3}[p]
    )


if __name__ == "__main__":
    print("Run using: python -m pytest tests/test_retention_engine.py -v")


from src.recommendations.retention_engine import classify_attrition_risk


def test_low_attrition_risk():
    assert classify_attrition_risk(0.20) == "Low"


def test_moderate_attrition_risk():
    assert classify_attrition_risk(0.45) == "Moderate"


def test_high_attrition_risk():
    assert classify_attrition_risk(0.75) == "High"


def test_risk_boundary_values():
    assert classify_attrition_risk(0.30) == "Moderate"
    assert classify_attrition_risk(0.60) == "High"
    assert classify_attrition_risk(0.00) == "Low"
    assert classify_attrition_risk(1.00) == "High"


def test_invalid_probability():
    import pytest

    with pytest.raises(ValueError):
        classify_attrition_risk(1.5)

    with pytest.raises(ValueError):
        classify_attrition_risk(-0.1)
