from typing import List, NamedTuple
from rich import box
from rich.console import Console
from rich.table import Table
import re


class Sort(NamedTuple):
    column: str
    order: str

class View:
    header: List[str]
    title: str

    def __init__(self, data: List):
        self.data = data

    def output(self, sort_column: Sort, keyword: str):
        console = Console()

        if len(self.data) == 0:
            console.print("Records not found!", style="bold red",  justify="center")
            return

        table = Table(title=self.title)

        for column in self.header:
            if sort_column.column == column.lower():
                table.add_column(f"{column} {"▲" if sort_column.order == "asc" else "▼"}", style="cyan", header_style="bold cyan")
            else:
                table.add_column(column)

        keyword = re.escape(keyword)

        for record in self.data:
            table.add_row(*self.get_row(record, keyword))

        table.box = box.SIMPLE
        console.clear()
        console.print(table, justify="center")

    def escape(self, s: str, keyword: str) -> str:
        return re.sub(rf"({keyword})", r"[b magenta not dim]\1[/]", s)

    def get_row(self, record: any, keyword: any) -> List[str]:
        raise NotImplementedError("get_row is not implemented")