import os
import pytest
import PyPDF2

# Define the non-compliance list globally so we can use it in our tests
non_compliance_list = []

# Path to the files
pdf_path = 'PolicyDocument.pdf'
risk_treatment_plan_path = 'Risk_Treatment_Plan.csv'
log_file_path = 'system.log'
report_file = 'test_report.txt'

# Function to write to the report file
def write_to_report(content):
    with open(report_file, 'a') as f:
        f.write(content)

# Function to parse the PDF and extract text
def parse_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text().lower()  # Ensure text is in lowercase
        return text
    except Exception as e:
        return ""  # Return an empty string if the file is unreadable

# Session-scoped fixture to initialize the report only once
@pytest.fixture(scope='session', autouse=True)
def setup_report():
    global non_compliance_list
    non_compliance_list.clear()  # Clear the non-compliance list at the start
    # Initialize the report
    with open(report_file, 'w') as f:
        f.write("This document exists as a report where you can see which guidelines you haven't implemented yet in the project. At the end of the list, you will be able to see which non-compliances you still have.\n")
    yield  # Allow tests to run
    # Write the non-compliance list at the end of the session
    with open(report_file, 'a') as f:
        f.write("\nNon-Compliance List:\n")
        for item in non_compliance_list:
            f.write(f"- {item}\n")

# Test: Check content of the policy document PDF
def test_pdf_content():
    global non_compliance_list
    if os.path.exists(pdf_path):
        pdf_text = parse_pdf(pdf_path)
        write_to_report("    5.1.A. Policy document exists\n")

        if 'organization specific' in pdf_text:
            write_to_report("    5.2.A. Policy document is tailored\n")
        else:
            write_to_report("[!] 5.2.A. Policy document is not tailored\n")
            non_compliance_list.append('5.2.A')

        if 'security objectives' in pdf_text:
            write_to_report("    5.2.B. Security Objectives documented\n")
        else:
            write_to_report("[!] 5.2.B. Security Objectives not documented\n")
            non_compliance_list.append('5.2.B')

        if 'commitment to compliance' in pdf_text:
            write_to_report("    5.2.C. Policy document contains Commitment to compliance\n")
        else:
            write_to_report("[!] 5.2.C. Policy document does not contain Commitment to compliance\n")
            non_compliance_list.append('5.2.C')
    else:
        write_to_report("[!] 5.1.A. Policy document missing\n")
        non_compliance_list.append('5.1.A')

# Test: Check content of the log file
def test_log_file_check():
    global non_compliance_list
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, 'r') as log_file:
                log_data = log_file.read().lower()
                if 'policy document' in log_data:
                    write_to_report("    5.2.F. Policy document communication confirmed\n")
                else:
                    write_to_report("[!] 5.2.F. Policy document communication not confirmed\n")
                    non_compliance_list.append('5.2.F')
        except Exception as e:
            write_to_report("[!] 5.2.F. Error reading log file\n")
            non_compliance_list.append('5.2.F')
    else:
        write_to_report("[!] 5.2.F. Log file missing\n")
        non_compliance_list.append('5.2.F')

# Test: Check if the risk treatment plan exists
def test_risk_treatment_plan():
    global non_compliance_list
    if os.path.exists(risk_treatment_plan_path):
        write_to_report("    8.1.A. Risk Treatment Plan exists\n")
    else:
        write_to_report("[!] 8.1.A. Risk Treatment Plan is missing!\n")
        non_compliance_list.append('8.1.A')

# To run the tests, execute this script with pytest:
# pytest test.py
