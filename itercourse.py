"""
itercourse
Iterators that take in SOC/Spreadsheet and output courses.
"""
import re
import course
import ccutils


class SOCIter():
    """
    Iterator that takes in a list of lines in SOC and outputs courses.
    """
    def __init__(self, soc_lines):
        self.lines = soc_lines
        self.i = 0

        # For regex matching purpose
        self.header_pattern = \
            r'(?P<number>98\d{3})'\
            r' Student Taught Courses \(StuCo\): (?P<long_title>.+)'\
            r' \((?P<short_title>STUCO: .+)\)'\
            r'\s+(?P<units>[\d~]+) units'

        # Skip 98000
        while not re.match(self.header_pattern, self.lines[self.i]):
            self.i += 1
            if self.i >= len(self.lines):
                raise StopIteration
        self.i += 1

    def __iter__(self):
        return self

    def __next__(self):
        # Find next course header line
        while not re.match(self.header_pattern, self.lines[self.i]):
            self.i += 1
            if self.i >= len(self.lines):
                raise StopIteration

        this_course = course.Course()

        # Parse number, long title, short title and units to course
        header_dict = re.match(self.header_pattern,
                               self.lines[self.i]).groupdict()
        this_course.number = header_dict["number"]
        this_course.long_title = header_dict["long_title"]
        this_course.short_title = header_dict["short_title"]

        # Build info pattern from info header
        self.i += 1
        info_pattern = self.prepare_info_pattern(self.lines[self.i])

        # Parse info line with info header and add info to course
        self.i += 1
        info_dict = re.match(info_pattern, self.lines[self.i]).groupdict()
        this_course.day_of_week = ccutils.str2dow(info_dict["day_of_week"])
        this_course.start_time = ccutils.str2time(info_dict["start_time"])
        this_course.end_time = ccutils.str2time(info_dict["end_time"])
        this_course.location = info_dict["location"].strip()
        if this_course.location == "CMU REMOTE":
            this_course.remote_only = True
        else:
            this_course.remote_only = False
        this_course.max_enroll = int(info_dict["max_enroll"])
        this_course.instructors = info_dict["instructors"].strip()

        return this_course

    def prepare_info_pattern(self, info_header):
        """
        Given the information header string, prepare a regex pattern
        """
        buildup_list = \
            [('LEC/SEC', 'lecture', r'[A-Z0-9]+'),
             ('DAY(S)', 'day_of_week', '(M|T|W|R|F|S|U|, )+'),
             ('BEGIN TIME', 'start_time', r'\d{2}:\d{2}(A|P)M'),
             ('END TIME', 'end_time', r'\d{2}:\d{2}(A|P)M'),
             ('BLDG/ROOM', 'location', r'[A-Z0-9 ]+'),
             ('INSTRUCTOR(S)', 'instructors',
              r'[A-Z][\w ]*,\s+[A-Z]\s+\(\w+\);*.*'),
             ('MAX ENROLL', 'max_enroll', r'[0-9]+'),
             ('ACT ENROLL', 'act_enroll', r'[0-9]+'),
             ('WL SIZE', 'wl_size', r'[0-9]+'),
             ('LOCATION', 'campus', r'\w+')]
        buildup_list.sort(key=lambda x: info_header.find(x[0]))
        buildup_list = ['(?P<' + x[1] + '>' + x[2] + ')' for x in buildup_list]
        buildup_list = [buildup_list[0]] + \
            [r'\s+' + x for x in buildup_list[1:]]
        return "".join(buildup_list)
