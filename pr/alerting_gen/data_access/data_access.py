"""functions that import data from api
their names will be mentioned in the config later """
import os

from dotenv import load_dotenv

from alerting_gen.infra.data_fetcher import get_github_data
from alerting_gen.infra.jenkinsConnetion import connect_to_jenkins, get_jenkins_data
from alerting_gen.infra.jiraconnection import JiraConnection

load_dotenv()


# jira project 1
def get_jira_data_p1():
    # Example usage
    email = os.environ["jira_email_p1"]
    jira_server = os.environ["jira_server_p1"]
    jira_token = os.environ["jira_token_p1"]
    options = {"server": jira_server}

    # Instantiate and connect to Jira
    jira_conn = JiraConnection(jira_server, jira_token, options, email)
    jira_conn.connect_to_jira()

    # Define JQL query and fields to retrieve(jira parameters)
    jql_query = 'project = "KAN"'
    selected_fields = ["key", "summary", "description", "status"]
    fields_map = {
        "key": [("str", "key")],
        "summary": [("str", "fields"), ("str", "summary")],
        "description": [("str", "fields"), ("str", "description")],
        "status": [("str", "fields"), ("str", "status"), ("str", "name")],
    }
    return jira_conn.get_jira_data(jql_query, selected_fields, fields_map)


# github project 1
def get_github_data_p1():
    access_token = os.environ["github_token"]
    user_name = os.environ["github_username"]
    return get_github_data(access_token, user_name).sort_values("created_at", ascending=False)


# jenkins project 1
def get_jenkins_jobs_df():
    jenkins_url = os.environ["jenkins_url"]
    username = os.environ["jenkins_username"]
    password = os.environ["jenkins_password"]
    server = connect_to_jenkins(jenkins_url, username, password)

    return get_jenkins_data(server)[0]


def get_jenkins_builds_df():
    jenkins_url = os.environ["jenkins_url"]
    username = os.environ["jenkins_username"]
    password = os.environ["jenkins_password"]
    server = connect_to_jenkins(jenkins_url, username, password)

    return get_jenkins_data(server)[1]


# 🆕 slack channel logs or messages
def get_slack_data_p1():
    slack_token = os.environ["slack_token"]
    channel_id = os.environ["slack_channel_id"]
    return get_slack_data(slack_token, channel_id)