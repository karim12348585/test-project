import pandas as pd
from sqlalchemy import create_engine


class DatabaseHelper:
    def __init__(self, sql_sever, sql_db, port, user_sql, password_sql):
        connection_string = "mssql+pyodbc://{}:{}@{}:{}/{}?driver=SQL+Server".format(
            user_sql, password_sql, sql_sever, port, sql_db
        )
        self.engine = create_engine(connection_string, use_setinputsizes=False)

    def create_table(self, dataframe, table_name, if_exists="append"):
        dataframe.to_sql(table_name, self.engine, if_exists=if_exists, index=False)

    def read_data(self, table_name, selected_columns=None):
        query = (
            f"SELECT * FROM {table_name}"
            if selected_columns
            else f"SELECT {', '.join(selected_columns)} FROM {table_name}"
        )
        data = pd.read_sql(query, self.engine)
        return data

    def insert_dataframe(self, dataframe, table_name):
        dataframe.to_sql(table_name, self.engine, if_exists="append", index=False)
