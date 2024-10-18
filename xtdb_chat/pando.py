import os
from pandasai.connectors.sql import PostgreSQLConnector
from pandasai.smart_dataframe import SmartDataframe
from pandasai.llm.openai import OpenAI

postgres_connector = PostgreSQLConnector(
    config={
        "host": "localhost",
        "port": 5432,
        "database": "xtdb",
        "table": "customer",
        "username": "",
        "password": ""
    }
)

llm = OpenAI(api_token=os.environ.get("OPENAI_API_KEY"))
df = SmartDataframe(postgres_connector, config={"llm": llm})
response = df.chat("Select an arbitrary customer ID")

print(response)
