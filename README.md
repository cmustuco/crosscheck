# Crosscheck

Crosscheck is a Python utility for comparing the Schedule of Classes and the StuCo Spreadsheet (both files in CSV). Usually, at the start of the semester, the Spreadsheet contains data from incoming course applications, and Kristin builds the Schedule of Classes from the Spreadsheet. However, some data fields on the SOC might be mistaken. Use this tool to generate a file detailing differences across these two documents.

## Requirements

Python 3

## Usage

Run `python crosscheck.py -h` for a complete diagnosis.

## For StuCo Exec
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

## Notes
- The parser expects these about the SOC CSV:
    - It is downloaded by Kristin from Tableau as XLSX and converted to CSV on the Unicode (UTF-8) character set, with a Field delimiter of `,`, and a string delimiter of `"`. When converting, check the "Save cell content as shown" field, and uncheck these fields: "Quote all text cells", "Fixed column width".
    - Course name matches this regex format: `Student Taught Courses \(StuCo\): (?P<long>.+) \(STUCO: (?P<short>.+)\)` otherwise course title might be parsed as "Error".
    - Day of week can be abbreviated, case insensitive:

        | Day of week | Acceptable inputs |
        | --- | --- |
        | Monday | 'M' or 'Mon' or 'Monday' |
        | Tuesday | 'T' or 'Tue' or 'Tuesday' |
        | Wednesday | 'W' or 'Wed' or 'Wednesday' |
        | Thursday | 'R' or 'Thu' or 'Thursday' |
        | Friday | 'F' or 'Fri' or 'Friday' |
        | Saturday | 'S' or 'Sat' or 'Saturday' |
        | Sunday | 'U' or 'Sun' or 'Sunday' |

    - Start/end times are written in this regex format: `\d\d?:\d{2}(:\d{2})?(A|P)M`.
    - Modality is written as one of {'IPE', 'IPO', 'REO', 'PER', 'IPR', 'IRR'}.
    - Column "Building" is the full name of the building according to the [CMU SOC Legend](https://www.cmu.edu/hub/legend.html)
- The parser expects these about the Spreadsheet CSV:
    - It is downloaded by Exec from Google Sheets as CSV.
    - The first row contains contains these columns in any order: "Class Number", "Long Title", "Short Title", "Instructor First Name", "Instructor Last Name", "Instructor AndrewID", "Room", "Max Size", "Day", "Start Time", "End Time", "Modality", "Course Description".
    - The second row contains info for 98000, which the parser ignores.
    - From the third row on, each row contains info for a course/instructor combination. For courses with more than 1 instructors, the different instructors will show up in neighboring rows.
    - Day of week can be abbreviated, case insensitive:

        | Day of week | Acceptable inputs |
        | --- | --- |
        | Monday | 'M' or 'Mon' or 'Monday' |
        | Tuesday | 'T' or 'Tue' or 'Tuesday' |
        | Wednesday | 'W' or 'Wed' or 'Wednesday' |
        | Thursday | 'R' or 'Thu' or 'Thursday' |
        | Friday | 'F' or 'Fri' or 'Friday' |
        | Saturday | 'S' or 'Sat' or 'Saturday' |
        | Sunday | 'U' or 'Sun' or 'Sunday' |

    - Start/end times are written in this regex format: `\d\d?:\d{2}(:\d{2})?(A|P)M`.
    - Modality is written as one of {'IPE', 'IPO', 'REO', 'PER', 'IPR', 'IRR'}.

## Contributing
You are welcome to improve this project. Currently, possible things to work on include:
- Support for parsing special characters e.g. ö which currently makes the regex parsing fail
- Robustness: report and do not crash when parsing fails due to incorrectly formatted input
- For some output entries (e.g. course description), write a formatted text to point out where exactly they are different
- If the spreadsheet is still on Google Sheets, call the apprpriate API to fetch the CSV from Google so the user doesn't need to manually download it each time.
