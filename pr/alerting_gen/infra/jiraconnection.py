import pandas as pd
from jira import JIRA


class JiraConnection:
    def __init__(self, jira_server, jira_token, options, email):
        self.jira_server = jira_server
        self.jira_token = jira_token
        self.options = options
        self.email = email

    def connect_to_jira(self):
        """Connects to the Jira instance."""
        self.jira = JIRA(
            server=self.jira_server,
            token_auth=self.jira_token,
            options=self.options,
            basic_auth=(self.email, self.jira_token),
        )

    def create_issue(self, fields):
        return self.jira.create_issue(fields=fields, prefetch=True)

    def create_issues(self, field_list):
        return self.jira.create_issues(field_list=field_list, prefetch=True)

    def search_issues(self, jql_l, selected_fields):
        return self.jira.search_issues(
            jql_l, startAt=0, maxResults=None, fields=selected_fields, expand="names"
        )

    @staticmethod
    def get_issue_fields(issue, fields_map):
        def deep_get(value, path_and_type):
            if not path_and_type or value is None:
                return value
            type, path = path_and_type[0]
            if type == "list":
                return [deep_get(ele.get(path), path_and_type[1:]) for ele in value]
            else:
                return deep_get(value.get(path), path_and_type[1:])

        return {
            result_field: deep_get(issue.raw, path_and_type)
            for result_field, path_and_type in fields_map.items()
        }

    def search_issues_fields(self, jql_l, selected_fields, fields_map):
        issues = self.search_issues(jql_l, selected_fields)
        return [JiraConnection.get_issue_fields(issue, fields_map) for issue in issues]

    # general function to access to jira data using api
    def get_jira_data(self, jql_query, selected_fields, fields_map):
        self.connect_to_jira()
        issues_data = self.search_issues_fields(jql_query, selected_fields, fields_map)
        return pd.DataFrame(issues_data)
