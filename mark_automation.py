import pandas as pd


def audit_marks(df):
  # Create a copy to avoid modifying the original dataframe
  df = df.copy()

  # Ensure column names match expected format by stripping whitespace
  df.columns = df.columns.str.strip()

  # 1. Identify missing Student IDs
  missing_ids_df = df[df["Student_ID"].isna() | (df["Student_ID"] == "")]

  # 2. Identify out-of-range marks
  numeric_marks = pd.to_numeric(df["Final_Mark"], errors="coerce")
  out_of_range_mask = (
      numeric_marks.isna() | (numeric_marks < 0) | (numeric_marks > 100)
  )
  out_of_range_df = df[out_of_range_mask]

  # 3. Clean records
  invalid_indices = set(missing_ids_df.index).union(set(out_of_range_df.index))
  clean_df = df.drop(index=list(invalid_indices))

  return clean_df, missing_ids_df, out_of_range_df
    audit_mark_sheet('sample_marks.xlsx')
