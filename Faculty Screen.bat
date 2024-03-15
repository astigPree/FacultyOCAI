@echo off
rem This is a batch script to run a Python program

rem Set the path to the Python script you want to run
set python_script="main_faculty.py"

rem Check if the Python script exists
if not exist %python_script% (
    echo Python script does not exist: %python_script%
    exit /b
)

rem Run the Python script
echo Running Python script: %python_script%
python %python_script%