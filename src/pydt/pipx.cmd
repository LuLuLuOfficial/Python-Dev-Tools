@echo off
set "CMD_DIR=%~dp0"
powershell -Command "Set-Location -LiteralPath '%CMD_DIR%'; & '..\..\python.exe' '_pipx.py' $args" %*