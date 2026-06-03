@echo off
setlocal
cd /d "C:\Users\jondr\projects\deep_search"
echo Starting Tor Search Engine...
echo Ensure Tor Browser is open.
"C:\Users\jondr\projects\deep_search\venv\Scripts\python.exe" "C:\Users\jondr\projects\deep_search\src\tor_search.py"
echo.
echo Press any key to exit...
pause >nul
