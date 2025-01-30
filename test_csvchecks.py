import os
import csv
import pytest

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():

    report_file = 'csvchecks_report.txt'
    with open(report_file, 'w') as file:
        file.write("This document has the purpose of showing the results of the checks for the Risk Treatment Plan CSV file.\n\n")
    
    yield 
    
    non_compliance_list = getattr(setup_and_teardown, 'non_compliance_list', [])
    with open(report_file, 'a') as file:
        file.write("\nNon-Compliance List:\n")
        for item in non_compliance_list:
            file.write(f"- {item}\n")

def test_csv_file_exists_and_validates_content():
    csv_file_path = 'Risk_Treatment_Plan.csv'
    report_file = 'csvchecks_report.txt'
    non_compliance_list = []

    if os.path.exists(csv_file_path):
        with open(report_file, 'a') as file:
            file.write("8.3.1a. Risk Treatment Plan exists\n")

        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            if rows:
                has_details = any('details' in value.lower() for row in rows for value in row.values() if value)

                if has_details:
                    with open(report_file, 'a') as file:
                        file.write("8.3.1b. Risk treatment plan contains details\n")
                else:
                    with open(report_file, 'a') as file:
                        file.write("[!] 8.3.1b Risk treatment plan does not contain details\n")
                    non_compliance_list.append('8.3.1b')

            else:
                with open(report_file, 'a') as file:
                    file.write("[!] 8.3.1a Risk Treatment Plan is empty\n")
                non_compliance_list.append('8.3.1a')

        except Exception as err:
            with open(report_file, 'a') as file:
                file.write(f"[!] Error parsing CSV file: {err}\n")
            non_compliance_list.append('CSV-parse error')

    else:
        with open(report_file, 'a') as file:
            file.write("[!] 8.3.1a. Risk Treatment Plan is missing!\n")
        non_compliance_list.append('8.3.1a')

    # Attach the non_compliance_list to the fixture for after test cleanup
    setup_and_teardown.non_compliance_list = non_compliance_list

