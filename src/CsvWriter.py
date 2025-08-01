import csv
from os import linesep
from typing import List

from BaseWriter import BaseWriter


class CsvWriter(BaseWriter):
    def open_output_file(self, output_file: str):
        self.file = open(output_file, encoding="UTF-8", mode='w')
        self.writer = csv.writer(self.file, )
    
    def __del__(self, *_):
        if hasattr(self, 'file') and self.file:
            self.file.close()

    def write_data(self, data: List[str]):
        row = [entry.replace(linesep, '') for entry in data]
        self.writer.writerow(row)
