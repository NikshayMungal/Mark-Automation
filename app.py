import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mark Automation Portal", page_icon="🎓")

st.title("🎓 Academic Mark Automation & Audit Portal")
st.write("Upload your class mark sheet below to automatically verify student IDs, check for out-of-range grades, and generate clean reports.")

# File uploader widget for teachers
uploaded_file = st.file_uploader("Upload Mark Sheet (Excel or CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Load the file based on its type
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.subheader("📋 Uploaded Data Preview")
    st.dataframe(df.head())

    # Audit checks
    missing_ids = df[df['Student_ID'].isnull()]
    invalid_marks = df[(df['Final_Mark'] < 0) | (df['Final_Mark'] > 100)]

    if not missing_ids.empty:
        st.error(f"[ALERT] Found {len(missing_ids)} rows with missing Student IDs.")
    if not invalid_marks.empty:
        st.error(f"[ALERT] Found {len(invalid_marks)} out-of-range marks (must be between 0 and 100).")

    # Clean the data
    clean_df = df.dropna(subset=['Student_ID']).copy()
    clean_df = clean_df[(clean_df['Final_Mark'] >= 0) & (clean_df['Final_Mark'] <= 100)]

    if 'Student_Name' in clean_df.columns:
        clean_df['Student_Name'] = clean_df['Student_Name'].str.strip()

    st.success(f"✅ Audit Complete! {len(clean_df)} valid records processed successfully.")

    # Convert clean dataframe to CSV for easy downloading
    csv_data = clean_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Cleaned Mark Sheet",
        data=csv_data,
        file_name="clean_marks_output.csv",
        mime="text/csv"
    )