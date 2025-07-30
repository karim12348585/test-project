import jenkins
import pandas as pd


# Function to connect to Jenkins with timeout handling and crumb issuer
def connect_to_jenkins(url, username, password):
    # Set up the Jenkins connection with a timeout
    server = jenkins.Jenkins(url, username=username, password=password, timeout=30)
    # Check if Jenkins is reachable and the connection is successful
    server.get_whoami()
    return server


# Function to get job and build information from Jenkins and return it as a DataFrame
def get_jenkins_data(server):
    jobs_data = []
    builds_data = []

    try:
        jobs = server.get_jobs()
        for job in jobs:
            job_name = job["name"]
            job_info = server.get_job_info(job_name)
            jobs_data.append(
                {
                    "Job Name": job_name,
                    "URL": job_info["url"],
                    "Description": job_info.get("description", ""),
                    "Buildable": job_info.get("buildable", ""),
                    "Color": job_info.get("color", ""),
                }
            )

            # Fetch build information for each job
            builds = job_info.get("builds", [])
            for build in builds:
                build_number = build["number"]
                build_info = server.get_build_info(job_name, build_number)
                builds_data.append(
                    {
                        "Job Name": job_name,
                        "Build Number": build_number,
                        "Result": build_info.get("result", ""),
                        "Duration": build_info.get("duration", ""),
                        "Timestamp": build_info.get("timestamp", ""),
                    }
                )
    except jenkins.JenkinsException as e:
        print(f"Failed to retrieve jobs or builds: {e}")

    jobs_df = pd.DataFrame(jobs_data)
    builds_df = pd.DataFrame(builds_data)

    return jobs_df, builds_df
