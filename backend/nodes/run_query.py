import duckdb
import pandas as pd
import numpy as np


def run_query(state):

    query = state["sql_query"].strip()

    if not query.upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")

    connection = duckdb.connect("customer_profile.duckdb")

    result_df = connection.execute(query).fetchdf()

    connection.close()

    state["query_result"] = result_df

    return state