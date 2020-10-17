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
import itercourse


def crosscheck(soc_lines, spr_lines):
    """
    Returns a list of error messages (strings), each containing one difference
    found between the SOC and the Spreadsheet.

    Args:
        soc_lines: a list containing each line in the SOC.
        spr_lines: a list containing each line in the spreadsheet.
    """
    soc_iter = itercourse.SOCIter(soc_lines)
    for course in soc_iter:
        print(course)
    return []


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

    error_list = crosscheck(soc_lines, spr_lines)
    with open(out_path, "w") as out_file:
        for error in error_list:
            out_file.write(error + "\n")
        if error_list == []:
            out_file.write("No difference found - All good!\n")
