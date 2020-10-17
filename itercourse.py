"""
itercourse
Iterators that take in SOC/Spreadsheet and output courses.
"""
import course
import re


class SOCIter():
    """
    Iterator that takes in a list of lines in SOC and outputs courses.
    """
    def __init__(self, soc_lines):
        self.lines = soc_lines
        self.idx = 0
        self.max_idx = len(self.lines) - 1

    def __iter__(self):
        return self

    def __next__(self):
        #  while not self.is_course_header()

    def is_course_header(self, s):
        pattern = "98\d{3} Student Taught Courses \(StuCo\): .* \(STUCO: .*\)"
        return re.match(pattern, s)
