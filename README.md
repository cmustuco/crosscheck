# Crosscheck

Crosscheck is a Python utility for comparing the Schedule of Classes PDF and the StuCo Spreadsheet CSV. It outputs a file detailing differences across these two documents.

## Dependencies

Before use, please install the Python module [pdftotext](https://pypi.org/project/pdftotext/).

## Usage

```bash
python crosscheck.py soc_path spr_path out_path
```
soc_path: Path to the Schedule of Classes PDF file. This should come from Kristin.
spr_path: Path to the StuCo Spreadsheet CSV file. This is maintained by Exec.
out_path: An new output file will be created on this path and will detail the differences across the SOC and the Spreadsheet.

## Notes


