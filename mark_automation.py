import pandas as pd

def audit_mark_sheet(file_path):
    print(f"--- Starting audit for: {file_path} ---")
    
    # 1. Load the spreadsheet (supports Excel or CSV)
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # 2. Check for missing Student IDs
    missing_ids = df[df['Student_ID'].isnull()]
    if not missing_ids.empty:
        print(f"[ALERT] Found {len(missing_ids)} rows with missing Student IDs.")

    # 3. Check for invalid marks (must be between 0 and 100)
    invalid_marks = df[(df['Final_Mark'] < 0) | (df['Final_Mark'] > 100)]
    if not invalid_marks.empty:
        print(f"[ALERT] Found {len(invalid_marks)} out-of-range marks (must be between 0-100).")

    # 4. Clean data: strip any whitespace from string columns
    if 'Student_Name' in df.columns:
        df['Student_Name'] = df['Student_Name'].str.strip()

    # 5. Generate Output Reports
    clean_df = df.dropna(subset=['Student_ID']).copy()
    clean_df = clean_df[(clean_df['Final_Mark'] >= 0) & (clean_df['Final_Mark'] <= 100)]
    
    clean_output = "clean_marks_output.xlsx"
    error_output = "audit_exceptions_report.xlsx"
    
    clean_df.to_excel(clean_output, index=False)
    
    # Save exceptions/errors for human review
    exceptions_df = df[~df.index.isin(clean_df.index)]
    if not exceptions_df.empty:
        exceptions_df.to_excel(error_output, index=False)
        print(f"[ACTION REQUIRED] {len(exceptions_df)} exception rows exported to '{error_output}' for manual review.")
    else:
        print("[SUCCESS] No exceptions found. All records are clean.")

    print(f"--- Audit Complete. Clean file saved as '{clean_output}' ---")

# Run the function
if __name__ == "__main__":
    audit_mark_sheet('sample_marks.xlsx')