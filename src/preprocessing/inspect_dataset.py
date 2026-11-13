
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. Locate and load the dataset
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
)

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("EMPLOYEE ATTRITION DATASET - INITIAL INSPECTION")
print("=" * 60)

# --------------------------------------------------
# 2. Dataset dimensions
# --------------------------------------------------

print("\n1. DATASET DIMENSIONS")
print("-" * 40)

print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

# --------------------------------------------------
# 3. Column names
# --------------------------------------------------

print("\n2. COLUMN NAMES")
print("-" * 40)

for index, column in enumerate(df.columns, start=1):
    print(f"{index}. {column}")

# --------------------------------------------------
# 4. Data types
# --------------------------------------------------

print("\n3. DATA TYPES")
print("-" * 40)

print(df.dtypes.to_string())

# --------------------------------------------------
# 5. Missing values
# --------------------------------------------------

print("\n4. MISSING VALUES")
print("-" * 40)

missing = df.isnull().sum()

missing_report = pd.DataFrame({
    "Missing Count": missing,
    "Missing Percentage": (
        missing / len(df) * 100
    ).round(2)
})

print(missing_report[missing_report["Missing Count"] > 0])

if missing.sum() == 0:
    print("No missing values found.")

# --------------------------------------------------
# 6. Duplicate records
# --------------------------------------------------

print("\n5. DUPLICATE RECORDS")
print("-" * 40)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count}")

# --------------------------------------------------
# 7. Target variable distribution
# --------------------------------------------------

print("\n6. TARGET VARIABLE DISTRIBUTION")
print("-" * 40)

if "Attrition" in df.columns:

    print(df["Attrition"].value_counts())

    print("\nPercentage distribution:")

    print(
        (df["Attrition"].value_counts(normalize=True) * 100)
        .round(2)
    )

else:
    print("Target column 'Attrition' was not found.")

# --------------------------------------------------
# 8. Unique values in each column
# --------------------------------------------------

print("\n7. UNIQUE VALUES PER COLUMN")
print("-" * 40)

print(df.nunique().to_string())

# --------------------------------------------------
# 9. Statistical summary
# --------------------------------------------------

print("\n8. STATISTICAL SUMMARY")
print("-" * 40)

print(df.describe(include="all").T.to_string())

# --------------------------------------------------
# 10. Sample records
# --------------------------------------------------

print("\n9. FIRST FIVE RECORDS")
print("-" * 40)

print(df.head().to_string(index=False))

print("\n" + "=" * 60)
print("INITIAL DATASET INSPECTION COMPLETED")
print("=" * 60)
