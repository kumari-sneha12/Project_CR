@echo off
title DriveEase - Premium Car Rental Server
color 0A
echo ============================================
echo    DriveEase Premium Car Rental Website
echo ============================================
echo.
echo Starting Django Development Server...
echo.
echo Website URL: http://127.0.0.1:8000/
echo Admin Panel: http://127.0.0.1:8000/custom-admin/
echo.
echo Press Ctrl+C to stop the server.
echo ============================================
echo.
call .venv\Scripts\activate
python manage.py runserver 8000
pause
