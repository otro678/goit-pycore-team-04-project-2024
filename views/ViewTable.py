from typing import List, NamedTuple
from rich import box
from rich.console import Console
from rich.table import Table
import re

from views.View import View

class Sort(NamedTuple):
    column: str
    order: str

class ViewTable(View):
    header: List[str] = []
    title: str = ""
    sort_column: Sort | None = None
    keyword: str = ""

    def __init__(self, data: List):
        self.data = data

    def output(self):
        console = Console()

        if len(self.data) == 0:
            console.print(f"{self.title}. Records not found!", style="bold red",  justify="center")
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
        console.clear()
        console.print(table, justify="center")

    def escape(self, s: str) -> str:
        return re.sub(rf"({re.escape(self.keyword)})", r"[b magenta not dim]\1[/]", s, flags=re.IGNORECASE)
