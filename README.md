# 🎓 Academic Mark Automation & Audit Portal

A web-based academic administration tool built with **Python**, **Pandas**, and **Streamlit** to automate the auditing and cleaning of student mark sheets.

---

## ✨ Features
* **Automated Data Validation**: Instantly scans uploaded Excel or CSV mark sheets for compliance.
* **Error Detection**: 
  * Flags missing or `None` Student IDs.
  * Detects out-of-range marks (grades falling outside the $0$ to $100$ scale).
* **Cleaned Output Generation**: Filters out faulty entries and provides a clean, submission-ready file.
* **Exception Reporting**: Separates invalid records into a dedicated review report for manual verification.

---

## 🛠️ Tech Stack
* **Frontend/UI**: Streamlit
* **Data Processing**: Pandas, Openpyxl
* **Hosting**: Streamlit Community Cloud & GitHub

---

## 🚀 Local Installation & Setup

If you want to run this application locally on your machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/nikshaymungal/Mark-Automation.git](https://github.com/nikshaymungal/Mark-Automation.git)
   cd Mark-Automation
