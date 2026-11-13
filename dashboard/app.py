import shap
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

import streamlit as st
import pandas as pd
import json
import joblib
import sys

from pathlib import Path

# --------------------------------------------------
# PROJECT ROOT AND PYTHON IMPORT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# --------------------------------------------------
# PROJECT MODULE IMPORTS
# --------------------------------------------------

from src.recommendations.retention_engine import (
    generate_employee_retention_report
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI-Powered HR Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("Navigation")

selected_page = st.sidebar.radio(
    "Select Dashboard Section",
    [
        "Overview",
        "Employee Risk Analysis",
        "Global Explainability",
        "Recruitment Matching"
    ]
)


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


# --------------------------------------------------
# APPLICATION TITLE
# --------------------------------------------------

st.title("AI-Powered HR Analytics Dashboard")

st.markdown(
    """
    An integrated platform for:

    - Employee attrition prediction
    - Employee retention recommendations
    - Explainable AI using SHAP
    - AI-assisted recruitment matching

    **Purpose:** Support informed HR decisions through predictive analytics
    and transparent recommendations.
    """
)

st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_employee_data():

    path = RAW_DIR / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

    return pd.read_csv(path)


@st.cache_data
def load_employee_data_from_upload(uploaded_file):

    return pd.read_csv(uploaded_file)


@st.cache_data
def load_retention_analysis():

    path = PROCESSED_DIR / "employee_retention_analysis.csv"

    return pd.read_csv(path)


@st.cache_data
def load_candidate_rankings():

    path = PROCESSED_DIR / "candidate_job_rankings.csv"

    return pd.read_csv(path)


# --------------------------------------------------
# LOAD DATASETS
# --------------------------------------------------

try:

    employee_dataset_path = RAW_DIR / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

    if employee_dataset_path.exists():

        employee_df = load_employee_data()

    else:

        st.warning(
            "The employee attrition dataset is not included in this repository."
        )

        uploaded_file = st.file_uploader(
            "Upload the IBM HR Employee Attrition CSV dataset",
            type=["csv"]
        )

        if uploaded_file is None:
            st.info("Upload the dataset to access Employee Risk Analysis.")
            st.stop()

        employee_df = load_employee_data_from_upload(uploaded_file)

    retention_df = load_retention_analysis()
    candidate_rankings_df = load_candidate_rankings()

    st.success("Employee and recruitment datasets loaded successfully.")

except Exception as e:

    st.error(f"Unable to load datasets: {e}")

    st.stop()


# --------------------------------------------------
# LOAD RANDOM FOREST SHAP EXPLAINER
# --------------------------------------------------

@st.cache_resource
def load_shap_explainer():

    # Load model configuration
    with open(
        MODEL_DIR / "attrition_model_config.json",
        "r"
    ) as file:
        config = json.load(file)

    # Load trained model and preprocessor
    model = joblib.load(
        MODEL_DIR / config["primary_model"]["file"]
    )

    preprocessor = joblib.load(
        MODEL_DIR / config["preprocessor"]
    )

    # Recreate original development and validation splits
    X = employee_df.drop(
        columns=[
            "Attrition",
            "EmployeeNumber",
            "EmployeeCount",
            "Over18",
            "StandardHours"
        ]
    )

    y = employee_df["Attrition"].map({
        "No": 0,
        "Yes": 1
    })

    X_development, X_final_test, y_development, y_final_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )

    X_fit, X_validation, y_fit, y_validation = (
        train_test_split(
            X_development,
            y_development,
            test_size=0.20,
            random_state=42,
            stratify=y_development
        )
    )

    # Recreate the same 100-row background sample
    X_background = X_fit.sample(
        n=100,
        random_state=42
    )

    X_background_processed = preprocessor.transform(
        X_background
    )

    feature_names = preprocessor.get_feature_names_out()

    # Initialize Random Forest explainer
    explainer = shap.TreeExplainer(
        model,
        data=X_background_processed,
        model_output="probability",
        feature_perturbation="interventional"
    )

    return model, preprocessor, explainer, feature_names


try:

    rf_model, shap_preprocessor, rf_explainer, feature_names = (
        load_shap_explainer()
    )

    st.sidebar.success("SHAP explainer loaded successfully.")

except Exception as e:

    st.error(f"Unable to initialize SHAP explainer: {e}")

    st.stop()


# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

total_employees = len(retention_df)

high_risk = (
    retention_df["RiskCategory"] == "High"
).sum()

moderate_risk = (
    retention_df["RiskCategory"] == "Moderate"
).sum()

low_risk = (
    retention_df["RiskCategory"] == "Low"
).sum()

total_recommendations = (
    retention_df["RecommendationCount"].sum()
)


# --------------------------------------------------
# DISPLAY KPI CARDS
# --------------------------------------------------

st.subheader("Workforce Risk Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Employees",
    f"{total_employees:,}"
)

col2.metric(
    "High Risk Employees",
    f"{high_risk:,}"
)

col3.metric(
    "Moderate Risk Employees",
    f"{moderate_risk:,}"
)

col4.metric(
    "Total Recommendations",
    f"{total_recommendations:,}"
)


# --------------------------------------------------
# RISK DISTRIBUTION
# --------------------------------------------------

st.divider()

st.subheader("Employee Attrition Risk Distribution")

risk_distribution = (
    retention_df["RiskCategory"]
    .value_counts()
    .reindex(["Low", "Moderate", "High"], fill_value=0)
)

risk_chart_df = pd.DataFrame({
    "Risk Category": risk_distribution.index,
    "Employees": risk_distribution.values
})

st.bar_chart(
    risk_chart_df,
    x="Risk Category",
    y="Employees"
)


# --------------------------------------------------
# DEPARTMENT ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("Department-wise Average Predicted Attrition Risk")

department_risk = (
    retention_df.groupby("Department")[
        "AttritionProbability"
    ]
    .mean()
    .reset_index()
    .sort_values(
        "AttritionProbability",
        ascending=False
    )
)

department_risk["AttritionProbability"] = (
    department_risk["AttritionProbability"].round(2)
)

st.dataframe(
    department_risk,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# DATASET INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("Dataset Information")

info_col1, info_col2, info_col3 = st.columns(3)

info_col1.metric(
    "Dataset Records",
    f"{len(employee_df):,}"
)

info_col2.metric(
    "Original Dataset Features",
    len(employee_df.columns)
)

info_col3.metric(
    "Departments",
    employee_df["Department"].nunique()
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    """
    AI-Powered Talent Acquisition and Employee Retention Predictive Analytics
    for Workplace Sustainability.

    This dashboard provides decision-support information only.
    Predictions and recommendations must be reviewed by authorized HR personnel.
    """
)


# --------------------------------------------------
# EMPLOYEE RISK ANALYSIS PAGE
# --------------------------------------------------

if selected_page == "Employee Risk Analysis":

    st.title("Employee Risk Analysis")

    st.write(
        "Search and examine individual employee attrition predictions."
    )

    employee_ids = retention_df["EmployeeNumber"].tolist()

    selected_employee_id = st.selectbox(
        "Select Employee Number",
        employee_ids
    )

    selected_employee = retention_df[
        retention_df["EmployeeNumber"] == selected_employee_id
    ].iloc[0]

    original_employee = employee_df[
        employee_df["EmployeeNumber"] == selected_employee_id
    ].iloc[0]

    st.divider()

    st.subheader("Employee Information")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Employee Number",
        int(selected_employee_id)
    )

    col2.metric(
        "Department",
        selected_employee["Department"]
    )

    col3.metric(
        "Job Role",
        selected_employee["JobRole"]
    )

    st.divider()

    st.subheader("Attrition Prediction")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Attrition Probability",
        f'{selected_employee["AttritionProbability"]:.2f}%'
    )

    col2.metric(
        "Risk Category",
        selected_employee["RiskCategory"]
    )

    col3.metric(
        "Review Priority",
        selected_employee["ReviewPriority"]
    )

    st.subheader("Actual vs Predicted Attrition")

    st.write(
        "Actual Attrition:",
        original_employee["Attrition"]
    )

    st.write(
        "Predicted Attrition:",
        "Yes" if selected_employee["AttritionProbability"] >= 50 else "No"
    )


    # --------------------------------------------------
    # RETENTION RECOMMENDATIONS
    # --------------------------------------------------

    st.divider()

    st.subheader("Employee Retention Recommendations")

    # Generate recommendations using original HR attributes
    retention_report = generate_employee_retention_report(
        original_employee,
        float(selected_employee["AttritionProbability"]) / 100
    )

    st.write(
        "Recommendation Status:",
        retention_report["recommendation_status"]
    )

    st.write(
        "Total Recommendations:",
        retention_report["total_recommendations"]
    )

    if retention_report["recommendations"]:

        for index, recommendation in enumerate(
            retention_report["recommendations"],
            start=1
        ):

            with st.expander(
                f"{index}. {recommendation['category']} "
                f"({recommendation['priority']} Priority)"
            ):

                st.write(
                    "**Risk Indicator:**",
                    recommendation["risk_indicator"]
                )

                st.write(
                    "**Recommended Action:**",
                    recommendation["recommendation"]
                )

                st.write(
                    "**Reason:**",
                    recommendation["reason"]
                )

    else:

        st.info(
            "No specific intervention triggers were identified. "
            "This does not mean that the employee has no retention needs."
        )


    # --------------------------------------------------
    # INDIVIDUAL SHAP EXPLAINABILITY
    # --------------------------------------------------

    st.divider()

    st.subheader("Explainable AI - Individual SHAP Analysis")

    st.write(
        "Understand which employee attributes influence "
        "the model's attrition prediction."
    )

    if st.button("Generate SHAP Explanation"):

        with st.spinner("Calculating individual SHAP values..."):

            # Prepare original employee features
            excluded_columns = [
                "Attrition",
                "EmployeeNumber",
                "EmployeeCount",
                "Over18",
                "StandardHours"
            ]

            employee_features = original_employee.drop(
                labels=excluded_columns
            )

            # Transform employee data
            employee_processed = shap_preprocessor.transform(
                pd.DataFrame([employee_features])
            )

            # Calculate SHAP values
            shap_values = rf_explainer.shap_values(
                employee_processed
            )

            # Extract Attrition = Yes contributions
            positive_shap = np.asarray(
                shap_values
            )[0, :, 1]

            # Extract feature values
            feature_values = (
                employee_processed.toarray()[0]
                if hasattr(employee_processed, "toarray")
                else np.asarray(employee_processed)[0]
            )

            # Create SHAP explanation
            explanation = shap.Explanation(
                values=positive_shap,
                base_values=float(
                    rf_explainer.expected_value[1]
                ),
                data=feature_values,
                feature_names=feature_names
            )

            # Display feature contributions
            contribution_df = pd.DataFrame({
                "Feature": feature_names,
                "SHAP Value": positive_shap
            })

            contribution_df["Absolute SHAP"] = (
                contribution_df["SHAP Value"].abs()
            )

            contribution_df["Direction"] = np.where(
                contribution_df["SHAP Value"] > 0,
                "Increases attrition risk",
                "Decreases attrition risk"
            )

            contribution_df = contribution_df.sort_values(
                "Absolute SHAP",
                ascending=False
            )

            st.subheader("Top Contributing Features")

            st.dataframe(
                contribution_df.head(10),
                use_container_width=True,
                hide_index=True
            )

            # Generate waterfall plot
            shap.plots.waterfall(
                explanation,
                max_display=20,
                show=False
            )

            fig = plt.gcf()

            st.subheader("Individual SHAP Waterfall Plot")

            st.pyplot(fig)

            plt.close(fig)

            # Verify SHAP reconstruction
            reconstructed_probability = (
                explanation.base_values +
                explanation.values.sum()
            )

            st.write(
                "Model predicted probability:",
                f"{selected_employee['AttritionProbability'] / 100:.4f}"
            )

            st.write(
                "SHAP reconstructed probability:",
                f"{reconstructed_probability:.4f}"
            )


# --------------------------------------------------
# GLOBAL EXPLAINABILITY PAGE
# --------------------------------------------------

if selected_page == "Global Explainability":

    st.title("Global Explainable AI Analysis")

    st.write(
        "Explore the features that influence attrition predictions "
        "across the validation dataset."
    )

    st.info(
        "These visualizations explain the Random Forest and "
        "Logistic Regression models. SHAP values from the two "
        "models use different output scales and should not be "
        "compared by magnitude."
    )

    st.divider()

    # Random Forest global importance
    st.subheader("Random Forest - Global Feature Importance")

    rf_importance_path = (
        FIGURES_DIR / "16_rf_shap_global_importance.png"
    )

    if rf_importance_path.exists():
        st.image(
            str(rf_importance_path),
            use_container_width=True
        )
    else:
        st.warning("Random Forest importance figure not found.")

    st.divider()

    # Random Forest summary plot
    st.subheader("Random Forest - SHAP Summary Plot")

    rf_summary_path = (
        FIGURES_DIR / "17_rf_shap_summary.png"
    )

    if rf_summary_path.exists():
        st.image(
            str(rf_summary_path),
            use_container_width=True
        )
    else:
        st.warning("Random Forest summary figure not found.")

    st.divider()

    # Logistic Regression global importance
    st.subheader("Logistic Regression - Global Feature Importance")

    lr_importance_path = (
        FIGURES_DIR / "18_lr_shap_global_importance.png"
    )

    if lr_importance_path.exists():
        st.image(
            str(lr_importance_path),
            use_container_width=True
        )
    else:
        st.warning("Logistic Regression importance figure not found.")

    st.divider()

    # Logistic Regression summary plot
    st.subheader("Logistic Regression - SHAP Summary Plot")

    lr_summary_path = (
        FIGURES_DIR / "19_lr_shap_summary.png"
    )

    if lr_summary_path.exists():
        st.image(
            str(lr_summary_path),
            use_container_width=True
        )
    else:
        st.warning("Logistic Regression summary figure not found.")

    st.divider()

    st.subheader("Interpretation Guidelines")

    st.markdown(
        """
        - **SHAP value:** Measures a feature's contribution to an individual prediction.
        - **Positive SHAP value:** Pushes the prediction towards Attrition = Yes.
        - **Negative SHAP value:** Pushes the prediction towards Attrition = No.
        - **Mean absolute SHAP:** Measures average feature contribution magnitude.
        - **Beeswarm plot:** Shows the distribution and direction of contributions
          across employees.

        SHAP explains model behavior, not causal relationships.
        """
    )


# --------------------------------------------------
# RECRUITMENT MATCHING PAGE
# --------------------------------------------------

if selected_page == "Recruitment Matching":

    st.title("AI-Assisted Recruitment Matching")

    st.write(
        "Evaluate and rank candidates against job requirements "
        "using a transparent, weighted suitability-scoring system."
    )

    st.info(
        "This module provides decision support only. "
        "Final recruitment decisions must involve human review."
    )

    # Job selection
    job_options = (
        candidate_rankings_df[["job_id", "job_title"]]
        .drop_duplicates()
        .sort_values("job_id")
    )

    selected_job = st.selectbox(
        "Select Job Position",
        job_options["job_id"],
        format_func=lambda job_id: (
            job_options.loc[
                job_options["job_id"] == job_id,
                "job_title"
            ].iloc[0]
        )
    )

    # Filter candidate rankings
    job_candidates = candidate_rankings_df[
        candidate_rankings_df["job_id"] == selected_job
    ].copy()

    job_candidates = job_candidates.sort_values("rank")

    st.divider()


    # Recruitment overview
    st.subheader("Recruitment Overview")

    total_candidates = len(job_candidates)

    meets_requirements = int(
        job_candidates["meets_minimum_requirements"].sum()
    )

    requires_review = total_candidates - meets_requirements

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Candidates Evaluated", total_candidates)

    with col2:
        st.metric("Meets Minimum Requirements", meets_requirements)

    with col3:
        st.metric("Requires Human Review", requires_review)

    st.divider()

    # Candidate rankings
    st.subheader("Candidate Rankings")

    display_columns = [
        "rank",
        "candidate_id",
        "candidate_name",
        "overall_score",
        "skills_score",
        "experience_score",
        "education_score",
        "certifications_score",
        "projects_score",
        "review_status"
    ]

    st.dataframe(
        job_candidates[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Candidate comparison
    st.subheader("Candidate Comparison")

    st.write(
        "Select two candidates to compare their suitability "
        "for the selected job position."
    )

    comparison_candidates = job_candidates[
        ["candidate_id", "candidate_name"]
    ].drop_duplicates()

    candidate_options = {
        f"{row['candidate_name']} ({row['candidate_id']})":
        row["candidate_id"]
        for _, row in comparison_candidates.iterrows()
    }

    if len(candidate_options) < 2:
        st.info("At least two candidates are required for comparison.")

    else:
        col1, col2 = st.columns(2)

        with col1:
            candidate_1_label = st.selectbox(
                "Select First Candidate",
                list(candidate_options.keys()),
                key="comparison_candidate_1"
            )

        with col2:
            candidate_2_options = [
                label for label in candidate_options
                if label != candidate_1_label
            ]

            candidate_2_label = st.selectbox(
                "Select Second Candidate",
                candidate_2_options,
                key="comparison_candidate_2"
            )

        candidate_1_id = candidate_options[candidate_1_label]
        candidate_2_id = candidate_options[candidate_2_label]

        candidate_1 = job_candidates[
            job_candidates["candidate_id"] == candidate_1_id
        ].iloc[0]

        candidate_2 = job_candidates[
            job_candidates["candidate_id"] == candidate_2_id
        ].iloc[0]

        comparison_metrics = {
            "Overall Score": "overall_score",
            "Skills Score": "skills_score",
            "Experience Score": "experience_score",
            "Education Score": "education_score",
            "Certifications Score": "certifications_score",
            "Projects Score": "projects_score"
        }

        comparison_data = pd.DataFrame({
            "Metric": comparison_metrics.keys(),
            candidate_1_label: [
                candidate_1[column]
                for column in comparison_metrics.values()
            ],
            candidate_2_label: [
                candidate_2[column]
                for column in comparison_metrics.values()
            ]
        })

        st.subheader("Side-by-Side Score Comparison")

        st.dataframe(
            comparison_data,
            use_container_width=True,
            hide_index=True
        )


        st.subheader("Candidate Strengths and Gaps")

        def safe_display(value, fallback="None recorded."):
            if pd.isna(value) or str(value).strip() == "":
                return fallback
            return str(value)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**{candidate_1_label}**")

            st.markdown("**Strengths**")
            st.write(safe_display(candidate_1["strengths"]))

            st.markdown("**Gaps**")
            st.write(safe_display(candidate_1["gaps"]))

            st.markdown("**Missing Required Skills**")
            st.write(
                safe_display(
                    candidate_1["missing_required_skills"],
                    "No missing required skills."
                )
            )

        with col2:
            st.markdown(f"**{candidate_2_label}**")

            st.markdown("**Strengths**")
            st.write(safe_display(candidate_2["strengths"]))

            st.markdown("**Gaps**")
            st.write(safe_display(candidate_2["gaps"]))

            st.markdown("**Missing Required Skills**")
            st.write(
                safe_display(
                    candidate_2["missing_required_skills"],
                    "No missing required skills."
                )
            )

        st.info(
            "This comparison is decision-support information only. "
            "Final recruitment decisions require human review."
        )
