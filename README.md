# Crosscheck

Crosscheck is a Python utility for comparing the Schedule of Classes PDF and the StuCo Spreadsheet CSV. It outputs a file detailing differences across these two documents.

## Requirements

1. Python 3
2. The Python module [pdftotext](https://pypi.org/project/pdftotext/)

## Usage

```bash
python crosscheck.py soc.pdf spr.csv out.txt
```
`soc.pdf`: Path to the Schedule of Classes PDF file. This should come from Kristin.<br />
`spr.csv`: Path to the StuCo Spreadsheet CSV file. This should be maintained by Exec.<br />
`out.txt`: An output file will be created on this path and will detail all differences found across the SOC and the Spreadsheet.  

## Notes
a\
b\
c
