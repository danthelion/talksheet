import os

from dotenv import load_dotenv
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.llms.openai import OpenAI
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine

load_dotenv()


FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question, as a list of tuples and separate list of column names
"""


def read_data_from_csv(question: str, path_to_csv: str):
    engine = create_engine("duckdb:///:memory:")
    file_name = os.path.basename(path_to_csv).split(".")[0]
    # create table
    engine.execute(f"CREATE TABLE {file_name} AS SELECT * FROM '{path_to_csv}';")
    db = SQLDatabase(engine=engine)
    toolkit = SQLDatabaseToolkit(db=db)

    agent_executor = create_sql_agent(
        llm=OpenAI(temperature=0),
        toolkit=toolkit,
        verbose=True,
        format_instructions=FORMAT_INSTRUCTIONS,
    )
    response = agent_executor.run(question)
    parsed_response = eval(response)
    return parsed_response


if __name__ == "__main__":
    res = read_data_from_csv(
        "Which users name starts with E?",
        "/Users/daniel.palma/Personal/talksheet/sample_data/users.csv",
    )
    print(f"Results: {res}")
