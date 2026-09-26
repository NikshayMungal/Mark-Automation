import io
import pandas as pd
import streamlit as st
from mark_automation import audit_marks

# Page Configuration
st.set_page_config(
    page_title="Academic Mark Automation & Audit Portal", page_icon="🎓", layout="centered"
)

# App Header
st.title("🎓 Academic Mark Automation & Audit Portal")
st.write(
    "Upload your class mark sheet below to automatically verify student IDs, check for out-of-range grades, and generate clean reports."
)

# File Uploader
uploaded_file = st.file_uploader(
    "Upload Mark Sheet (Excel or CSV)", type=["xlsx", "csv"]
)

if uploaded_file is not None:
  try:
    # Read the file based on extension
    if uploaded_file.name.endswith(".csv"):
      input_df = pd.read_csv(uploaded_file)
    else:
      input_df = pd.read_excel(uploaded_file)

    st.subheader("📋 Uploaded Data Preview")
    st.dataframe(input_df.head())

    # Run the audit automation logic
    clean_df, missing_ids_df, out_of_range_df = audit_marks(input_df)

    # Display Alerts and Summaries
    has_errors = False

    if not missing_ids_df.empty:
      has_errors = True
      st.error(
          f"[ALERT] Found {len(missing_ids_df)} rows with missing Student IDs."
      )
      with st.expander("View Missing ID Exceptions"):
        st.dataframe(missing_ids_df)

    if not out_of_range_df.empty:
      has_errors = True
      st.error(
          f"[ALERT] Found {len(out_of_range_df)} out-of-range marks (must be between 0 and 100)."
      )
      with st.expander("View Out-of-Range Grade Exceptions"):
        st.dataframe(out_of_range_df)

    if not has_errors:
      st.success(
          "🎉 Audit Complete! All records are valid and fully compliant."
      )
    else:
      st.success(
          f"✅ Audit Complete! {len(clean_df)} valid records processed successfully."
      )

    st.markdown("---")
    st.subheader("📥 Download Audit Results")

    # Helper function to convert dataframe to Excel bytes for proper formatting
    def convert_df_to_excel(df):
      output = io.BytesIO()
      with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Report")
      return output.getvalue()

    col1, col2 = st.columns(2)

    with col1:
      # Clean Marks Download Button (Excel)
      clean_excel = convert_df_to_excel(clean_df)
      st.download_button(
          label="Download Clean Marks (.xlsx)",
          data=clean_excel,
          file_name="clean_marks_output.xlsx",
          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      )

    with col2:
      if has_errors:
        # Combine exceptions into a single report dataframe
        exceptions_df = pd.concat([missing_ids_df, out_of_range_df]).drop_duplicates()
        exceptions_excel = convert_df_to_excel(exceptions_df)

        st.download_button(
            label="Download Exception Report (.xlsx)",
            data=exceptions_excel,
            file_name="exception_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

  except Exception as e:
    st.error(
        f"An error occurred while processing your file: {e}. Please ensure your columns match: Student_ID, Student_Name, Final_Mark."
    )

  except Exception as e:
    st.error(
        f"An error occurred while processing your file: {e}. Please ensure your"
        " columns match: Student_ID, Student_Name, Final_Mark."
    )
