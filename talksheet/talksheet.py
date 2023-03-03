import pandas as pd
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.containers import Container
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

    def on_ready(self) -> None:
        """Called  when the DOM is ready."""
        pass

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "question":
            self.ask_question()

    def on_mount(self) -> None:
        df = pd.read_csv("sample_data/purchase_items.csv", nrows=10)
        self.source_data_table.add_columns(*df.columns)
        self.source_data_table.add_rows(df.values)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.ask_question()

    def ask_question(self):
        question = self.query_one("#question")
        res = read_data_from_csv(question.value, "sample_data/purchase_items.csv")
        # text_log = self.query_one(TextLog)
        # text_log.write(res)
        results = eval(res)
        if len(results):
            columns = ["column_" + str(i) for i in range(len(results[0]))]
            self.results_data_table.add_columns(*columns)
        self.results_data_table.add_rows(eval(res))


app = TalkSheet(css_path="talksheet.css")
if __name__ == "__main__":
    app.run()
