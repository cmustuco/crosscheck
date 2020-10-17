"""
course
Class definitions for Course and Instructor.
"""


class Instructor:
    def __init__(self, fini, lname, andrew):
        self.first_initial = fini
        self.last_name = lname
        self.andrew_id = andrew


class Course:
    def __init__(self):
        self.title = ""
        self.day_of_week = 0  # 1 = Mon, 2 = Tues, ..., 7 = Sun
        self.start_time = None  # datetime object
        self.end_time = None  # datetime object
        self.location = ""
        self.remote = None  # Boolean value, true iff the class is remote
        self.instructors = []  # A list of Instructor objects
        self.description = ""
