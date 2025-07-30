from sqlalchemy import create_engine

from alerting_gen.application.validate import (
    extract_data_sources,
    get_credentials,
    send_alerts,
    validate_data,
)
from alerting_gen.config import All_Rules

# connexion to postgreSQL server (sql server)
engine = create_engine("postgresql://postgres:karim123@localhost:5432/MyDataBase")
# email credentials
sender, password = get_credentials()

# list contains the names of the sources
sources_list = ["jira", "jenkins", "github"]

# validation and alerting process
for source in sources_list:
    print(f"validating data from  {source} ...")

    for rule_dict in All_Rules.get(source):
        # extraction
        data_source, stored_data = extract_data_sources(rule_dict, engine)
        # validation
        alert_message = validate_data(rule_dict, data_source, stored_data)
        # alerting
        send_alerts(alert_message, rule_dict, source, sender, password)

print("validation is done")
