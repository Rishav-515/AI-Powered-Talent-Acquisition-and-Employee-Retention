# Employee Attrition Dataset Documentation

## 1. Dataset Information

- Dataset: IBM HR Analytics Employee Attrition & Performance
- File: `WA_Fn-UseC_-HR-Employee-Attrition.csv`
- Records: 1,470
- Columns: 35
- Format: CSV
- Target variable: `Attrition`

## 2. Target Variable

The target variable is `Attrition`.

- `Yes`: Employee left the organization.
- `No`: Employee remained with the organization.

Observed distribution:

| Class | Records | Percentage |
|---|---:|---:|
| No | 1,233 | 83.88% |
| Yes | 237 | 16.12% |

The dataset exhibits class imbalance.

## 3. Data Quality Assessment

| Check | Result |
|---|---|
| Missing values | 0 |
| Duplicate records | 0 |
| Total records | 1,470 |
| Total columns | 35 |

## 4. Columns Requiring Special Treatment

- `EmployeeCount`: Constant feature.
- `Over18`: Constant feature.
- `StandardHours`: Constant feature.
- `EmployeeNumber`: Unique employee identifier.

These four columns will be excluded from model training.

The original CSV will remain unchanged.

## 5. Feature Categories

- Demographics
- Job information
- Compensation
- Employee satisfaction
- Work conditions
- Work experience
- Career progression
- Training and performance

## 6. Modeling Considerations

- Handle categorical features through appropriate encoding.
- Evaluate the need for numerical feature scaling based on the selected model.
- Use stratified train-test splitting.
- Evaluate class-specific performance, particularly attrition recall.
- Compare models using accuracy, precision, recall, F1-score, confusion matrix and ROC-AUC.
- Consider Precision-Recall AUC due to class imbalance.

## 7. Dataset Limitations

The dataset contains fictional employee records. Model performance on this dataset should not be interpreted as validated performance on real-world organizational HR data.

## 8. Exploratory Data Analysis – Age Group

Employees were divided into five age groups to examine
attrition patterns.

| Age Group | Employees Who Left | Attrition Rate |
|---|---:|---:|
| 18-25 | 44 | 35.77% |
| 26-35 | 116 | 19.14% |
| 36-45 | 43 | 9.19% |
| 46-55 | 26 | 11.50% |
| 56-60 | 8 | 17.02% |

### Key Observations
- The 18-25 age group has the highest attrition rate.
- The 26-35 age group has the highest number of departures.
- The 36-45 age group has the lowest attrition rate.
- Attrition rates vary across age groups.

These observations indicate associations within the dataset
and should not be interpreted as causal relationships.

## 9. Exploratory Data Analysis – Gender

| Gender | Employees Who Left | Attrition Rate |
|---|---:|---:|
| Female | 87 | 14.80% |
| Male | 150 | 17.01% |

### Key Observations
- Male employees have a slightly higher attrition rate.
- The difference between the two groups is approximately 2.21 percentage points.
- These findings represent associations in the dataset and do not establish causation.

## 10. Exploratory Data Analysis – Department

| Department | Employees Who Left | Attrition Rate |
|---|---:|---:|
| Research & Development | 133 | 13.84% |
| Human Resources | 12 | 19.05% |
| Sales | 92 | 20.63% |

### Key Observations
- Sales has the highest attrition rate.
- Human Resources has the second-highest attrition rate.
- Research & Development has the lowest attrition rate.
- Research & Development has the highest number of departures.
- Department sizes should be considered when interpreting these percentages.

## 11. Exploratory Data Analysis – Job Role

| Job Role | Employees Who Left | Attrition Rate |
|---|---:|---:|
| Sales Representative | 33 | 39.76% |
| Laboratory Technician | 62 | 23.94% |
| Human Resources | 12 | 23.08% |
| Sales Executive | 57 | 17.48% |
| Research Scientist | 47 | 16.10% |
| Healthcare Representative | 9 | 6.87% |
| Manufacturing Director | 10 | 6.90% |
| Manager | 5 | 4.90% |
| Research Director | 2 | 2.50% |

### Key Observations
- Sales Representatives have the highest attrition rate.
- Laboratory Technicians have the highest number of departures.
- Research Directors have the lowest attrition rate.
- Attrition patterns vary across job roles.
- Both group size and attrition percentage should be considered.

## 12. Exploratory Data Analysis – Overtime

| Overtime | Employees Who Left | Attrition Rate |
|---|---:|---:|
| No | 110 | 10.44% |
| Yes | 127 | 30.53% |

### Key Observations
- Employees working overtime have a higher attrition rate.
- The difference between the groups is 20.09 percentage points.
- The attrition rate among employees working overtime is approximately 2.92 times higher.
- Overtime is a potentially important predictive feature.

These findings represent associations and do not establish causation.

## 13. Exploratory Data Analysis – Monthly Income

Employees were divided into four income quartiles.

| Income Group | Employees Who Left | Attrition Rate |
|---|---:|---:|
| Low | 108 | 29.27% |
| Lower-Middle | 52 | 14.21% |
| Upper-Middle | 39 | 10.63% |
| High | 38 | 10.33% |

### Key Observations
- The Low income group has the highest attrition rate.
- Attrition decreases across the income groups.
- The High income group has the lowest attrition rate.
- Monthly income may be an important predictive feature.

These findings represent associations and do not establish causation.

## 14. Exploratory Data Analysis – Job Satisfaction

| Satisfaction Level | Meaning | Attrition Rate |
|---:|---|---:|
| 1 | Low | 22.84% |
| 2 | Medium | 16.43% |
| 3 | High | 16.52% |
| 4 | Very High | 11.33% |

### Key Observations
- Low job satisfaction has the highest attrition rate.
- Very high job satisfaction has the lowest attrition rate.
- Satisfaction levels 2 and 3 show similar attrition rates.
- Lower job satisfaction is associated with higher attrition in this dataset.

These findings represent associations and do not establish causation.

## 15. Exploratory Data Analysis – Work-Life Balance

| Work-Life Balance | Meaning | Attrition Rate |
|---:|---|---:|
| 1 | Bad | 31.25% |
| 2 | Good | 16.86% |
| 3 | Better | 14.22% |
| 4 | Best | 17.65% |

### Key Observations
- Bad work-life balance has the highest attrition rate.
- Better work-life balance has the lowest attrition rate.
- The attrition rate increases slightly at level 4.
- The relationship is not perfectly linear.

These findings represent associations and do not establish causation.

## 16. Exploratory Data Analysis – Correlation Analysis

Pearson correlation analysis was performed to examine the linear relationships between numerical features and employee attrition.

Attrition was encoded as a binary variable:
- No = 0
- Yes = 1

### Features with Negative Correlation

| Feature | Correlation |
|---|---:|
| TotalWorkingYears | -0.1711 |
| JobLevel | -0.1691 |
| YearsInCurrentRole | -0.1605 |
| MonthlyIncome | -0.1598 |
| Age | -0.1592 |
| YearsWithCurrManager | -0.1562 |
| StockOptionLevel | -0.1371 |
| YearsAtCompany | -0.1344 |
| JobInvolvement | -0.1300 |
| JobSatisfaction | -0.1035 |

### Features with Positive Correlation

| Feature | Correlation |
|---|---:|
| DistanceFromHome | 0.0779 |
| NumCompaniesWorked | 0.0435 |
| MonthlyRate | 0.0152 |
| PerformanceRating | 0.0029 |

### Key Observations

- TotalWorkingYears has the strongest negative correlation with attrition among the numerical features.
- JobLevel, MonthlyIncome, and work experience variables also show negative correlations.
- DistanceFromHome has the strongest positive correlation, although the relationship is weak.
- No numerical feature demonstrates a strong individual linear correlation with attrition.
- Correlation does not establish causation.

Constant columns and the EmployeeNumber identifier were excluded from the correlation analysis.

The correlation heatmap is saved as `reports/figures/10_correlation_heatmap.png`.