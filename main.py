import streamlit as st
import sqlite3
import pandas as pd
import sql_db
from prompts.prompts import SYSTEM_MESSAGE
from azure_openai import messages_ai
import json

def query_database(query, conn):
    """ Run SQL query and return results in a dataframe """
    return pd.read_sql_query(query, conn)

# Create or connect to SQLite database
conn = sql_db.create_connection()

# Schema Representation for finances table
schemas = sql_db.get_schema_representation()

st.title("Query SqlDB using Azure OpenAI GPT-4 model")
# Input field for the user to type a message
user_message = st.text_input("Ask your question here")

if user_message:
    # Format the system message with the schema
    formatted_system_message = SYSTEM_MESSAGE.format(schema=schemas['finances'])

    # Use GPT-4 to generate the SQL query
    response = messages_ai(formatted_system_message, user_message)
    json_start = response.find('{')
    json_end = response.rfind('}') + 1
    # Extract the JSON portion
    json_output = response[json_start:json_end].strip()
    # Load the JSON into a Python dictionary
    json_response = json.loads(json_output)
    query = json_response['query']

    # Display the generated SQL query
    st.write("Generated SQL Query:")
    st.code(query, language="sql")

    try:
        # Run the SQL query and display the results
        sql_results = query_database(query, conn)
        st.write("Query Results:")
        st.dataframe(sql_results)

    except Exception as e:
        st.write(f"An error occurred: {e}")
