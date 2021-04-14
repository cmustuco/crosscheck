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
        return 0


def dow2str(dow):
    """
    Converts a number scale of day of week to a string representation.
    """
    return ['Error', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday'][dow]


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


def building2abb(bd):
    """
    Represent the building name passed in into abbreviation according to the
    university's convention. See https://www.cmu.edu/hub/legend.html
    """
    abbreviations = {'Baker Hall': 'BH',
                     'College of Fine Arts': 'CFA',
                     'Collaborative Innovation Center': 'CIC',
                     'Carnegie Mellon': 'CMU',
                     'Cohon University Center': 'CUC',
                     'Cyert Hall': 'CYH',
                     'Doherty Hall': 'DH',
                     'Elliot Dunlap Smith Hall': 'EDS',
                     'Gesling Stadium': 'GES',
                     'Gates and Hillman Centers': 'GHC',
                     'Gates Hillman Center': 'GHC',
                     'Weigand Gymnasium': 'GYM',
                     'Hamburg Hall': 'HBH',
                     'Hamerschlag Hall': 'HH',
                     'Hunt Library': 'HL',
                     'Hall of the Arts': 'HOA',
                     '4616 Henry Street': 'INI',
                     'Mellon Institute': 'MI',
                     'Margaret Morrison Carnegie Hall': 'MM',
                     'Newell-Simon Hall': 'NSH',
                     'Off Campus': 'OFF',
                     'Purnell Center for the Arts': 'PCA',
                     'Porter Hall': 'PH',
                     'Posner Hall': 'POS',
                     'Pittsburgh Technology Center - 2nd Avenue': 'PTC',
                     'Roberts Engineering Hall': 'REH',
                     'Tepper Quad': 'TEP',
                     '300 South Craig Street': '3SC',
                     '407 South Craig Street': '4SC',
                     'Software Engineering Institute': 'SEI',
                     'Scaife Hall': 'SH',
                     'Warner Hall': 'WH',
                     'Wean Hall': 'WEH'}
    if bd in abbreviations:
        return abbreviations[bd]
    else:
        return 'Error'


def parse_course_num(numstr):
    return parse_int(re.sub("-", "", numstr))


def parse_int(numstr):
    try:
        return int(numstr)
    except ValueError:
        return "Error"
