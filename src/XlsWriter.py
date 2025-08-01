from os import linesep
from typing import List

from xlsxwriter import Workbook

from BaseWriter import BaseWriter


class XlsWriter(BaseWriter):
    def open_output_file(self, output_file: str):
        self.file = Workbook(output_file)
        self.writer = self.file.add_worksheet()
        self.row_index = 0
    
    def __del__(self, *_):
        if hasattr(self, 'file') and self.file:
            self.file.close()

    def write_data(self, data: List[str]):
        row = [entry.replace(linesep, ' ') for entry in data]
        self.writer.write_row(self.row_index, 0, row)
        self.row_index += 1
