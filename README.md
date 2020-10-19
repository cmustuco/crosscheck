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
The output file lists all the differences found across both documents grouped by course. In its language, SOC means Schedule of Classes, and SPR means the Spreadsheet.

### Actions to take
Here's what to do upon each difference found:

- **Long title and short title**
    - If the SPR version doesn't seem to be too far off from the SOC version, change the SPR to the same as the SOC. Otherwise, make sure that the SPR version is what the instructors really want and report to Kristin. Sometimes the SOC PDF can truncate the titles; it's a weakness inherent to the PDF that SOC generated, we don't need to care about that.
- **Day of week, start and end time**
    - If Day of week is wrong, ask Kristin to change the SOC.
    - If start/end time is wrong, take these steps:
        1. Validate the instructor input. StuCo class lengths are always 50 mins, 80 mins, or 110 mins. Classes aren't permitted to end on the hour.
        2. If the instructor request is legitimate, verify that it is what they really want and report to Kristin.
        
        However, this is an indented block!

## Contributing

You are welcome to contribute to this project. Currently, possible things to work on include:
- Support for command-line options so future Exec can choose to ignore some subset of course data (they may not care if the descriptions are different)
- For some output entries (e.g. course description), write a formatted text to point out where exactly they are different
