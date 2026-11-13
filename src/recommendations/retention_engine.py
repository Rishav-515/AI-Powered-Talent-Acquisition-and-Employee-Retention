
"""
Employee Retention Recommendation Engine

Generates human-reviewable retention recommendations
based on employee HR attributes.

This module does not make employment decisions.
"""

import pandas as pd


def generate_retention_recommendations(employee):
    """
    Generate retention recommendations for one employee.

    Parameters
    ----------
    employee : pandas.Series or dict
        Employee HR attributes from the IBM HR dataset.

    Returns
    -------
    list
        List of recommendation dictionaries.
    """

    recommendations = []

    # Convert input to dictionary if necessary
    if isinstance(employee, pd.Series):
        employee = employee.to_dict()

    def add_recommendation(
        category,
        risk_indicator,
        recommendation,
        reason,
        priority="Medium"
    ):
        recommendations.append({
            "category": category,
            "risk_indicator": risk_indicator,
            "recommendation": recommendation,
            "reason": reason,
            "priority": priority
        })

    # --------------------------------------------------
    # 1. OVERTIME
    # --------------------------------------------------

    if employee.get("OverTime") == "Yes":

        add_recommendation(
            category="Workload Management",
            risk_indicator="Frequent overtime",
            recommendation=(
                "Review workload distribution, staffing levels "
                "and opportunities to reduce excessive overtime."
            ),
            reason=(
                "The employee is recorded as working overtime. "
                "HR should investigate workload sustainability."
            ),
            priority="High"
        )

    # --------------------------------------------------
    # 2. JOB SATISFACTION
    # --------------------------------------------------

    job_satisfaction = employee.get("JobSatisfaction")

    if pd.notna(job_satisfaction) and job_satisfaction <= 2:

        add_recommendation(
            category="Employee Engagement",
            risk_indicator="Low job satisfaction",
            recommendation=(
                "Conduct an employee feedback discussion to identify "
                "concerns related to responsibilities, management "
                "or the work environment."
            ),
            reason=(
                "The recorded job satisfaction score is low."
            ),
            priority="High"
        )

    # --------------------------------------------------
    # 3. WORK-LIFE BALANCE
    # --------------------------------------------------

    work_life_balance = employee.get("WorkLifeBalance")

    if pd.notna(work_life_balance) and work_life_balance <= 2:

        add_recommendation(
            category="Work-Life Balance",
            risk_indicator="Low work-life balance",
            recommendation=(
                "Review workload expectations, scheduling flexibility "
                "and opportunities for improved work-life balance."
            ),
            reason=(
                "The employee has a low recorded work-life balance score."
            ),
            priority="High"
        )

    # --------------------------------------------------
    # 4. ENVIRONMENT SATISFACTION
    # --------------------------------------------------

    environment_satisfaction = employee.get(
        "EnvironmentSatisfaction"
    )

    if (
        pd.notna(environment_satisfaction)
        and environment_satisfaction <= 2
    ):

        add_recommendation(
            category="Work Environment",
            risk_indicator="Low environment satisfaction",
            recommendation=(
                "Discuss workplace concerns and evaluate improvements "
                "to the employee's working environment."
            ),
            reason=(
                "The recorded environment satisfaction score is low."
            ),
            priority="Medium"
        )

    # --------------------------------------------------
    # 5. RELATIONSHIP SATISFACTION
    # --------------------------------------------------

    relationship_satisfaction = employee.get(
        "RelationshipSatisfaction"
    )

    if (
        pd.notna(relationship_satisfaction)
        and relationship_satisfaction <= 2
    ):

        add_recommendation(
            category="Workplace Relationships",
            risk_indicator="Low relationship satisfaction",
            recommendation=(
                "Review team dynamics and offer appropriate "
                "managerial support or conflict resolution."
            ),
            reason=(
                "The recorded relationship satisfaction score is low."
            ),
            priority="Medium"
        )

    # --------------------------------------------------
    # 6. CAREER PROGRESSION
    # --------------------------------------------------

    years_since_promotion = employee.get(
        "YearsSinceLastPromotion"
    )

    if (
        pd.notna(years_since_promotion)
        and years_since_promotion >= 5
    ):

        add_recommendation(
            category="Career Development",
            risk_indicator="Long period without promotion",
            recommendation=(
                "Review career progression, promotion eligibility "
                "and opportunities for increased responsibilities."
            ),
            reason=(
                "The employee has not received a promotion for "
                "five or more years."
            ),
            priority="Medium"
        )

    # --------------------------------------------------
    # 7. MANAGERIAL SUPPORT
    # --------------------------------------------------

    years_with_manager = employee.get(
        "YearsWithCurrManager"
    )

    if (
        pd.notna(years_with_manager)
        and years_with_manager >= 7
    ):

        add_recommendation(
            category="Career and Managerial Support",
            risk_indicator="Long tenure under current manager",
            recommendation=(
                "Conduct a career development discussion with the "
                "employee and review whether additional mentoring, "
                "role expansion or internal mobility would be useful."
            ),
            reason=(
                "The employee has worked with the same manager "
                "for seven or more years. This is a prompt for review, "
                "not evidence of a problem."
            ),
            priority="Low"
        )

    # --------------------------------------------------
    # 8. JOB INVOLVEMENT
    # --------------------------------------------------

    job_involvement = employee.get("JobInvolvement")

    if pd.notna(job_involvement) and job_involvement <= 2:

        add_recommendation(
            category="Employee Engagement",
            risk_indicator="Low job involvement",
            recommendation=(
                "Discuss role expectations, employee interests "
                "and opportunities for meaningful participation "
                "in team activities."
            ),
            reason=(
                "The recorded job involvement score is low."
            ),
            priority="Medium"
        )

    # --------------------------------------------------
    # RETURN RESULTS
    # --------------------------------------------------

    return recommendations


def generate_recommendation_summary(employee):
    """
    Generate a structured retention recommendation summary.
    """

    recommendations = generate_retention_recommendations(employee)

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    recommendations.sort(
        key=lambda item: priority_order[item["priority"]]
    )

    if not recommendations:
        return {
            "status": "No specific intervention triggers identified",
            "total_recommendations": 0,
            "recommendations": []
        }

    return {
        "status": "Human review recommended",
        "total_recommendations": len(recommendations),
        "recommendations": recommendations
    }

def classify_attrition_risk(probability):
    """
    Classify employee attrition risk using predicted probability.

    Risk thresholds:
        Below 0.30       -> Low
        0.30 to below 0.60 -> Moderate
        0.60 and above   -> High

    Parameters
    ----------
    probability : float
        Predicted attrition probability between 0 and 1.

    Returns
    -------
    str
        Low, Moderate, or High
    """

    if not isinstance(probability, (int, float)):
        raise TypeError("Probability must be a numeric value.")

    if not 0 <= probability <= 1:
        raise ValueError("Probability must be between 0 and 1.")

    if probability < 0.30:
        return "Low"

    elif probability < 0.60:
        return "Moderate"

    else:
        return "High"


def generate_employee_retention_report(employee, attrition_probability):
    """
    Generate a combined employee attrition risk and
    retention recommendation report.

    Parameters
    ----------
    employee : pandas.Series or dict
        Original employee HR attributes.

    attrition_probability : float
        Random Forest predicted attrition probability.

    Returns
    -------
    dict
        Employee risk classification and recommendations.
    """

    # Classify attrition risk
    risk_category = classify_attrition_risk(
        attrition_probability
    )

    # Generate retention recommendations
    recommendation_summary = generate_recommendation_summary(
        employee
    )

    # Convert probability into percentage
    risk_percentage = round(
        attrition_probability * 100, 2
    )

    # Determine HR review priority
    if risk_category == "High":
        review_priority = "High"

    elif risk_category == "Moderate":
        review_priority = "Medium"

    else:
        review_priority = "Low"

    return {
        "attrition_probability": risk_percentage,
        "risk_category": risk_category,
        "review_priority": review_priority,
        "recommendation_status": recommendation_summary["status"],
        "total_recommendations": recommendation_summary[
            "total_recommendations"
        ],
        "recommendations": recommendation_summary[
            "recommendations"
        ]
    }
