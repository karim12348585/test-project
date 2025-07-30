"""general functions for data fetching from (APIs ,sql server ...)"""

import pandas as pd
from github import Github

from alerting_gen.config import sql_folder_path

path = sql_folder_path


# accessing to SQl server Databases
def get_stored_data(engine, sql_file):
    global path
    # absolute path of sql files folder
    file = path + sql_file
    try:
        with open(file, "r") as file:
            sql_query = file.read()
        data = pd.read_sql(sql_query, engine)
        return data
    except Exception as e:
        print(f"Error reading stored data: {e}")
        return pd.DataFrame()


# general function to access to github data using api
def get_github_data(access_token, user_name):
    g = Github(access_token)
    user = g.get_user(user_name)
    repos = user.get_repos()
    # Extract relevant information and store it in a list of dictionaries
    repo_data = []
    for repo in repos:
        repo_info = {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "url": repo.html_url,
            "created_at": repo.created_at,
            "updated_at": repo.updated_at,
            "language": repo.language,
            "forks_count": repo.forks_count,
            "stargazers_count": repo.stargazers_count,
            "watchers_count": repo.watchers_count,
        }
        repo_data.append(repo_info)

    return pd.DataFrame(repo_data)
