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
        while not self.parse_course_header(self.i):
            self.i += 1
            if self.over_bound(self.i):
                raise StopIteration
        # i currently pointing at a header

        thisCourse = course.Course()

        # Reading from header: number, long title and short title
        header_match = self.parse_course_header(self.i)
        header_dict = header_match.groupdict()
        thisCourse.number = header_dict["number"]
        thisCourse.long_title = header_dict["long_title"]
        thisCourse.short_title = header_dict["short_title"]


        self.i += 1
        return thisCourse



    def parse_course_header(self, idx):
        """
        Returns a regex match object if the string at index idx of the
        lines seems to be a valid course header. None otherwise.
        """
        curr = self.lines[idx]
        header_pattern = \
                r'(?P<number>98\d{3})'\
                r' Student Taught Courses \(StuCo\): '\
                r'(?P<long_title>.*)'\
                r' \('\
                r'(?P<short_title>STUCO: .*)'\
                r'\)'
        return re.match(header_pattern, curr)

    def over_bound(self, i):
        return self.i >= len(self.lines)
