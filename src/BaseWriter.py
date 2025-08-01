from abc import ABC, abstractmethod
from os import linesep
from typing import List

from robot.api import SuiteVisitor
from robot.model import TestCase
from robot.utils import robottime

class BaseWriter(SuiteVisitor, ABC):
    default_format = (
        "full_name",
        "doc",
        "tags",
        "status",
        "message",
        "elapsedtime",
        "starttime",
        "endtime",
    )
    default_format_str = ",".join(default_format)
    more_format = (
        "id",
        "parent.name",
        "name",
        "parent.metadata",
        *default_format[1:],
        "timeout",
        "source",
        "lineno",
    )
    more_format_str = ",".join(more_format)

    def __init__(
        self,
        output_file: str,
        format_specifier: str = default_format_str,
        docs_max_len: int = 100,
    ):
        self.output_file, self.docs_max_len = output_file, docs_max_len
        self.format_specifier = (
            BaseWriter.more_format_str
            if format_specifier == "MORE"
            else format_specifier
        )

        self.open_output_file(self.output_file)
        self.write_header(self.format_specifier)

    def visit_test(self, test: TestCase):
        data: List[str] = list()

        for item in self.format_specifier.split(","):
            match item.lower():
                case x if "parent" in x:
                    value = str(getattr(test.parent, item.split(".")[1]))
                case "doc":
                    value = test.doc[: self.docs_max_len]
                case "shortdoc":
                    value = test.doc
                    value = value[: value.find(linesep)]
                case "tags":
                    value = ",".join(test.tags)
                case "elapsedtime":
                    value = robottime.secs_to_timestr(test.elapsedtime/1000, compact=True)
                case i:
                    value = str(getattr(test, i))
            data.append(value)

        self.write_data(data)

    def write_header(self, format_specifier: str):
        data = [self.pretty_name(entry) for entry in format_specifier.split(",")]
        self.write_data(data)

    def pretty_name(self, specifier: str):
        my_pretty_dict = {
            "doc": "Documentation",
            "starttime": "Start Time",
            "endtime": "End Time",
            "elapsedtime": "Elapsed Time",
            "lineno": "Line",
        }
        default_pretty_name = specifier.replace("_", " ").replace(".", " ").title()
        return my_pretty_dict.get(specifier, default_pretty_name)

    @abstractmethod
    def open_output_file(self, output_file: str): ...

    @abstractmethod
    def write_data(self, data: list): ...
