""" dict contains all sources with their rules
    sql_query : contains query to fetch data from SQL Server
    extract_data_source : name of the function that extract data from API (functions are in dat_access.py)
    columns_to_compare : list of columns to compare against (use ["All"] if u don't want to specify)
    validating_data_func : name of the func that apply the rules (exp comparing) (functions are in rules.py)
    pattern : The regex pattern used for validation (columns_to_compare should contain only one column ) ."""

All_Rules = {
    "jira": [
        {
            "sql_query": "file.sql",
            "extract_data_source": "get_jira_data_p1",
            "columns_to_compare": ["key"],
            "receivers": ["souissik646@gmail.com"],
            "mail_subject": "missing data rows while extraction ",
            "validating_data_func": "check_missing_rows_df",
        },
        {
            "sql_query": "file.sql",
            "extract_data_source": "get_jira_data_p1",
            "columns_to_compare": ["All"],
            "receivers": ["souissik646@gmail.com"],
            "mail_subject": "wrong values  while extraction ",
            "validating_data_func": "check_wrong_values_df",
        },
        {
            "sql_query": "file.sql",
            "columns_to_compare": ["key"],
            "extract_data_source": "get_jira_data_p1",
            "pattern": r"KANb-\d",
            "receivers": ["souissik646@gmail.com"],
            "mail_subject": "wrong pattern",
            "validating_data_func": "check_pattern_df",
        },
    ],
    "github": [
        {
            "sql_query": "file_2.sql",
            "extract_data_source": "get_github_data_p1",
            "columns_to_compare": ["All"],
            "receivers": ["souissik646@gmail.com"],
            "mail_subject": "missing data rows while extraction ",
            "validating_data_func": "check_missing_rows_df",
        },
    ],
    "jenkins": [
        {
            "sql_query": "file_3.sql",
            "extract_data_source": "get_jenkins_builds_df",
            "columns_to_compare": ["All"],
            "receivers": ["souissik646@gmail.com"],
            "mail_subject": "missing data rows while extraction ",
            "validating_data_func": "check_missing_rows_df",
        },
    ],
}
# the path  should end with /
sql_folder_path = "C:/Users/LEGION/Desktop/summer internship 2024/alerting generation system/alerting_gen/sql files/"

# the path of the reports.txt
report_path = "C:/Users/LEGION/Desktop/summer internship 2024/alerting generation system/alerting_gen/reports.txt"
