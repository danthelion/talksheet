import asyncio
import os

import pandas as pd
from dotenv import load_dotenv
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.llms.openai import OpenAI
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    Header,
    Input,
)

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

load_dotenv()


class TalkSheet(App):
    TITLE = "TalkSheet"
    SUB_TITLE = "Talk to your Spreadsheets"

    source_data_table = DataTable(id="source_table")
    results_data_table = DataTable(id="results_table")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = None
        self.toolkit = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Input(placeholder="path/to/file.csv", id="data_file"),
            self.source_data_table,
        )
        yield Container(
            Input(placeholder="Ask your Spreadsheet anything!", id="question"),
            self.results_data_table,
        )

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "question":
            asyncio.create_task(self.ask_question())
        if event.input.id == "data_file":
            self.load_base_table(event.input.value)

    def load_base_table(self, path_to_csv: str):
        df = pd.read_csv(path_to_csv, nrows=50)
        self.source_data_table.clear(columns=True)
        self.source_data_table.add_columns(*df.columns)
        self.source_data_table.add_rows(df.values)
        self.engine = create_engine("duckdb:///:memory:")
        self.engine.execute("INSTALL httpfs;")
        self.engine.execute("LOAD httpfs;")
        file_name = os.path.basename(path_to_csv).split(".")[0]
        file_name = "".join([c for c in file_name if c.isalnum() or c == "_"])
        self.engine.execute(
            f"CREATE TABLE {file_name} AS SELECT * FROM '{path_to_csv}';"
        )
        self.toolkit = SQLDatabaseToolkit(db=SQLDatabase(engine=self.engine))

    def on_mount(self) -> None:
        source_file_path = self.query_one("#data_file")
        # Default to bundled sample data
        sample_data_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "sample_data", "users.csv"
        )
        source_file_path.value = sample_data_path
        self.load_base_table(source_file_path.value)

    async def ask_question(self):
        question = self.query_one("#question")
        agent_executor = create_sql_agent(
            llm=OpenAI(temperature=0),
            toolkit=self.toolkit,
            verbose=True,
            format_instructions=FORMAT_INSTRUCTIONS,
        )
        results = agent_executor.run(question.value)
        try:
            parsed_results = eval(results)
        except SyntaxError:
            # Fall back to string
            parsed_results = [[(results,)], ["result"]]
        self.results_data_table.clear(columns=True)
        if len(parsed_results):
            columns = parsed_results[1]
            values = parsed_results[0]
            self.results_data_table.add_columns(*columns)
            self.results_data_table.add_rows(values)


app = TalkSheet(css_path="talksheet.css")
if __name__ == "__main__":
    app.run()
