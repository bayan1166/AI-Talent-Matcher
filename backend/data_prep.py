import pandas as pd

employee_data_path = 'data/Employee Sample Data.csv'
resume_data_path = 'data/resume_data.csv'

try:
    employees_df = pd.read_csv(employee_data_path)
    resumes_df = pd.read_csv(resume_data_path)

    print("Data loaded successfully!\n")
    
    print("--- Employee Data ---")
    print(f"Shape: {employees_df.shape}")
    print(employees_df.columns.tolist())
    print("\n")

    print("--- Resume Data ---")
    print(f"Shape: {resumes_df.shape}")
    print(resumes_df.columns.tolist())

except Exception as e:
    print(f"Error: {e}")