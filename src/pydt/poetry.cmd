@echo off
set "CMD_DIR=%~dp0"
for %%I in ("%CMD_DIR%\..\..") do set "PYTHON_EXE=%%~fI\python.exe"
set "POETRY_SCRIPT=%CMD_DIR%_poetry.py"
powershell -Command "& '%PYTHON_EXE%' '%POETRY_SCRIPT%' $args" %*