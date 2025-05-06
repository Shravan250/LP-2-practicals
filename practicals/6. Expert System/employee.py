import pandas as pd

# Load dataset
df = pd.read_csv("Extended_Employee_Performance_and_Productivity_Data.csv")
df.head()

# Basic info (non-null values, datatypes)
print(df.info())

# Total missing values per column
print(df.isnull().sum())

# Statistical summary of numerical columns
df.describe()

# Fill missing satisfaction scores with the mean
df['Employee_Satisfaction_Score'] = df['Employee_Satisfaction_Score'].fillna(
    df['Employee_Satisfaction_Score'].mean()
)

# Convert and encode categorical columns
df['Department'] = df['Department'].astype('category')
df['Department_encoded'] = df['Department'].cat.codes
print(df[['Department', 'Department_encoded']])

def evaluate_performance(training_hours, kpi_met, awards_won):
    if training_hours > 20 and kpi_met > 80:
        return 'Excellent'
    elif kpi_met > 60:
        return 'Good'
    else:
        return 'Needs Improvement'

def is_eligible_for_promotion(performance_rating, previous_year_rating):
    if performance_rating == 'Excellent' and previous_year_rating >= 80:
        return 'Eligible'
    else:
        return 'Not Eligible'

def needs_training(training_hours):
    if training_hours < 10:
        return 'Yes'
    else:
        return 'No'

def calculate_salary(monthly_salary, performance_rating):
    if performance_rating == 'Excellent':
        return monthly_salary * 1.20  # 20% increment for excellent performance
    elif performance_rating == 'Good':
        return monthly_salary * 1.10  # 10% increment for good performance
    else:
        return monthly_salary  # No increment for needs improvement

# Apply the logic using the DataFrame columns
df['performance_rating'] = df.apply(
    lambda row: evaluate_performance(
        row['Training_Hours'],
        row['Performance_Score'],
        row['Promotions']
    ),
    axis=1
)

df['promotion_eligibility'] = df.apply(
    lambda row: is_eligible_for_promotion(
        row['performance_rating'],
        row['Employee_Satisfaction_Score']
    ),
    axis=1
)

df['needs_training'] = df['Training_Hours'].apply(needs_training)

df['new_salary'] = df.apply(
    lambda row: calculate_salary(
        row['Monthly_Salary'],
        row['performance_rating']
    ),
    axis=1
)

# Check the updated DataFrame
print(
    df[
        [
            'Employee_ID',
            'performance_rating',
            'promotion_eligibility',
            'needs_training',
            'new_salary'
        ]
    ].head()
)
