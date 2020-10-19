# Crosscheck

Crosscheck is a Python utility for comparing the Schedule of Classes PDF and the StuCo Spreadsheet CSV. It outputs a file detailing differences across these two documents.

## Requirements

1. Python 3
2. The Python module [pdftotext](https://pypi.org/project/pdftotext/)

## Usage

```bash
python crosscheck.py soc.pdf spr.csv out.txt
```
`soc.pdf`: Pathname of the Schedule of Classes PDF file. This should come from Kristin.\
`spr.csv`: Pathname of the StuCo Spreadsheet CSV file. This should be maintained by Exec.\
`out.txt`: An output file will be created on this pathname and will detail all differences found across the SOC and the Spreadsheet.

## Notes
The output file lists all the differences found across both documents grouped by course. In its language, SOC means Schedule of Classes, and SPR means the Spreadsheet. Here's what to do upon each type of difference found:
- Long title and short title
    If the SPR version doesn't seem to be too far off from the SOC version, change the SPR to the same as the SOC.
- Hello
   This is 3 spaces.
- 4 space
    This is 4 space.
- Tab
    This is a tab.

## Contributing

You are welcome to contribute to this project. Currently, possible things to work on include:
- Support for command-line options so future Exec can choose to ignore some subset of course data (they may not care if the descriptions are different)
- For some output entries (e.g. course description), write a formatted text to point out where exactly they are different
