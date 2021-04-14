"""
course
Class definitions for Course and Instructor.
"""
import ccutils


class Instructor:
    """
    Instructor class. For available fields see __init__
    """
    def __init__(self, fini, lname, andrew):
        # string initial letter of first name, capitalized e.g. "J"
        self.first_initial = fini

        # string last name, capitalized e.g. "Lee"
        self.last_name = lname

        # string Andrew ID, smaller case e.g. "nobodysandrew1"
        self.andrew_id = andrew

    def __repr__(self):
        return self.first_initial + ". " + self.last_name + " (" + \
            self.andrew_id + ")"


class Course:
    """
    Course class. For available fields see __init__
    """
    def __init__(self):
        # int including 98 excluding hyphen e.g. 98012
        self.number = 0

        # string WITHOUT the "Student Taught Courses (StuCo): " prefix
        # e.g. "Fun with Robots"
        self.long_title = ""

        # string WITH the "STUCO: " prefix e.g. "STUCO: FUN WTH ROBTS"
        self.short_title = ""

        # int type: 1 = Mon, 2 = Tues, ..., 7 = Sun, 0 = Error
        self.day_of_week = 0

        # datetime object denoting starting time on the day
        self.start_time = None

        # datetime object denoting ending time on the day
        self.end_time = None

        # string room abbreviated according to the university convention
        self.location = ""

        # string modality one of {'IPE', 'IPO', 'REO', 'PER', 'IPR', 'IRR'}
        self.modality = ""

        # A set of Instructor objects
        self.instructors = set()

        # int max enrollment
        self.max_enroll = 0

        # string description as same on SIO
        self.description = ""

    def __repr__(self):
        target = ""
        target += str(self.number) + "\n"
        target += self.long_title + " (" + self.short_title + ")\n"
        target += ccutils.dow2str(self.day_of_week)
        target += " " + str(self.start_time)
        target += " - " + str(self.end_time) + "\n"
        target += "Location " + self.location + "\n"
        target += "Remote only: " + str(self.modality) + "\n"
        target += "Max enroll = " + str(self.max_enroll) + "\n"
        target += "Instructor(s):"
        for instructor in self.instructors:
            target += "\n\t" + str(instructor)
        target += "\nDescription: \n\t" + self.description + "\n"

        return target
