from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive

from textual.widgets import DataTable, Header, Footer, Input, Static, Button

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]


class TalkSheetChat(Static):
    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Input(placeholder="Question...")
        yield Button("Send", id="send", variant="success")


class TalkSheetTable(Static):
    data = reactive([])
    data_table = DataTable()

    def compose(self) -> ComposeResult:
        yield Input(placeholder="sample_data/employees.csv", id="data_file")
        yield self.data_table

    def read_data_file(self, file_name):
        with open(file_name) as f:
            self.data = [line.split(",") for line in f.readlines()]
        # TODO load into duckdb here and display in data_table

    def on_input_submitted(self, event: Input.Submitted):
        self.read_data_file(event.value)
        rows = iter(ROWS)
        self.data_table.add_columns(*next(rows))
        self.data_table.add_rows(rows)


class TalkSheet(App):
    TITLE = "TalkSheet"
    SUB_TITLE = "A Textual App"
    CSS_PATH = "talksheet.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(TalkSheetTable())
        yield Container(TalkSheetChat())


app = TalkSheet()
if __name__ == "__main__":
    app.run()
