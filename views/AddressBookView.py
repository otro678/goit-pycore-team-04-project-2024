from typing import List, NamedTuple, Dict

from record import Record
from views.View import View

from rich import box
from rich.console import Console
from rich.table import Table
import re

class Sort(NamedTuple):
    column: str
    order: str

class AddressBookView(View):
    data: List[Record]

    def __init__(self, contact_list: List[Record]):
        # possible validation of type
        super().__init__(contact_list)

    def output(self, sort_column: Sort, keyword: str):
        header = ['Name', 'Phone', 'Address', 'Birthday', 'Email']
        console = Console()

        table = Table(title="Addressbook view")

        for column in header:
            if sort_column.column == column.lower():
                table.add_column(f"{column} {"▲" if sort_column.order == "asc" else "▼"}", style="cyan", header_style="bold cyan")
            else:
                table.add_column(column)

        keyword = re.escape(keyword)

        def escape(s: str) -> str:
            return re.sub(rf"({keyword})", r"[b magenta not dim]\1[/]", s)

        for record in self.data:
            table.add_row(*[
                escape(record.name.value),
                escape(", ".join(phone.value for phone in record.phones)),
                escape(record.address.value),
                escape(str(record.birthday.value)),
                escape(record.email.value),
            ])

        table.box = box.SIMPLE

        console.print(table, justify="center")
