@echo off
set "RUN_DIR=%CD%"
cd /d "%~dp0.."
"./python_standalone/python.exe" -m src.pydt.__poetry__ "%RUN_DIR%." %*