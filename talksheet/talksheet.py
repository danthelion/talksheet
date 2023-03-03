import pandas as pd
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import (
    DataTable,
    Header,
    Footer,
    Input,
)

from engine.engine import read_data_from_csv


class TalkSheet(App):
    TITLE = "TalkSheet"
    SUB_TITLE = "Talk to your Spreadsheets"

    source_data_table = DataTable(id="source_table")
    results_data_table = DataTable(id="results_table")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Input(
                placeholder="path/to/file.csv", id="data_file", classes="question-box"
            ),
            self.source_data_table,
        )
        yield Container(
            Input(placeholder="Question?", id="question"), self.results_data_table
        )
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "question":
            self.ask_question()
        if event.input.id == "data_file":
            self.load_base_table(event.input.value)

    def load_base_table(self, path_to_csv: str):
        df = pd.read_csv(path_to_csv, nrows=30)
        self.source_data_table.clear(columns=True)
        self.source_data_table.add_columns(*df.columns)
        self.source_data_table.add_rows(df.values)

    def on_mount(self) -> None:
        source_file_path = self.query_one("#data_file")
        source_file_path.value = "sample_data/users.csv"
        df = pd.read_csv(source_file_path.value, nrows=30)
        self.source_data_table.add_columns(*df.columns)
        self.source_data_table.add_rows(df.values)

    def ask_question(self):
        question = self.query_one("#question")
        source_file_path = self.query_one("#data_file")
        results = read_data_from_csv(question.value, source_file_path.value)
        self.results_data_table.clear(columns=True)
        if len(results):
            columns = results[1]
            values = results[0]
            self.results_data_table.add_columns(*columns)
            self.results_data_table.add_rows(values)


app = TalkSheet(css_path="talksheet.css")
if __name__ == "__main__":
    app.run()
