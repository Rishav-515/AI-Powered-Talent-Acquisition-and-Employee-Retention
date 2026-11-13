
# Recruitment Matching Engine

## 1. Overview

The Recruitment Matching Engine is a rule-based candidate evaluation and ranking component of the AI-Powered Talent Acquisition and Employee Retention Predictive Analytics for Workplace Sustainability project.

Its purpose is to evaluate candidate profiles against technical job requirements and generate suitability scores to assist recruiters in identifying potentially suitable candidates.

The engine evaluates candidates using their:
- Technical skills
- Professional experience
- Educational qualifications
- Certifications
- Project experience and relevance

It generates an overall suitability score, identifies candidate strengths and gaps, and ranks candidates for individual job positions.

The system is designed as a decision-support tool. It does not automatically select or reject candidates.

## 2. Objectives

The main objectives of the recruitment matching engine are:

1. Evaluate candidate profiles against job-specific requirements.
2. Measure the alignment between candidate skills and required skills.
3. Assess experience and educational qualification suitability.
4. Evaluate mandatory and preferred certifications.
5. Identify relevant academic and personal project experience.
6. Calculate an overall candidate suitability score.
7. Rank candidates based on their suitability for a particular job.
8. Provide transparent explanations of candidate strengths and gaps.
9. Support recruiters in comparing multiple candidates.

## 3. Technology Stack

The recruitment matching engine uses the following technologies:

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| Pandas | Candidate and job dataset processing |
| CSV | Dataset storage and ranking exports |
| Pathlib | Project path management |
| VS Code | Development environment |

No machine learning model is trained for recruitment matching. The engine uses predefined rules, comparisons, and manually assigned scoring weights.

## 4. Dataset Description

Two synthetic datasets were created for developing and testing the recruitment matching engine.

### 4.1 Candidate Dataset

File location: `data/raw/candidates.csv`

The dataset contains 50 synthetic candidate records.

Each candidate profile includes the following attributes:

| Attribute | Description |
|---|---|
| candidate_id | Unique candidate identifier |
| candidate_name | Candidate name |
| education_level | Highest educational qualification |
| degree | Academic degree |
| specialization | Academic specialization |
| graduation_year | Year of graduation |
| experience_years | Total professional experience |
| skills | Technical skills possessed by the candidate |
| certifications | Certifications obtained |
| projects | Candidate project descriptions |
| project_domains | Domains associated with candidate projects |
| preferred_role | Candidate's preferred technical role |

The dataset includes both freshers and experienced candidates with professional experience ranging from 0 to 5 years.

### 4.2 Job Dataset

File location: `data/raw/jobs.csv`

The dataset contains five synthetic technical job descriptions.

| Job ID | Job Title | Minimum Experience |
|---|---|---:|
| JOB001 | Python Developer | 0 years |
| JOB002 | Backend Developer | 1 year |
| JOB003 | Data Analyst | 0 years |
| JOB004 | Machine Learning Engineer | 2 years |
| JOB005 | Full Stack Developer | 1 year |

Each job record contains:

- Job title and department
- Minimum educational qualification
- Required academic specialization
- Minimum professional experience
- Required technical skills
- Preferred technical skills
- Mandatory certifications
- Preferred certifications
- Job description

### 4.3 Dataset Limitations

The candidate and job datasets are synthetically generated for project development and demonstration.

They do not represent actual job applicants or real organizational recruitment records.

The synthetic dataset also contains predefined relationships between candidate preferences, skills, and project domains. Consequently, the ranking results should not be interpreted as evidence of real-world recruitment effectiveness.

## 5. System Architecture

The recruitment matching engine follows a modular, rule-based architecture.

The processing workflow is:

1. Load candidate and job datasets.
2. Select a job position for evaluation.
3. Compare each candidate against the selected job.
4. Calculate individual component scores.
5. Calculate the overall suitability score.
6. Identify candidate strengths and gaps.
7. Evaluate minimum job requirements.
8. Generate a candidate review status.
9. Rank candidates in descending order of suitability.
10. Export ranking results into CSV files.

### Processing Flow

Candidate Dataset + Job Dataset<br>
↓<br>
Data Loading and Parsing<br>
↓<br>
Skill Matching<br>
↓<br>
Experience Matching<br>
↓<br>
Education Matching<br>
↓<br>
Certification Matching<br>
↓<br>
Project Relevance Evaluation<br>
↓<br>
Weighted Suitability Calculation<br>
↓<br>
Requirement and Review Status Evaluation<br>
↓<br>
Candidate Ranking and Comparison<br>
↓<br>
CSV Export

## 6. Candidate Suitability Scoring Methodology

The engine calculates candidate suitability using five evaluation components.

The overall score is calculated using the following weighted formula:

Overall Suitability Score =

(Skills Score × 0.50) +<br>
(Experience Score × 0.20) +<br>
(Education Score × 0.15) +<br>
(Certification Score × 0.10) +<br>
(Project Relevance Score × 0.05)

The maximum possible overall score is 100.

### 6.1 Scoring Weights

| Evaluation Component | Weight |
|---|---:|
| Skills Matching | 50% |
| Experience Matching | 20% |
| Education Matching | 15% |
| Certification Matching | 10% |
| Project Relevance | 5% |
| Total | 100% |

These weights are manually selected project heuristics. They have not been statistically trained or empirically calibrated against historical recruitment outcomes.

## 7. Individual Matching Components

### 7.1 Skills Matching

The skill matching component compares candidate skills with required and preferred job skills.

The skill score is divided into two parts:

- Required skills: 80%
- Preferred skills: 20%

Required Skill Score =

(Number of Matched Required Skills / Total Required Skills) × 100

Preferred Skill Score =

(Number of Matched Preferred Skills / Total Preferred Skills) × 100

Final Skill Score =

(Required Skill Score × 0.80) +<br>
(Preferred Skill Score × 0.20)

The engine identifies:

- Matched required skills
- Missing required skills
- Matched preferred skills
- Missing preferred skills

Skill comparison uses normalized, case-insensitive skill names.

### 7.2 Experience Matching

The experience matching component evaluates whether the candidate satisfies the minimum professional experience specified in the job description.

The experience score is determined using the difference between candidate experience and minimum required experience.

| Experience Gap | Score |
|---|---:|
| Meets or exceeds requirement | 100 |
| 1 year below requirement | 75 |
| 2 years below requirement | 50 |
| 3 years below requirement | 25 |
| 4 or more years below requirement | 0 |

The component also generates a Boolean indicator showing whether the candidate meets the minimum experience requirement.

### 7.3 Education Matching

The education matching component compares the candidate's educational qualification with the minimum qualification specified for the job.

The implemented qualification hierarchy is:

1. High School
2. Diploma
3. Bachelor's Degree
4. Master's Degree
5. PhD

The scoring rules are:

| Condition | Score |
|---|---:|
| Candidate does not meet minimum education level | 0 |
| Candidate meets education level and specialization | 100 |
| Candidate meets education level but specialization differs | 70 |

The component separately evaluates:

- Minimum education level
- Academic specialization relevance

This distinction allows the system to identify candidates who satisfy the minimum educational qualification but have a different academic specialization.

### 7.4 Certification Matching

The certification component evaluates mandatory and preferred certifications.

The implementation assigns:

- Mandatory certification matching: 70% of the certification component.
- Preferred certification matching: 30% of the certification component.

Mandatory Certification Score =

(Matched Mandatory Certifications / Total Mandatory Certifications) × 100

Preferred Certification Score =

(Matched Preferred Certifications / Total Preferred Certifications) × 100

When both categories are specified:

Certification Score =

(Mandatory Score × 0.70) +<br>
(Preferred Score × 0.30)

When only one category is specified, its score is used directly.

When neither category is specified, the certification score defaults to 100.

The engine identifies matched and missing mandatory and preferred certifications separately.

Preferred certifications influence the suitability score but are not treated as mandatory eligibility conditions.

### 7.5 Project Relevance

The project relevance component evaluates the relationship between a candidate's project experience and the selected job role.

The implementation uses project-domain matching and basic keyword comparison.

The scoring rules are:

| Project Relevance | Score |
|---|---:|
| Relevant project domain found | 100 |
| Job title keyword match | 75 |
| Candidate has projects but no strong relevance match | 50 |
| No project information available | 0 |

The component also provides a relevance category such as High, Moderate, Partial, or None.

This is a heuristic evaluation and does not involve semantic project analysis or a trained natural language processing model.

## 8. Candidate Suitability Output

The `calculate_candidate_suitability()` function combines the five component scores and produces the final evaluation result.

The output contains:

- Candidate ID and name
- Job ID and title
- Overall suitability score
- Individual component scores
- Detailed matching results
- Candidate strengths
- Candidate gaps
- Minimum experience requirement status
- Minimum education requirement status
- Mandatory certification requirement status
- Consolidated minimum requirement status
- Human-review status

The detailed output allows recruiters to understand why a candidate received a particular suitability score.

## 9. Candidate Ranking

The `rank_candidates()` function evaluates all candidates against a selected job position.

The ranking process:

1. Iterates through the candidate dataset.
2. Calculates each candidate's suitability score.
3. Sorts candidates in descending order of overall suitability.
4. Assigns a rank to each candidate.

Candidates with higher suitability scores appear earlier in the ranking.

The ranking is specific to the selected job. A candidate may receive different rankings for different technical positions.

## 10. Candidate Comparison

The `compare_candidates()` function evaluates a selected group of candidates against a particular job.

It provides a structured comparison using:

- Overall suitability score
- Skills score
- Experience score
- Education score
- Certification score
- Project relevance score
- Candidate strengths
- Candidate gaps

The selected candidates are sorted by their overall suitability scores.

This functionality allows recruiters to compare shortlisted candidates using consistent evaluation criteria.

## 11. Minimum Requirement Evaluation

The system evaluates whether candidates satisfy the minimum requirements of a job.

Three mandatory conditions are checked:

1. Minimum professional experience
2. Minimum educational qualification level
3. Mandatory certification requirements

The `meets_minimum_requirements` field combines these three conditions.

The system also generates a `review_status` field.

| Condition | Review Status |
|---|---|
| All minimum requirements satisfied | Meets minimum requirements |
| At least one minimum requirement not satisfied | Requires human review |

The review status is intended to highlight candidates who need additional assessment.

It is not an automatic rejection mechanism.

Academic specialization mismatch affects the education score but does not independently trigger the consolidated review status.

## 12. Ranking Export and Storage

The engine exports evaluation results into CSV files for further analysis and dashboard integration.

The export script is:

`src/recruitment/export_rankings.py`

The script generates:

### 12.1 Master Ranking File

`data/processed/candidate_job_rankings.csv`

Contains all candidate evaluations across all five job positions.

### 12.2 Job-Specific Ranking Files

- `JOB001_candidate_rankings.csv`
- `JOB002_candidate_rankings.csv`
- `JOB003_candidate_rankings.csv`
- `JOB004_candidate_rankings.csv`
- `JOB005_candidate_rankings.csv`

Each file contains the 50 candidates evaluated and ranked for its corresponding job.

### 12.3 Exported Information

The exported records include:

- Job and candidate identifiers
- Candidate names
- Candidate ranking
- Overall suitability score
- Individual component scores
- Matched and missing required certifications
- Matched and missing preferred certifications
- Missing required skills
- Minimum requirement indicators
- Review status
- Candidate strengths and gaps

## 13. Implementation Files

The recruitment engine implementation is organized as follows:

| File | Purpose |
|---|---|
| `src/recruitment/data_generator.py` | Generates synthetic candidate and job datasets |
| `src/recruitment/validate_datasets.py` | Validates candidate and job datasets |
| `src/recruitment/matching_engine.py` | Implements matching, scoring, ranking, and comparison |
| `src/recruitment/update_job_certifications.py` | Adds preferred certification requirements to jobs |
| `src/recruitment/test_candidate_ranking.py` | Tests candidate ranking |
| `src/recruitment/test_candidate_comparison.py` | Tests candidate comparison |
| `src/recruitment/test_certification_matching.py` | Tests certification matching |
| `src/recruitment/test_requirement_flags.py` | Tests minimum requirement indicators |
| `src/recruitment/test_review_status.py` | Tests consolidated review status |
| `src/recruitment/export_rankings.py` | Generates ranking CSV files |
| `tests/test_recruitment_engine.py` | Runs automated recruitment engine tests |

## 14. Testing and Validation

The recruitment matching engine was tested using the 50 synthetic candidate profiles and five synthetic job descriptions.

### 14.1 Dataset Validation

- Candidate records: 50
- Job records: 5
- Technical job roles: 5
- Candidate experience range: 0–5 years

### 14.2 Ranking Export Validation

| Validation | Result |
|---|---:|
| Total evaluation records | 250 |
| Expected evaluation records | 250 |
| Unique candidates | 50 |
| Unique jobs | 5 |
| Records per job | 50 |
| Duplicate candidate-job pairs | 0 |

### 14.3 Review Status Results

| Job Role | Meets Minimum Requirements | Requires Human Review |
|---|---:|---:|
| Python Developer | 50 | 0 |
| Backend Developer | 42 | 8 |
| Data Analyst | 50 | 0 |
| Machine Learning Engineer | 31 | 19 |
| Full Stack Developer | 42 | 8 |
| Total | 215 | 35 |

These values represent candidate-job evaluations, not unique candidates across all job roles.

### 14.4 Automated Testing

The following automated tests were implemented:

| Test | Result |
|---|---|
| Skill matching | PASS |
| Experience matching | PASS |
| Education matching | PASS |
| Certification matching | PASS |
| Project relevance | PASS |
| Candidate suitability calculation | PASS |
| Candidate ranking | PASS |
| Candidate comparison | PASS |

**Final automated testing result: 8 out of 8 tests passed.**

The automated tests verify the core matching functions, output structure, score ranges, and ranking order.

## 15. Limitations

The recruitment matching engine has the following limitations:

1. The candidate and job datasets are synthetic and do not represent real recruitment records.
2. The scoring weights are manually assigned and have not been validated against historical hiring outcomes.
3. Skill matching uses normalized string comparisons and does not understand semantic equivalence between different skill names.
4. Project relevance uses predefined domain mappings and basic keyword matching.
5. Certification matching depends on the certification names supplied in the datasets.
6. The scoring system does not evaluate soft skills, communication abilities, interview performance, or cultural fit.
7. The engine has not been evaluated using real-world recruitment data.
8. Suitability scores are not probabilities of successful recruitment or future job performance.

## 16. Responsible AI and Human Oversight

The recruitment matching engine is intended to assist human recruiters rather than replace their judgment.

The following safeguards are considered:

- Candidate rankings are advisory.
- The system does not automatically hire or reject candidates.
- Missing preferred skills or certifications should not be interpreted as automatic disqualification.
- Recruiters should review candidate profiles and supporting evidence before making decisions.
- The system's synthetic dataset and manually selected scoring weights must be disclosed.
- Candidate information should be handled securely and used only for appropriate recruitment purposes.

The final hiring decision must remain with authorized human decision-makers.

## 17. Conclusion

The Recruitment Matching Engine successfully implements a rule-based candidate evaluation and ranking system for five technical job roles.

It evaluates candidates using skills, experience, education, certifications, and project relevance. The engine calculates weighted suitability scores, identifies candidate strengths and gaps, checks minimum job requirements, compares selected candidates, and exports ranked results.

Testing with 50 synthetic candidates and five job descriptions produced 250 candidate-job evaluation records. All eight automated recruitment engine tests passed.

The completed implementation provides the recruitment component required for integration into the unified AI-powered HR analytics dashboard.
