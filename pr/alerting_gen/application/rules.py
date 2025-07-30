"""functions that will validate data later and will be mentioned in config
any function should contain as parameters : data_source ,stored_data ,cols
                                 or   :  data_source ,col ,pattern
the function should return a dataframe or a string that will be sent in the email """

import re

import pandas as pd


def check_missing_rows(data_source, stored_data, cols):
    mail_to_send = ""

    if cols != ["All"]:
        data_source, stored_data = data_source[cols], stored_data[cols]

    if data_source.shape[0] != stored_data.shape[0]:
        # Merge data_source and stored_data to find rows that are in data_source but not in stored_data
        merged = data_source.merge(stored_data, how="outer", indicator=True)

        # Filter for rows only in data_source (left_only)
        missing_rows = merged[merged["_merge"] == "left_only"]

        # Get the missing rows
        missing_data = missing_rows[data_source.columns]

        # Convert missing_data to a string representation (for example)
        missing_data_str = "\nMissing Rows:\n" + missing_data.to_string(index=False)

        mail_to_send += missing_data_str

    return mail_to_send


def check_missing_rows_df(data_source, stored_data, cols):
    result_df = pd.DataFrame()
    if cols != ["All"]:
        data_source, stored_data = data_source[cols], stored_data[cols]
    if data_source.shape[0] != stored_data.shape[0]:
        # Merge data_source and stored_data to find rows that are in data_source but not in stored_data
        merged = data_source.merge(stored_data, how="outer", indicator=True)
        # Filter for rows only in data_source (left_only)
        missing_rows = merged[merged["_merge"] == "left_only"]
        # Get the missing rows
        missing_data = missing_rows[data_source.columns]
        result_df = missing_data
    return result_df


def check_wrong_values(data_source, stored_data, cols=None):
    mail_to_send = ""

    if data_source.shape[0] != stored_data.shape[0]:
        diff = data_source.shape[0] - stored_data.shape[0]
        data_source = data_source.iloc[diff:].reset_index(drop=True)

    if cols is None or cols == ["All"]:
        cols = data_source.columns.tolist()
    else:
        data_source, stored_data = data_source[cols], stored_data[cols]

    if data_source.shape[0] == stored_data.shape[0]:
        for column in cols:
            # Determine which rows are different for the current column
            diff_rows = data_source[data_source[column] != stored_data[column]]

            if not diff_rows.empty:
                # Create a detailed message for the current column
                detailed_message = f"Differences found in column '{column}':\n"
                for index, row in diff_rows.iterrows():
                    detailed_message += f"Row {index}: Stored value - {stored_data.loc[index, column]} | Data source value - {row[column]}\n"

                # Append detailed message to the main message
                mail_to_send += f"\n{detailed_message}"

    return mail_to_send


def check_wrong_values_df(data_source, stored_data, cols=None):
    # Initialize an empty list to hold the differences
    differences = []
    result_df = pd.DataFrame()

    if data_source.shape[0] != stored_data.shape[0]:
        diff = data_source.shape[0] - stored_data.shape[0]
        data_source = data_source.iloc[diff:].reset_index(drop=True)

    if cols is None or cols == ["All"]:
        cols = data_source.columns.tolist()
    else:
        data_source, stored_data = data_source[cols], stored_data[cols]

    if data_source.shape[0] == stored_data.shape[0]:
        for column in cols:
            # Determine which rows are different for the current column
            diff_rows = data_source[data_source[column] != stored_data[column]]

            if not diff_rows.empty:
                for index, row in diff_rows.iterrows():
                    # Collect the differences in a dictionary
                    differences.append(
                        {
                            "Row": index,
                            "Column": column,
                            "Stored Value": stored_data.loc[index, column],
                            "Data Source Value": row[column],
                        }
                    )

    # Create a DataFrame from the differences
    result_df = pd.DataFrame(differences)
    return result_df


def check_pattern(df, column_name, pattern):
    mail_to_send = ""
    non_matching_values = []
    # Iterate over column values and validate against the pattern
    for index, value in df[column_name].items():
        if not re.fullmatch(pattern, str(value)):
            non_matching_values.append((index, value))

    # Construct the final message
    if non_matching_values:
        mail_to_send = f"The following values in column '{column_name}' do not respect the pattern '{pattern}':\n"
        for index, value in non_matching_values:
            mail_to_send += f" - Value '{value}' at row {index}\n"

    return mail_to_send


def check_pattern_df(df, column_name, pattern):
    non_matching_values = []
    result_df = pd.DataFrame()
    # Iterate over column values and validate against the pattern
    for index, value in df[column_name].items():
        if not re.fullmatch(pattern, str(value)):
            non_matching_values.append((index, value, f" pattern {pattern} is not respected "))

    # Create a DataFrame from the non-matching values
    if non_matching_values:
        result_df = pd.DataFrame(non_matching_values, columns=["Row Index", "Value", "error"])
    else:
        result_df = pd.DataFrame(
            columns=["Row Index", "Value"]
        )  # Empty DataFrame with column names

    return result_df
