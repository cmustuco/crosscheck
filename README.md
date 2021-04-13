# Crosscheck

Crosscheck is a Python utility for comparing the Schedule of Classes and the StuCo Spreadsheet (both files in CSV). It outputs a file detailing differences across these two documents.

## Requirements

Python 3

## Usage

Usually, at the start of the semester, the Spreadsheet contains data from incoming course applications. Kristin builds the Schedule of Classes from the Spreadsheet but some data fields on the SOC might be mistaken. Run the following command to find out if any data fields differ across the SOC and the Spreadsheet:

```bash
python crosscheck.py soc.pdf spr.csv out.txt
```
`soc.pdf`: Pathname of the Schedule of Classes CSV file. This should come from Kristin.\
`spr.csv`: Pathname of the StuCo Spreadsheet CSV file. This should be maintained by Exec.\
`out.txt`: An output file will be created on this pathname and will detail all differences found across the SOC and the Spreadsheet.

## For StuCo Exec
The output file lists all the differences found across both documents grouped by course number. SOC means Schedule of Classes, and SPR means the Spreadsheet.

### Actions to take
Here's what to do upon each difference found:

- **Long title, Short title, Description**
    - If the SPR version doesn't seem to be too far off from the SOC version, change the SPR to match the SOC. Otherwise, make sure that the SPR version is what the instructors really want and report to Kristin.
- **Day of week, Modality, Instructors**
    - Verify and ask Kristin to change the SOC.
- **Location, Max Enroll**
    - Kristin decides the enrollment cap and location based on historical max and room capacities. Change the Spreadsheet to match the SOC.
- **Start and End time**
    - Validate the instructor input. StuCo class lengths are always 50 mins, 80 mins, or 110 mins. Classes aren't permitted to end on the hour.
    - If the instructor input is bad, go with the nearest reasonable time range on both the Spreadsheet and the SOC. For example, if some course wants to have a 60-min class from 6:30 to 7:30, change that to a 50-min class from 6:30 to 7:20. If it's not clear what the instructors want, contact them to find out.
    - If the instructor request is legitimate, verify that it is what they really want and report to Kristin.

Exec should go over the output list of differences, make any changes needed to the Spreadsheet, and then forward to Kristin a list of changes to be made to the SOC.

### Notes
- The parser expects these about the SOC CSV:
- The parser expects these about the Spreadsheet CSV:
    - The first row contains contains these columns in any order: "Class Number", "Long Title", "Short Title", "Instructor First Name", "Instructor Last Name", "Instructor AndrewID", "Room", "Max Size", "Day", "Start Time", "End Time", "Modality", "Course Description".
    - The second row contains info for 98000, which the parser ignores.
    - From the third row on, each row contains info for a course/instructor combination. For courses with more than 1 instructors, the different instructors will show up in neighboring rows.
    - Course number is written with a hyphen e.g. "98-000"
    - Day of week is written in this format:

        | Day of week | Acceptable inputs |||
        | --- | --- | --- | --- | --- |
        | Monday | 'M' | 'Mon' | 'Monday' |
        | Tuesday | 'T' | 'Tue' | 'Tuesday' |

        | e | e |
        | 45 | 35 |
    - Start/end times are written in this regex format: `\d\d?:\d{2}(:\d{2})?(A|P)M`

## Contributing

You are welcome to improve this project. Currently, possible things to work on include:
- Support for command-line options so future Exec can choose to ignore some subset of course data (they may not care if the descriptions are different)
- For some output entries (e.g. course description), write a formatted text to point out where exactly they are different
- If the spreadsheet is still on Google Sheets, call the apprpriate API to fetch the CSV from Google so the user doesn't need to manually download it each time.
    - In this case, it's also possible to *automate some changes* to the cloud document when it's clear some field on the Spreadsheet needs to be changed.
