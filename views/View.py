from dataclasses import dataclass
from typing import List, Literal

from rich.console import Console


@dataclass
class OutputData:
    data: any = None
    style: str = ""
    justify: Literal["default", "left", "center", "right", "full"] = "default"

class View:
    output_data: OutputData = OutputData()

    def output(self, clear = False):
        console = Console()

        if clear:
            console.clear()
        console.print(self.output_data.data, justify=self.output_data.justify, style=self.output_data.style)
