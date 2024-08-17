from typing import List, NamedTuple
from rich import box
from rich.table import Table
import re

from views.View import View, OutputData


class Sort(NamedTuple):
    column: str
    order: str

class TableView(View):
    header: List[str] = []
    title: str = ""
    sort_column: Sort | None = None
    keyword: str = ""

    def __init__(self, data: List):
        self.data = data

    def prepare_output_data(self):
        if len(self.data) == 0:
            self.output_data.data = f"{self.title}. Records not found!"
            self.output_data.style = "bold red"
            self.output_data.justify = "center"
            return

        table = Table(title=self.title)

        for column in self.header:
            if self.sort_column is not None and self.sort_column.column == column.lower():
                table.add_column(f"{column} {'▲' if self.sort_column.order == 'asc' else '▼'}", style="cyan", header_style="bold cyan")
            else:
                table.add_column(column)

        for record in self.data:
            table.add_row(*self.get_row(record))

        table.box = box.SIMPLE
        self.output_data.data = table
        self.output_data.justify = "center"

    def output(self, clear = False):
        self.prepare_output_data()
        super().output(clear = clear)

    def escape(self, s: str) -> str:
        return re.sub(rf"({re.escape(self.keyword)})", r"[b magenta not dim]\1[/]", s, flags=re.IGNORECASE)

    def get_row(self, record: any) -> List[str]:
        raise NotImplementedError("get_row is not implemented")