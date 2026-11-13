
import pandas as pd

from src.recruitment.matching_engine import (
    calculate_skill_match,
    calculate_experience_match,
    calculate_education_match,
    calculate_certification_match,
    calculate_project_relevance,
    calculate_candidate_suitability,
    rank_candidates,
    compare_candidates,
)


def test_candidate_with_no_skills():
    candidate = {"skills": ""}
    job = {
        "required_skills": "Python; SQL",
        "preferred_skills": "Flask",
    }

    result = calculate_skill_match(candidate, job)

    assert result["score"] == 0
    assert result["missing_required_skills"] == ["python", "sql"]


def test_candidate_with_zero_experience():
    candidate = {"experience_years": 0}
    job = {"minimum_experience": 0}

    result = calculate_experience_match(candidate, job)

    assert result["score"] == 100
    assert result["meets_requirement"] is True


def test_candidate_below_minimum_experience():
    candidate = {"experience_years": 0}
    job = {"minimum_experience": 1}

    result = calculate_experience_match(candidate, job)

    assert result["score"] == 75
    assert result["meets_requirement"] is False


def test_candidate_with_insufficient_education():
    candidate = {
        "education_level": "diploma",
        "specialization": "Computer Science",
    }
    job = {
        "minimum_education": "bachelor's",
        "required_specialization": "Computer Science",
    }

    result = calculate_education_match(candidate, job)

    assert result["score"] == 0
    assert result["education_level_match"] is False


def test_candidate_missing_required_certifications():
    candidate = {"certifications": ""}
    job = {
        "required_certifications": "Python Certification",
        "preferred_certifications": "",
    }

    result = calculate_certification_match(candidate, job)

    assert result["score"] == 0
    assert result["has_required_certifications"] is False


def test_candidate_with_no_projects():
    candidate = {
        "projects": "",
        "project_domains": "",
    }
    job = {
        "job_title": "Python Developer",
        "job_description": "Python backend development",
    }

    result = calculate_project_relevance(candidate, job)

    assert result["score"] == 0
    assert result["relevance"] == "None"


def test_empty_candidate_dataframe_ranking():
    candidates = pd.DataFrame()
    job = {"job_id": "JOB001", "job_title": "Python Developer"}

    result = rank_candidates(candidates, job)

    assert result == []


def test_empty_candidate_comparison():
    candidates = pd.DataFrame(columns=["candidate_id"])
    job = {"job_id": "JOB001", "job_title": "Python Developer"}

    result = compare_candidates(candidates, job, [])

    assert result == []


def test_candidate_with_none_project_information():
    candidate = {
        "projects": None,
        "project_domains": None,
    }
    job = {
        "job_title": "Python Developer",
        "job_description": "Python backend development",
    }

    result = calculate_project_relevance(candidate, job)

    assert result["score"] == 0
    assert result["relevance"] == "None"
