import pandas as pd
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import (
    DataTable,
    Header,
    Footer,
    Input,
    Static,
    Button,
    Markdown,
    TextLog,
)
from textual.widget import Widget

from engine.engine import read_data_from_csv


class TalkSheet(App):
    TITLE = "TalkSheet"
    SUB_TITLE = "Talk to your Spreadsheets"
    source_data_table = DataTable(id="source_table")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="sample_data/employees.csv", id="data_file")
        yield Input(placeholder="Question?", id="question")
        yield self.source_data_table
        yield TextLog()
        yield Footer()

    def load_base_data(self, path_to_csv: str):
        df = pd.read_csv(path_to_csv, nrows=5)
        self.source_data_table.add_columns(*df.columns)
        self.source_data_table.add_rows(df.values)

    def on_ready(self) -> None:
        """Called  when the DOM is ready."""
        text_log = self.query_one(TextLog)
        text_log.write("Welcome to TalkSheet!")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "question":
            self.ask_question()

    def on_mount(self) -> None:
        df = pd.read_csv("sample_data/users.csv", nrows=5)
        self.source_data_table.add_columns(*df.columns)
        self.source_data_table.add_rows(df.values)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.ask_question()

    def ask_question(self):
        question = self.query_one("#question")
        res = read_data_from_csv(question.value, "sample_data/users.csv")
        text_log = self.query_one(TextLog)
        text_log.write(res)


app = TalkSheet()
if __name__ == "__main__":
    app.run()
