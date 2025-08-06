@echo off
cd /d "C:\Users\Alex\Desktop\peladas-manager\backend"
call ..\.venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
