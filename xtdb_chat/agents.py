import database
import json
from swarm import Agent

def create_prompt(params):
    schema = params["schema"]
    prompt = "You are an intelligent and technically skilled SQL engineer who responds to requests for data.\n"
    prompt += "You may ask clarifying questions about the user's intent which allow you to construct a correct SQL query.\n"
    prompt += "When you understand the user request, generate a valid SQL select statement and execute it against the database.\n"
    prompt += "If the generated SQL has any order by clauses using aggregate functions, alias the aggregate function and use the alias in the order by clause instead.\n"
    prompt += "You shouldn't write non-deterministic queries using RANDOM(), use deterministic sorting whenever you can.\n"
    prompt += "You have access to the database schema in structured JSON format, provided below.\n"
    prompt += "Refer to tables using their corresponding \"tableName\" and \"schemaName\" values.\n"
    prompt += str(schema)
    return prompt

def exec_select_query(context_variables, query):
    """Executes the provided SQL SELECT query against the read-only database"""
    print(f"SQL: \033[32;1m{query}\033[0m")
    conn = database.get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        results = cur.fetchall()
    except:
        print(f"\033[91;1m😥 An SQL error occurred\033[0m")
        results = None
    cur.close()
    return results

class SQLAgent:
    def __init__(self):
        conn = database.get_connection()
        with open('resources/tables.json', 'r') as file:
            schema = file.read()
        self.agent = Agent(
            name = "SQL Agent",
            instructions = create_prompt({"schema": schema}),
            functions = [exec_select_query],
        )
