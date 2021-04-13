"""
ccutils
crosscheck utils
Various utilities for use for the crosscheck project.
"""
import re
import datetime


def str2dow(curr):
    """
    Converts a string representation of a day of week into a number scale
    where 1 = Monday, ..., 7 = Sunday, and -1 = Error.
    """
    curr = curr.lower()
    buildup_list = ['m', 'mon', 'monday',
                    't', 'tue', 'tuesday',
                    'w', 'wed', 'wednesday',
                    'r', 'thu', 'thursday',
                    'f', 'fri', 'friday',
                    's', 'sat', 'saturday',
                    'u', 'sun', 'sunday']
    if curr in buildup_list:
        return (buildup_list.index(curr) // 3) + 1
    else:
        return -1


def dow2str(dow):
    """
    Converts a number scale of day of week to a string representation.
    """
    if dow == 1:
        return "Monday"
    if dow == 2:
        return "Tuesday"
    if dow == 3:
        return "Wednesday"
    if dow == 4:
        return "Thursday"
    if dow == 5:
        return "Friday"
    if dow == 6:
        return "Saturday"
    if dow == 7:
        return "Sunday"
    return "Noday"


def str2time(curr):
    """
    Converts a string representation of a time to a datetime object.
    Input: \d\d?:\d{2}(:\d{2})?(A|P)M
    """
    curr = re.sub(r"(?P<actual_time>\d\d?:\d{2}):\d{2} ?(?P<ampm>(A|P)M)",
                  r"\g<actual_time>\g<ampm>", curr)
    is_pm = curr[-2] == 'P'
    if is_pm:
        format_str = "%H:%MPM"
    else:
        format_str = "%H:%MAM"
    this_time = datetime.datetime.strptime(curr, format_str)
    if (is_pm):
        this_time += datetime.timedelta(hours=12)
    return this_time.time()


def timediff(time1, time2):
    """
    Given two datetime.time objects, return a datetime.timedelta object.
    """
    datetime1 = datetime.datetime.combine(datetime.date.today(), time1)
    datetime2 = datetime.datetime.combine(datetime.date.today(), time2)
    timedelta = datetime2 - datetime1
    return timedelta


def before(time1, time2):
    """
    Return True iff time1 is before time2.
    """
    return timediff(time2, time1).days < 0


def time2str(curr):
    """
    Represent the given time in the format \d{2}:\d{2}, in 24 hours notation.
    """
    return datetime.time.strftime(curr, "%H:%M")
