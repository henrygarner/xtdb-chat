from swarm import Agent
from swarm.repl import run_demo_loop
import database

def create_prompt(params):
    schema = params["schema"]
    prompt = "You are an intelligent and technically skilled SQL engineer who responds to requests for data.\n"
    prompt += "You may ask clarifying questions about the user's intent which allow you to construct a correct SQL query.\n"
    prompt += "When you understand the user request, generate a valid SQL select statement and execute it against the database.\n"
    prompt += "If the generated SQL has any order by clauses using aggregate functions, alias the aggregate function and use the alias in the order by clause instead.\n"
    prompt += "You have access to the database INFORMATION_SCHEMA.columns output, provided below:\n"
    prompt += str(schema)
    return prompt

def exec_select_query(context_variables, query):
    """Executes the provided SQL SELECT query against the read-only database"""
    print(f"SQL: \033[32;1m{query}\033[0m")
    conn = database.get_connection()
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    return results

if __name__ == "__main__":
    conn = database.get_connection()
    schema = database.get_schema(conn)
    sql_agent = Agent(
        name = "SQL Agent",
        instructions = create_prompt({"schema": schema}),
        functions = [exec_select_query],
    )
    run_demo_loop(sql_agent, stream=True)
