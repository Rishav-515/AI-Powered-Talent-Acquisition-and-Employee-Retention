
"""
Synthetic Recruitment Dataset Generator
Project: AI-Powered Talent Acquisition and Employee Retention Analytics

Generates:
    data/raw/candidates.csv  - 50 synthetic candidate profiles
    data/raw/jobs.csv        - 5 technical job descriptions

All records are fictional and generated for project demonstration.
"""

import csv
import random
from pathlib import Path

# --------------------------------------------------
# 1. PROJECT PATHS AND RANDOM SEED
# --------------------------------------------------

random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. TECHNICAL ROLE PROFILES
# --------------------------------------------------

role_profiles = {
    "Python Developer": {
        "skills": [
            "Python", "SQL", "Flask", "Django",
            "REST API", "Git", "OOP", "PostgreSQL"
        ],
        "projects": [
            "Inventory Management API",
            "Online Quiz Application",
            "Student Management System",
            "Task Tracking Application"
        ],
        "domain": "Backend Development"
    },

    "Backend Developer": {
        "skills": [
            "Python", "Java", "SQL", "REST API",
            "Flask", "Django", "PostgreSQL",
            "MySQL", "Docker", "Git"
        ],
        "projects": [
            "Employee Management API",
            "E-Commerce Backend",
            "Authentication Service",
            "Booking Management System"
        ],
        "domain": "Backend Development"
    },

    "Data Analyst": {
        "skills": [
            "Python", "SQL", "Excel", "Power BI",
            "Pandas", "NumPy", "Matplotlib",
            "Statistics", "Tableau"
        ],
        "projects": [
            "Sales Data Analysis",
            "Customer Behaviour Analysis",
            "Financial Dashboard",
            "Business Intelligence Report"
        ],
        "domain": "Data Analytics"
    },

    "Machine Learning Engineer": {
        "skills": [
            "Python", "Machine Learning", "Scikit-learn",
            "TensorFlow", "Pandas", "NumPy",
            "Deep Learning", "Statistics", "SQL"
        ],
        "projects": [
            "Customer Churn Prediction",
            "Image Classification System",
            "House Price Prediction",
            "Recommendation System"
        ],
        "domain": "Machine Learning"
    },

    "Full Stack Developer": {
        "skills": [
            "Python", "JavaScript", "HTML", "CSS",
            "React", "Flask", "REST API",
            "SQL", "Git", "Bootstrap"
        ],
        "projects": [
            "Job Portal Application",
            "E-Commerce Web Application",
            "Online Learning Platform",
            "Project Management Dashboard"
        ],
        "domain": "Full Stack Development"
    }
}

# --------------------------------------------------
# 3. CANDIDATE PROFILE OPTIONS
# --------------------------------------------------

first_names = [
    "Aarav", "Aditya", "Arjun", "Ishaan", "Karan",
    "Rahul", "Rohan", "Siddharth", "Vihaan", "Kabir",
    "Ananya", "Diya", "Isha", "Meera", "Neha",
    "Priya", "Riya", "Sanya", "Tanya", "Aditi"
]

last_names = [
    "Sharma", "Verma", "Patel", "Reddy", "Gupta",
    "Mehta", "Nair", "Rao", "Kapoor", "Singh",
    "Iyer", "Das", "Malhotra", "Joshi", "Kumar"
]

education_options = [
    ("Bachelor's", "B.Tech", "Computer Science"),
    ("Bachelor's", "B.Tech", "Information Technology"),
    ("Bachelor's", "B.Tech", "Artificial Intelligence"),
    ("Bachelor's", "B.Tech", "Electronics and Communication"),
    ("Bachelor's", "BCA", "Computer Applications"),
    ("Bachelor's", "B.Sc", "Data Science"),
    ("Master's", "MCA", "Computer Applications"),
    ("Master's", "M.Tech", "Computer Science"),
    ("Master's", "M.Sc", "Data Science")
]

experience_options = [0, 0, 1, 1, 2, 2, 3, 4, 5]

certification_options = [
    "",
    "AWS Cloud Practitioner",
    "Microsoft Azure Fundamentals",
    "Python Programming Certification",
    "SQL Certification",
    "Machine Learning Certification",
    "Google Data Analytics Certificate"
]

# --------------------------------------------------
# 4. GENERATE 50 SYNTHETIC CANDIDATES
# --------------------------------------------------

candidates = []

names = [
    f"{first} {last}"
    for first in first_names
    for last in last_names
]

random.shuffle(names)

candidate_number = 1

for role, profile in role_profiles.items():

    # Generate 10 candidates for each technical role
    for _ in range(10):

        experience = random.choice(experience_options)

        education_level, degree, specialization = random.choice(
            education_options
        )

        # Start with skills relevant to the candidate's preferred role
        candidate_skills = profile["skills"].copy()

        # Add some variation to candidate skill sets
        random.shuffle(candidate_skills)

        skill_count = random.randint(4, len(candidate_skills))
        selected_skills = candidate_skills[:skill_count]

        # Add occasional transferable technical skills
        extra_skills = [
            "Linux", "Docker", "Git", "Java",
            "C", "C++", "Communication"
        ]

        if random.random() < 0.6:
            extra_skill = random.choice(extra_skills)

            if extra_skill not in selected_skills:
                selected_skills.append(extra_skill)

        certification = random.choice(certification_options)

        project_count = random.randint(1, 3)

        selected_projects = random.sample(
            profile["projects"],
            k=min(project_count, len(profile["projects"]))
        )

        graduation_year = 2026 - min(experience + 1, 6)

        candidate = {
            "candidate_id": f"CAND{candidate_number:03d}",
            "candidate_name": names[candidate_number - 1],
            "education_level": education_level,
            "degree": degree,
            "specialization": specialization,
            "graduation_year": graduation_year,
            "experience_years": experience,
            "skills": "; ".join(selected_skills),
            "certifications": certification,
            "projects": "; ".join(selected_projects),
            "project_domains": profile["domain"],
            "preferred_role": role
        }

        candidates.append(candidate)
        candidate_number += 1

# --------------------------------------------------
# 5. DEFINE FIVE TECHNICAL JOB DESCRIPTIONS
# --------------------------------------------------

jobs = [
    {
        "job_id": "JOB001",
        "job_title": "Python Developer",
        "department": "Engineering",
        "minimum_education": "Bachelor's",
        "required_specialization": "Computer Science; Information Technology; Computer Applications",
        "minimum_experience": 0,
        "required_skills": "Python; SQL; OOP; Git",
        "preferred_skills": "Flask; Django; REST API; PostgreSQL",
        "required_certifications": "",
        "job_description": (
            "Develop and maintain Python applications, "
            "write database queries, build APIs, and "
            "collaborate with the engineering team."
        )
    },
    {
        "job_id": "JOB002",
        "job_title": "Backend Developer",
        "department": "Engineering",
        "minimum_education": "Bachelor's",
        "required_specialization": "Computer Science; Information Technology; Computer Applications",
        "minimum_experience": 1,
        "required_skills": "Python; SQL; REST API; Git",
        "preferred_skills": "Flask; Django; PostgreSQL; Docker; MySQL",
        "required_certifications": "",
        "job_description": (
            "Design and implement backend services, "
            "develop REST APIs, integrate databases, "
            "and maintain application performance."
        )
    },
    {
        "job_id": "JOB003",
        "job_title": "Data Analyst",
        "department": "Analytics",
        "minimum_education": "Bachelor's",
        "required_specialization": "Computer Science; Information Technology; Data Science; Computer Applications",
        "minimum_experience": 0,
        "required_skills": "Python; SQL; Excel; Statistics",
        "preferred_skills": "Pandas; NumPy; Power BI; Tableau; Matplotlib",
        "required_certifications": "",
        "job_description": (
            "Analyze structured datasets, prepare reports, "
            "identify business trends, and create "
            "data visualizations to support decisions."
        )
    },
    {
        "job_id": "JOB004",
        "job_title": "Machine Learning Engineer",
        "department": "AI and Data Science",
        "minimum_education": "Bachelor's",
        "required_specialization": "Computer Science; Information Technology; Data Science; Artificial Intelligence",
        "minimum_experience": 2,
        "required_skills": "Python; Machine Learning; Scikit-learn; Statistics",
        "preferred_skills": "TensorFlow; Deep Learning; Pandas; NumPy; SQL",
        "required_certifications": "",
        "job_description": (
            "Develop, evaluate, and deploy machine learning "
            "models, prepare datasets, and collaborate "
            "on AI-driven applications."
        )
    },
    {
        "job_id": "JOB005",
        "job_title": "Full Stack Developer",
        "department": "Product Engineering",
        "minimum_education": "Bachelor's",
        "required_specialization": "Computer Science; Information Technology; Computer Applications",
        "minimum_experience": 1,
        "required_skills": "JavaScript; HTML; CSS; SQL; REST API",
        "preferred_skills": "React; Python; Flask; Bootstrap; Git",
        "required_certifications": "",
        "job_description": (
            "Build and maintain frontend and backend "
            "application components, integrate APIs, "
            "and develop responsive web applications."
        )
    }
]

# --------------------------------------------------
# 6. SAVE DATASETS AS CSV FILES
# --------------------------------------------------

candidate_file = RAW_DATA_DIR / "candidates.csv"
job_file = RAW_DATA_DIR / "jobs.csv"

with open(candidate_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=candidates[0].keys()
    )

    writer.writeheader()
    writer.writerows(candidates)

with open(job_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=jobs[0].keys()
    )

    writer.writeheader()
    writer.writerows(jobs)

# --------------------------------------------------
# 7. DISPLAY GENERATION SUMMARY
# --------------------------------------------------

print("=" * 55)
print("SYNTHETIC RECRUITMENT DATASETS GENERATED")
print("=" * 55)

print(f"\nCandidate records: {len(candidates)}")
print(f"Job descriptions  : {len(jobs)}")

freshers = sum(
    1 for candidate in candidates
    if candidate["experience_years"] == 0
)

experienced = len(candidates) - freshers

print(f"\nFreshers          : {freshers}")
print(f"Experienced       : {experienced}")

print("\nCandidate distribution by preferred role:")

for role in role_profiles:
    count = sum(
        1 for candidate in candidates
        if candidate["preferred_role"] == role
    )
    print(f"{role}: {count}")

print("\nGenerated files:")
print(candidate_file)
print(job_file)

print("\nDataset generation completed successfully.")
