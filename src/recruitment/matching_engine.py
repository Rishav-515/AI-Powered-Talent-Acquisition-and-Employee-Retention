
"""
Candidate Recruitment Matching Engine

Milestone 7:
Transparent, rule-based candidate-to-job matching.
"""

# --------------------------------------------------
# 1. SKILL NORMALIZATION
# --------------------------------------------------

def normalize_skill(skill):
    """
    Normalize skill names for consistent comparison.
    """

    return skill.strip().lower()


def parse_skills(skill_string):
    """
    Convert semicolon-separated skills into a normalized set.
    """

    if not skill_string or not isinstance(skill_string, str):
        return set()

    return {
        normalize_skill(skill)
        for skill in skill_string.split(";")
        if skill.strip()
    }


# --------------------------------------------------
# 2. SKILL MATCHING
# --------------------------------------------------

def calculate_skill_match(candidate, job):
    """
    Compare candidate skills against required and preferred skills.

    Required skills carry 80% of the skill score.
    Preferred skills carry 20% of the skill score.

    Returns:
        Dictionary containing:
        - score
        - matched_required_skills
        - missing_required_skills
        - matched_preferred_skills
        - missing_preferred_skills
    """

    candidate_skills = parse_skills(candidate.get("skills", ""))

    required_skills = parse_skills(job.get("required_skills", ""))

    preferred_skills = parse_skills(job.get("preferred_skills", ""))

    # Required skill matching
    matched_required = candidate_skills.intersection(required_skills)

    missing_required = required_skills - candidate_skills

    # Preferred skill matching
    matched_preferred = candidate_skills.intersection(preferred_skills)

    missing_preferred = preferred_skills - candidate_skills

    # Calculate required skill score
    if required_skills:
        required_score = (
            len(matched_required) / len(required_skills)
        ) * 100
    else:
        required_score = 100

    # Calculate preferred skill score
    if preferred_skills:
        preferred_score = (
            len(matched_preferred) / len(preferred_skills)
        ) * 100
    else:
        preferred_score = 100

    # Combine required and preferred scores
    skill_score = (
        required_score * 0.80
        + preferred_score * 0.20
    )

    return {
        "score": round(skill_score, 2),
        "required_score": round(required_score, 2),
        "preferred_score": round(preferred_score, 2),
        "matched_required_skills": sorted(matched_required),
        "missing_required_skills": sorted(missing_required),
        "matched_preferred_skills": sorted(matched_preferred),
        "missing_preferred_skills": sorted(missing_preferred)
    }


# --------------------------------------------------
# 3. EXPERIENCE MATCHING
# --------------------------------------------------

def calculate_experience_match(candidate, job):
    """
    Evaluate candidate experience against job requirements.

    Returns:
        score: Experience matching score out of 100.
        meets_requirement: Whether minimum experience is met.
        experience_gap: Number of years below requirement.
    """

    candidate_experience = float(
        candidate.get("experience_years", 0)
    )

    required_experience = float(
        job.get("minimum_experience", 0)
    )

    experience_gap = max(
        0,
        required_experience - candidate_experience
    )

    if experience_gap == 0:
        score = 100

    elif experience_gap == 1:
        score = 75

    elif experience_gap == 2:
        score = 50

    elif experience_gap == 3:
        score = 25

    else:
        score = 0

    return {
        "score": score,
        "meets_requirement": experience_gap == 0,
        "candidate_experience": candidate_experience,
        "required_experience": required_experience,
        "experience_gap": experience_gap
    }


# --------------------------------------------------
# 4. EDUCATION MATCHING
# --------------------------------------------------

def calculate_education_match(candidate, job):
    """
    Evaluate candidate education against job requirements.

    Returns:
        score: Education matching score.
        education_level_match: Whether education level is sufficient.
        specialization_match: Whether specialization is relevant.
    """

    education_hierarchy = {
        "high school": 1,
        "diploma": 2,
        "bachelor's": 3,
        "master's": 4,
        "phd": 5
    }

    candidate_education = str(
        candidate.get("education_level", "")
    ).strip().lower()

    required_education = str(
        job.get("minimum_education", "")
    ).strip().lower()

    candidate_level = education_hierarchy.get(
        candidate_education, 0
    )

    required_level = education_hierarchy.get(
        required_education, 0
    )

    education_level_match = (
        candidate_level >= required_level
        and required_level > 0
    )

    candidate_specialization = str(
        candidate.get("specialization", "")
    ).strip().lower()

    required_specializations = {
        item.strip().lower()
        for item in str(
            job.get("required_specialization", "")
        ).split(";")
        if item.strip()
    }

    specialization_match = (
        candidate_specialization in required_specializations
    )

    if not education_level_match:
        score = 0

    elif specialization_match:
        score = 100

    else:
        score = 70

    return {
        "score": score,
        "education_level_match": education_level_match,
        "specialization_match": specialization_match,
        "candidate_education": candidate_education,
        "required_education": required_education,
        "candidate_specialization": candidate_specialization,
        "required_specializations": sorted(
            required_specializations
        )
    }


# --------------------------------------------------
# 5. CERTIFICATION MATCHING
# --------------------------------------------------


def calculate_certification_match(candidate, job):
    """
    Compare candidate certifications against mandatory and
    preferred job certifications.

    Mandatory certifications: 70% of certification score.
    Preferred certifications: 30% of certification score.

    If a category is not specified, its weight is redistributed
    to the category that is specified.
    """

    candidate_certifications = parse_skills(
        candidate.get("certifications", "")
    )

    required_certifications = parse_skills(
        job.get("required_certifications", "")
    )

    preferred_certifications = parse_skills(
        job.get("preferred_certifications", "")
    )

    matched_required = (
        candidate_certifications.intersection(
            required_certifications
        )
    )

    missing_required = (
        required_certifications - candidate_certifications
    )

    matched_preferred = (
        candidate_certifications.intersection(
            preferred_certifications
        )
    )

    missing_preferred = (
        preferred_certifications - candidate_certifications
    )

    # Calculate mandatory certification score
    if required_certifications:
        required_score = (
            len(matched_required) / len(required_certifications)
        ) * 100
    else:
        required_score = None

    # Calculate preferred certification score
    if preferred_certifications:
        preferred_score = (
            len(matched_preferred) / len(preferred_certifications)
        ) * 100
    else:
        preferred_score = None

    # Calculate combined certification score
    if required_score is not None and preferred_score is not None:
        score = (required_score * 0.70) + (preferred_score * 0.30)

    elif required_score is not None:
        score = required_score

    elif preferred_score is not None:
        score = preferred_score

    else:
        score = 100

    return {
        "score": round(score, 2),

        "required_score": (
            round(required_score, 2)
            if required_score is not None else None
        ),

        "preferred_score": (
            round(preferred_score, 2)
            if preferred_score is not None else None
        ),

        "matched_certifications": sorted(
            matched_required
        ),

        "missing_certifications": sorted(
            missing_required
        ),

        "matched_preferred_certifications": sorted(
            matched_preferred
        ),

        "missing_preferred_certifications": sorted(
            missing_preferred
        ),

        "has_required_certifications": (
            len(missing_required) == 0
        )
    }



# --------------------------------------------------
# 6. PROJECT RELEVANCE MATCHING
# --------------------------------------------------

def calculate_project_relevance(candidate, job):
    """
    Evaluate project relevance using candidate project domains,
    project titles, job title, and job description.
    """

    raw_domain = candidate.get("project_domains", "")
    raw_projects = candidate.get("projects", "")

    candidate_domain = (
        str(raw_domain).strip().lower()
        if raw_domain is not None else ""
    )

    candidate_projects = (
        str(raw_projects).strip().lower()
        if raw_projects is not None else ""
    )

    job_title = str(
        job.get("job_title", "")
    ).strip().lower()

    job_description = str(
        job.get("job_description", "")
    ).strip().lower()

    # Map job titles to relevant project domains
    job_domain_mapping = {
        "python developer": ["backend development"],
        "backend developer": ["backend development"],
        "data analyst": ["data analytics"],
        "machine learning engineer": ["machine learning"],
        "full stack developer": ["full stack development"]
    }

    relevant_domains = job_domain_mapping.get(
        job_title, []
    )

    # Domain-based matching
    domain_match = candidate_domain in relevant_domains

    # Keyword-based project matching
    job_keywords = set(
        job_title.replace("-", " ").split()
    )

    project_keywords = set(
        candidate_projects.replace("-", " ").split()
    )

    title_keyword_match = bool(
        job_keywords.intersection(project_keywords)
    )

    # Determine project relevance score
    if domain_match:
        score = 100
        relevance = "High"

    elif title_keyword_match:
        score = 75
        relevance = "Moderate"

    elif candidate_projects:
        score = 50
        relevance = "Partial"

    else:
        score = 0
        relevance = "None"

    return {
        "score": score,
        "relevance": relevance,
        "domain_match": domain_match,
        "title_keyword_match": title_keyword_match,
        "candidate_project_domains": candidate_domain,
        "candidate_projects": candidate_projects
    }


# --------------------------------------------------
# 7. OVERALL CANDIDATE SUITABILITY SCORE
# --------------------------------------------------

def calculate_candidate_suitability(candidate, job):
    """
    Calculate the overall candidate suitability score
    using five weighted components.

    This score is decision-support information only.
    It does not automatically select or reject candidates.
    """

    # Calculate individual component scores
    skill_result = calculate_skill_match(candidate, job)

    experience_result = calculate_experience_match(
        candidate, job
    )

    education_result = calculate_education_match(
        candidate, job
    )

    certification_result = calculate_certification_match(
        candidate, job
    )

    project_result = calculate_project_relevance(
        candidate, job
    )

    # Component weights
    weights = {
        "skills": 0.50,
        "experience": 0.20,
        "education": 0.15,
        "certifications": 0.10,
        "projects": 0.05
    }

    # Calculate weighted suitability score
    final_score = (
        skill_result["score"] * weights["skills"]
        + experience_result["score"] * weights["experience"]
        + education_result["score"] * weights["education"]
        + certification_result["score"] * weights["certifications"]
        + project_result["score"] * weights["projects"]
    )

    # Collect strengths and gaps
    strengths = []
    gaps = []

    if skill_result["matched_required_skills"]:
        strengths.append(
            "Matched required skills: "
            + ", ".join(
                skill_result["matched_required_skills"]
            )
        )

    if skill_result["missing_required_skills"]:
        gaps.append(
            "Missing required skills: "
            + ", ".join(
                skill_result["missing_required_skills"]
            )
        )

    if experience_result["meets_requirement"]:
        strengths.append("Meets minimum experience requirement")
    else:
        gaps.append(
            f"Experience shortfall: "
            f"{experience_result['experience_gap']} years"
        )

    if education_result["education_level_match"]:
        strengths.append("Meets minimum education requirement")
    else:
        gaps.append("Does not meet minimum education requirement")

    if education_result["specialization_match"]:
        strengths.append("Relevant academic specialization")

    if certification_result["has_required_certifications"]:
        strengths.append("Meets mandatory certification requirements")
    else:
        gaps.append(
            "Missing required certifications: "
            + ", ".join(
                certification_result["missing_certifications"]
            )
        )

    if project_result["relevance"] == "High":
        strengths.append("Strongly relevant project experience")
    elif project_result["relevance"] == "None":
        gaps.append("No relevant projects identified")

    meets_minimum_requirements = (
    experience_result["meets_requirement"]
    and education_result["education_level_match"]
    and certification_result["has_required_certifications"]
    )

    review_status = (
        "Meets minimum requirements"
        if meets_minimum_requirements
        else "Requires human review"
    )

    return {
        "candidate_id": candidate.get("candidate_id"),
        "candidate_name": candidate.get("candidate_name"),
        "job_id": job.get("job_id"),
        "job_title": job.get("job_title"),

        "overall_score": round(final_score, 2),

        "component_scores": {
            "skills": skill_result["score"],
            "experience": experience_result["score"],
            "education": education_result["score"],
            "certifications": certification_result["score"],
            "projects": project_result["score"]
        },

        "skill_details": skill_result,
        "experience_details": experience_result,
        "education_details": education_result,
        "certification_details": certification_result,
        "project_details": project_result,

        "strengths": strengths,
        "gaps": gaps,

        "meets_experience_requirement":
            experience_result["meets_requirement"],

        "meets_education_requirement":
            education_result["education_level_match"],

        "meets_certification_requirement":
            certification_result["has_required_certifications"],

        "meets_minimum_requirements": meets_minimum_requirements,
        "review_status": review_status
    }


# --------------------------------------------------
# 8. RANK CANDIDATES FOR A JOB
# --------------------------------------------------

def rank_candidates(candidates, job):
    """
    Evaluate and rank all candidates against a selected job.

    Candidates are ranked by overall suitability score.
    This ranking supports human review and is not an
    automatic hiring decision.
    """

    results = []

    for _, candidate in candidates.iterrows():

        candidate_data = candidate.to_dict()

        result = calculate_candidate_suitability(
            candidate_data,
            job
        )

        results.append(result)

    # Sort by overall score, highest first
    ranked_results = sorted(
        results,
        key=lambda x: x["overall_score"],
        reverse=True
    )

    # Assign ranking positions
    for rank, result in enumerate(
        ranked_results,
        start=1
    ):
        result["rank"] = rank

    return ranked_results


# --------------------------------------------------
# 9. COMPARE SELECTED CANDIDATES
# --------------------------------------------------

def compare_candidates(candidates, job, candidate_ids):
    """
    Compare selected candidates against the same job.

    Args:
        candidates: Candidate DataFrame.
        job: Selected job dictionary.
        candidate_ids: List of candidate IDs.

    Returns:
        List of candidate evaluation results.
    """

    comparison_results = []

    selected_candidates = candidates[
        candidates["candidate_id"].isin(candidate_ids)
    ]

    for _, candidate in selected_candidates.iterrows():

        result = calculate_candidate_suitability(
            candidate.to_dict(),
            job
        )

        comparison_results.append(result)

    # Sort by overall suitability
    comparison_results.sort(
        key=lambda x: x["overall_score"],
        reverse=True
    )

    return comparison_results
