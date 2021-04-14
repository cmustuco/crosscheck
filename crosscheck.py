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
            errdict[course_num] = ["Exists in SOC but not in SPR."]
            soc_pop_list.append(course_num)
    for waste_num in soc_pop_list:
        soc_dict.pop(waste_num)

    spr_pop_list = []
    for course_num in spr_dict:
        if course_num not in soc_dict:
            errdict[course_num] = ["Exists in SPR but not in SOC."]
            spr_pop_list.append(course_num)
    for waste_num in spr_pop_list:
        spr_dict.pop(waste_num)

    # Now that both dicts contain equal entries, check each course
    for course_num in soc_dict:
        soc_course = soc_dict[course_num]
        spr_course = spr_dict[course_num]
        errmsg_list = []

        # Long title
        if soc_course.long_title == 'Error':
            errmsg_list.append("Error parsing long title on SOC.")
        if soc_course.long_title != spr_course.long_title:
            soc_long_title_msg = 'Long title on SOC: "' +\
                                 soc_course.long_title + '".'
            spr_long_title_msg = 'Long title on SPR: "' +\
                                 spr_course.long_title + '".'
            errmsg_list.append(soc_long_title_msg)
            errmsg_list.append(spr_long_title_msg)

        # Short title
        if soc_course.short_title == 'Error':
            errmsg_list.append("Error parsing short title on SOC.")
        if soc_course.short_title != spr_course.short_title:
            soc_short_title_msg = 'Short title on SOC: "' +\
                                  soc_course.short_title + '".'
            spr_short_title_msg = 'Short title on SPR: "' +\
                                  spr_course.short_title + '".'
            errmsg_list.append(soc_short_title_msg)
            errmsg_list.append(spr_short_title_msg)

        # Day of week
        if soc_course.day_of_week == 0:
            errmsg_list.append("Error parsing day of week on SOC.")
        if spr_course.day_of_week == 0:
            errmsg_list.append("Error parsing day of week on SPR.")
        if soc_course.day_of_week != spr_course.day_of_week:
            soc_dow_msg = 'Day of week on SOC: ' +\
                          ccutils.dow2str(soc_course.day_of_week) + '.'
            spr_dow_msg = 'Day of week on SPR: ' +\
                          ccutils.dow2str(spr_course.day_of_week) + '.'
            errmsg_list.append(soc_dow_msg)
            errmsg_list.append(spr_dow_msg)

        # Start & End time
        if soc_course.start_time != spr_course.start_time or\
                soc_course.end_time != spr_course.end_time:
            soc_set_msg = 'Time range on SOC: ' +\
                          ccutils.time2str(soc_course.start_time) + ' - ' +\
                          ccutils.time2str(soc_course.end_time) + '.'
            spr_set_msg = 'Time range on SPR: ' +\
                          ccutils.time2str(spr_course.start_time) + ' - ' +\
                          ccutils.time2str(spr_course.end_time) + '.'
            errmsg_list.append(soc_set_msg)
            errmsg_list.append(spr_set_msg)

        # Duration
        socdur = ccutils.timediff(soc_course.start_time, soc_course.end_time)
        sprdur = ccutils.timediff(spr_course.start_time, spr_course.end_time)
        if socdur != sprdur:
            soc_dur_msg = 'Duration on SOC: ' + str(socdur)
            spr_dur_msg = 'Duration on SPR: ' + str(sprdur)
            errmsg_list.append(soc_dur_msg)
            errmsg_list.append(spr_dur_msg)

        # Location
        if soc_course.location != spr_course.location:
            soc_loc_msg = 'Location on SOC: "' + soc_course.location + '".'
            spr_loc_msg = 'Location on SPR: "' + spr_course.location + '".'
            errmsg_list.append(soc_loc_msg)
            errmsg_list.append(spr_loc_msg)

        # Modality
        if soc_course.modality != spr_course.modality:
            soc_mod_msg = 'Modality on SOC: "' + soc_course.modality + '".'
            spr_mod_msg = 'Modality on SPR: "' + spr_course.modality + '".'
            errmsg_list.append(soc_mod_msg)
            errmsg_list.append(spr_mod_msg)

        # Instructors #########################################################
        soc_ins_dict = {ins.andrew_id: ins for ins in soc_course.instructors}
        spr_ins_dict = {ins.andrew_id: ins for ins in spr_course.instructors}

        # Check if any instructor is only in one profile and not the other
        soc_ins_pop_list = []
        for insid in soc_ins_dict:
            if insid not in spr_ins_dict:
                soc_ins_msg = 'Instructor ' + str(soc_ins_dict[insid]) +\
                        ' is included in SOC but not in SPR.'
                errmsg_list.append(soc_ins_msg)
                soc_ins_pop_list.append(insid)
        for waste_id in soc_ins_pop_list:
            soc_ins_dict.pop(waste_id)

        spr_ins_pop_list = []
        for insid in spr_ins_dict:
            if insid not in soc_ins_dict:
                spr_ins_msg = 'Instructor ' + str(spr_ins_dict[insid]) +\
                        ' is included in SPR but not in SOC.'
                errmsg_list.append(spr_ins_msg)
                spr_ins_pop_list.append(insid)
        for waste_id in spr_ins_pop_list:
            spr_ins_dict.pop(waste_id)

        # Now both profiles contain equal instructor IDs, check each name
        for insid in soc_ins_dict:
            soc_ins = soc_ins_dict[insid]
            spr_ins = spr_ins_dict[insid]
            if soc_ins.first_initial != spr_ins.first_initial:
                fini_msg = 'Instructor ' + str(soc_ins) +\
                        ' has first name initial "' + soc_ins.first_initial +\
                        '" in SOC but "' + spr_ins.first_initial + '" in SPR.'
                errmsg_list.append(fini_msg)
            if soc_ins.last_name != spr_ins.last_name:
                lname_msg = 'Instructor ' + str(soc_ins) + ' has last name "'\
                    + soc_ins.last_name + '" in SOC but "'\
                    + spr_ins.last_name + '" in SPR.'
                errmsg_list.append(lname_msg)
        #######################################################################

        # Max enroll
        if soc_course.max_enroll == "Error":
            errmsg_list.append("Error parsing Max Enroll on SOC.")
        if spr_course.max_enroll == "Error":
            errmsg_list.append("Error parsing Max Enroll on SPR.")
        if soc_course.max_enroll != spr_course.max_enroll:
            soc_me_msg = 'Max Enroll on SOC is ' +\
                    str(soc_course.max_enroll) + '.'
            spr_me_msg = 'Max Enroll on SPR is ' +\
                    str(spr_course.max_enroll) + '.'
            errmsg_list.append(soc_me_msg)
            errmsg_list.append(spr_me_msg)

        # Description
        soc_desc = soc_course.description.replace(" ", "").replace("\n", "")\
            .replace("\t", "")
        spr_desc = spr_course.description.replace(" ", "").replace("\n", "")\
            .replace("\t", "")
        if soc_desc != spr_desc:
            des_msg = "Course descriptions are different."
            errmsg_list.append(des_msg)

        if errmsg_list != []:
            errdict[course_num] = errmsg_list

    return errdict


def main():
    soc_path = sys.argv[1]
    spr_path = sys.argv[2]
    out_path = sys.argv[3]

    with open(soc_path, "r") as soc_file:
        soc_reader = csv.reader(soc_file)
        soc_lines = list(soc_reader)

    with open(spr_path, "r") as spr_file:
        spr_reader = csv.reader(spr_file)
        spr_lines = list(spr_reader)

    error_dict = crosscheck(soc_lines, spr_lines)
    with open(out_path, "w") as out_file:
        if error_dict == {}:
            out_file.write("No difference found - All good!")
            print("No difference found - All good!")
        else:
            for course_num in error_dict:
                out_file.write(str(course_num))
                for error_msg in error_dict[course_num]:
                    out_file.write("\n\t" + error_msg)
                out_file.write("\n")
            print(f"Discrepancies found from {len(error_dict)} courses "
                  f"written to {out_path}.")


if __name__ == "__main__":
    main()
