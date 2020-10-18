"""
crosscheck
Writes a file containing any discrepancies found between the SOC and the
Spreadsheet.

Usage: python crosscheck.py soc_path spr_path out_path

Args:
    soc_path: Path to the SOC PDF file. The SOC is the Schedule of Classes and
        should come from Kristin.
    spr_path: Path to the Spreadsheet CSV file. The Spreadsheet is maintained
        maintained by Exec and should be downloaded as a CSV.
    out_path: Path to the output file that will be created and will contain
        any output info.
"""
import sys
import csv
import pdftotext
import datetime
import itercourse
import ccutils


def crosscheck(soc_lines, spr_lines):
    """
    Returns a list of error messages (strings), each containing one difference
    found between the SOC and the Spreadsheet.

    Args:
        soc_lines: a list containing each line in the SOC.
        spr_lines: a list containing each line in the spreadsheet.
    """
    soc_iter = itercourse.SocIter(soc_lines)
    soc_dict = {course.number: course for course in soc_iter}

    spr_iter = itercourse.SprIter(spr_lines)
    spr_dict = {course.number: course for course in spr_iter}

    errdict = {}

    # Checking if some course exists in one profile but not the other
    soc_pop_list = []
    for course_num in soc_dict:
        if course_num not in spr_dict:
            errdict[course_num] = [
                f"Course number {course_num} exists in SOC but not in the "
                "Spreadsheet."]
            soc_pop_list.append(course_num)
    for waste_num in soc_pop_list:
        soc_dict.pop(waste_num)

    spr_pop_list = []
    for course_num in spr_dict:
        if course_num not in soc_dict:
            errdict[course_num] = [
                f"Course number {course_num} exists in the Spreadsheet but "
                "not in SOC."]
            spr_pop_list.append(course_num)
    for waste_num in spr_pop_list:
        spr_dict.pop(waste_num)

    # Now that both dicts contain equal entries, check each course
    for course_num in soc_dict:
        soc_course = soc_dict[course_num]
        spr_course = spr_dict[course_num]
        errmsg_list = []

        # Long title
        if soc_course.long_title != spr_course.long_title:
            soc_long_title_msg = 'Long title on SOC: "' +\
                                 soc_course.long_title + '".'
            spr_long_title_msg = 'Long title on Spreadsheet: "' +\
                                 spr_course.long_title + '".'
            errmsg_list.append(soc_long_title_msg)
            errmsg_list.append(spr_long_title_msg)

        # Short title
        if soc_course.short_title != spr_course.short_title:
            soc_short_title_msg = 'Short title on SOC: "' +\
                                  soc_course.short_title + '".'
            spr_short_title_msg = 'Short title on Spreadsheet: "' +\
                                  spr_course.short_title + '".'
            errmsg_list.append(soc_short_title_msg)
            errmsg_list.append(spr_short_title_msg)

        # Day of week
        if soc_course.day_of_week != spr_course.day_of_week:
            soc_dow_msg = 'Day of week on SOC: ' +\
                          ccutils.dow2str(soc_course.day_of_week) + '.'
            spr_dow_msg = 'Day of week on Spreadsheet: ' +\
                          ccutils.dow2str(spr_course.day_of_week) + '.'
            errmsg_list.append(soc_dow_msg)
            errmsg_list.append(spr_dow_msg)

        # Start & End time
        # These following checks are specific to S21
        socst = soc_course.start_time
        socet = soc_course.end_time
        socint = ccutils.timediff(socst, socet)
        sprst = spr_course.start_time
        spret = spr_course.end_time
        sprint = ccutils.timediff(sprst, spret)
        halfpastsix = datetime.time(18, 30)
        



        if errmsg_list != []:
            errdict[course_num] = errmsg_list

    return errdict


if __name__ == "__main__":
    soc_path = sys.argv[1]
    spr_path = sys.argv[2]
    out_path = sys.argv[3]

    with open(soc_path, "rb") as soc_file:
        soc_pdf = pdftotext.PDF(soc_file)
        soc_str = "".join(soc_pdf)
        soc_lines = soc_str.split("\n")
        soc_lines = [x.strip() for x in soc_lines]

    with open(spr_path, "r") as spr_file:
        spr_reader = csv.reader(spr_file)
        spr_lines = list(spr_reader)

    error_dict = crosscheck(soc_lines, spr_lines)
    with open(out_path, "w") as out_file:
        for course_num in error_dict:
            out_file.write(str(course_num))
            for error_msg in error_dict[course_num]:
                out_file.write("\n\t" + error_msg)
            out_file.write("\n")
        if error_dict == {}:
            out_file.write("No difference found - All good!\n")
