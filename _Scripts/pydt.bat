@echo off
cd /d "%~dp0.."
"./python_standalone/python.exe" "./src/pydt/__main__.py" %*