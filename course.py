"""
course
Class definitions for Course and Instructor.
"""


class Instructor:
    def __init__(self, fini, lname, andrew):
        # string initial letter of first name, capitalized e.g. "J"
        self.first_initial = fini

        # string last name, capitalized e.g. "Lee"
        self.last_name = lname

        # string Andrew ID, smaller case e.g. "nobodysandrew1"
        self.andrew_id = andrew


class Course:
    def __init__(self):
        # int including 98 excluding hyphen e.g. 98012
        self.number = 0
        
        # string including "Student Taught Courses (StuCo): " prefix
        # e.g. "Student Taught Courses (StuCo): Fun with Robots"
        self.long_title = ""
        
        # string including "STUCO: " prefix e.g. "STUCO: FUN WTH ROBTS"
        self.short_title = ""

        # int type: 1 = Mon, 2 = Tues, ..., 7 = Sun
        self.day_of_week = 0

        # datetime object denoting starting time on the day
        self.start_time = None

        # datetime object denoting ending time on the day
        self.end_time = None

        # string as it shows on SIO
        self.location = ""

        # bool value, trueiff the class is remote only
        self.remote_only = None

        # A list of Instructor objects
        self.instructors = []

        # string description as same on SIO
        self.description = ""

    def __repr__(self):
        target = ""
        target += str(self.number) + "\n\t"
        target += self.long_title + "\n\t"
        target += self.short_title + "\n\t"

        return target
