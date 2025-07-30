import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

from alerting_gen.application import rules
from alerting_gen.config import report_path
from alerting_gen.data_access import data_access
from alerting_gen.infra.data_fetcher import get_stored_data
from alerting_gen.infra.mailing import Mailing

load_dotenv()


def get_time():
    time_format = "%Y-%h-%d-%H:%M:%S"
    time_now = datetime.now()
    return time_now.strftime(time_format)


def get_credentials():
    return os.environ["email"], os.environ["password"]


def send_mail(sender, password, receiver, subject, mail_to_send):
    try:
        # sending the alert
        mail = Mailing(sender, password, receiver)
        mail.send_mail(subject, mail_to_send)
        # reporting the alert in a text file
        path = report_path
        with open(path + "reports.txt", "a") as file:
            file.write(f"{subject}\n" + " " + get_time() + "\n")
    except Exception as e:
        print(f"Error while sending alert :{e}")


# extract
def extract_data_sources(rule_dict, my_engine):
    # Getting stored data from SQL server
    query = rule_dict.get("sql_query")
    stored_data = get_stored_data(my_engine, query)

    # Getting data_source from API
    extract_data_func = getattr(data_access, rule_dict.get("extract_data_source"))
    data_source = extract_data_func()

    return data_source, stored_data


# validate
def validate_data(rule_dict, data_source, stored_data):
    columns_to_compare = rule_dict.get("columns_to_compare")
    pattern = rule_dict.get("pattern")
    # Validating and alerting
    validating_data_func = getattr(rules, rule_dict.get("validating_data_func"))
    if pattern is None:
        alert_message = validating_data_func(
            data_source, stored_data, columns_to_compare
        )  # Returns a string
    else:
        alert_message = validating_data_func(stored_data, columns_to_compare[0], pattern)

    return alert_message


# alert
def send_alerts(alert_message, rule_dict, type_source, sender, password):
    if (isinstance(alert_message, str) and alert_message != "") or (
        isinstance(alert_message, pd.DataFrame) and (not alert_message.empty)
    ):
        receivers = rule_dict.get("receivers")
        mail_subject = rule_dict.get("mail_subject")
        for receiver in receivers:
            send_mail(sender, password, receiver, f"{mail_subject} {type_source}", alert_message)
