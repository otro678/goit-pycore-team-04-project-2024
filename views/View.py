from typing import List


class View:
    def get_row(self, record: any) -> List[str]:
        raise NotImplementedError("get_row is not implemented")