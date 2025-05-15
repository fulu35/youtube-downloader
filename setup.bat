@echo off
REM Python kurulumu kontrol ediliyor
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python bulunamadı.
    echo Lütfen resmi web sitesinden Python'u kurunuz: https://www.python.org/downloads/
    pause
) ELSE (
    echo Python zaten kurulu.
    pause
) 