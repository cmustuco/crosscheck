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
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        while not self.is_course_header(self.idx):
            self.idx += 1
            if self.over_bound(self.i):
                raise StopIteration
        # i currently pointing at a header

       thisCourse = course.Course()



    def is_course_header(self, idx):
        curr = self.lines[idx]
        pattern = "98\d{3} Student Taught Courses \(StuCo\): .* \(STUCO: .*\)"
        return re.match(pattern, curr)

    def over_bound(self, i):
        return self.i >= len(self.lines)
