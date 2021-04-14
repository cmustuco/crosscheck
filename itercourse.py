"""
itercourse
Iterators that take in SOC/Spreadsheet and output courses.
"""
import re
import course
import ccutils


class SocIter():
    """
    Iterator that takes in a the SOC lines and outputs courses.
    """
    def __init__(self, soc_lines):
        self.lines = soc_lines
        self.i = 0

        # Discovering entry order. Assume row 0 contains all titles
        buildup_list = ["COURSE", "COURSE TITLE", "DESCRIPTION",
                        "DAY", "BEGIN TIME", "END TIME", "BUILDING", "ROOM",
                        "INSTRUCTORS", "TEACHING MODALITY", "MAX ENROLL"]
        self.index_dict = {x: self.lines[0].index(x) for x in buildup_list}

        # Skip 98000
        while ccutils.parse_course_num(self.get_entry(self.i, "COURSE")) !=\
                98000:
            self.i += 1
            if self.i >= len(self.lines):
                break
        self.i += 1
        # self.i now points at first line after 98000 entry

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= len(self.lines):
            raise StopIteration

        # self.i now points at first row of new course
        thisCourse = course.Course()

        # Reading various info on this line
        thisCourse.number = ccutils.parse_course_num(
            self.get_entry(self.i, "COURSE"))
        title_format = r'Student Taught Courses \(StuCo\): (?P<long>.+)'\
            r' \((?P<short>STUCO: .+)\)'
        titles = re.match(title_format,
                          self.get_entry(self.i, "COURSE TITLE"))
        if titles is None:
            titles = {'long': 'Error', 'short': 'Error'}
        thisCourse.long_title = titles['long']
        thisCourse.short_title = titles['short']
        thisCourse.day_of_week = ccutils.str2dow(self.get_entry(self.i, "DAY"))
        thisCourse.start_time = ccutils.str2time(
                self.get_entry(self.i, "BEGIN TIME"))
        thisCourse.end_time = ccutils.str2time(
                self.get_entry(self.i, "END TIME"))
        building = self.get_entry(self.i, "BUILDING")
        room = self.get_entry(self.i, "ROOM")
        thisCourse.location = ccutils.building2abb(building) + " " + room
        thisCourse.modality = self.get_entry(self.i, "TEACHING MODALITY")
        thisCourse.max_enroll = int(self.get_entry(self.i, "MAX ENROLL"))
        thisCourse.description = self.get_entry(self.i, "DESCRIPTION")
        instructors = self.get_entry(self.i, "INSTRUCTORS").split(";")
        instructor_pattern = r"(?P<last_name>[A-Z][\w' -]+),\s*"\
                             r'(?P<first_initial>[A-Z])\s*\('\
                             r'(?P<andrew_id>[a-z0-9]+)\)'
        for insstr in instructors:
            insstr = insstr.strip()
            this_match = re.match(instructor_pattern, insstr)
            thisInstructor = course.Instructor(this_match["first_initial"],
                                               this_match["last_name"],
                                               this_match["andrew_id"])
            thisCourse.instructors.add(thisInstructor)

        self.i += 1
        return thisCourse

    def get_entry(self, line_num, keyword):
        return self.lines[line_num][self.index_dict[keyword]]


class SprIter():
    """
    Iterator that takes in the spreadsheet lines and outputs courses.
    """
    def __init__(self, spr_lines):
        self.lines = spr_lines
        self.i = 0

        # Discovering entry order. Assume row 0 contains all titles
        buildup_list = ["Class Number", "Long Title", "Short Title",
                        "Instructor First Name", "Instructor Last Name",
                        "Instructor AndrewID", "Room", "Max Size", "Day",
                        "Start Time", "End Time", "Modality",
                        "Course Description"]
        self.index_dict = {x: self.lines[0].index(x) for x in buildup_list}

        # Skip 98000
        while ccutils.parse_course_num(self.get_entry(self.i,
                                                      "Class Number"))\
                != 98000:
            self.i += 1
            if self.i >= len(self.lines):
                break
        self.i += 1
        # self.i now points at first line after 98000 entry

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= len(self.lines):
            raise StopIteration

        # self.i now points at first row of new course
        thisCourse = course.Course()

        # Reading various info from first row
        thisCourse.number = ccutils.parse_course_num(
                self.get_entry(self.i, "Class Number"))
        thisCourse.long_title = self.get_entry(self.i, "Long Title")
        thisCourse.short_title = self.get_entry(self.i, "Short Title")
        thisCourse.day_of_week = ccutils.str2dow(self.get_entry(self.i, "Day"))
        thisCourse.start_time = ccutils.str2time(
                self.get_entry(self.i, "Start Time"))
        thisCourse.end_time = ccutils.str2time(
                self.get_entry(self.i, "End Time"))
        thisCourse.location = self.get_entry(self.i, "Room")
        thisCourse.modality = self.get_entry(self.i, "Modality")
        thisCourse.max_enroll =\
            ccutils.parse_int(self.get_entry(self.i, "Max Size"))
        thisCourse.description = self.get_entry(self.i, "Course Description")

        # Read every instructor line by line
        while ccutils.parse_course_num(self.get_entry(self.i, "Class Number"))\
                == thisCourse.number:
            lname = self.get_entry(self.i, "Instructor Last Name").strip()
            fini = self.get_entry(self.i, "Instructor First Name").strip()[0]
            andrew = self.get_entry(self.i, "Instructor AndrewID").strip()
            thisInstructor = course.Instructor(fini, lname, andrew)
            thisCourse.instructors.add(thisInstructor)
            self.i += 1
            if self.i >= len(self.lines):
                break

        return thisCourse

    def get_entry(self, line_num, keyword):
        return self.lines[line_num][self.index_dict[keyword]]
