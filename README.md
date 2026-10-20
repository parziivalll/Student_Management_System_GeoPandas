# Student Management System with GeoPandas

A beginner-friendly Python Data Science mini project for college.

## Features
- Add, view, search, and delete student records
- Save records in `students.csv`
- Calculate average marks and attendance, and count pass/fail students
- Plot student marks and city-wise counts
- Use GeoPandas to represent recognized student cities as geographic points

## Requirements
- Python 3.10 or newer recommended
- Internet connection for the initial package installation

## Setup
Open a terminal in this folder and run:

```bash
python -m pip install -r requirements.txt
```

Then start the project:

```bash
python student_management.py
```

On some Windows installations, use `py` instead of `python`.

## First run
The program automatically creates `students.csv` with five sample students. You can view them using menu option 2. Add, edit, or remove records by using the program or editing the CSV carefully.

## GeoPandas demonstration
Choose menu option 7. The program converts city longitude/latitude into point geometries in a GeoDataFrame using the EPSG:4326 coordinate reference system, then plots the points.

The chart is a longitude/latitude point plot, not a street map or geographic boundary map. Only cities listed in `CITY_COORDINATES` can be plotted. Add more city coordinates in the source code if needed.

## Project files
- `student_management.py` — main application
- `requirements.txt` — required Python libraries
- `students.csv` — sample data (created automatically if absent)
- `PROJECT_REPORT.md` — project overview, workflow, and limitations
- `VIVA_QUESTIONS.md` — sample viva questions and answers

## Notes
- Passing marks are set to 40 as a project example; update this if your college uses another rule.
- Coordinates are approximate city-center locations.
- This is an educational console application, not a production student information system.
