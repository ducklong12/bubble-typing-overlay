@echo off
chcp 65001 >nul
title Quan ly P5 Bubble

echo Đang kiem tra trang thai P5 Bubble...

wmic process where "name='pythonw.exe' and commandline like '%%p5bubble.py%%'" get processid | findstr [0-9] >nul
if %errorlevel% equ 0 (
    echo P5 Bubble dang chay. Dang TAT...
    wmic process where "name='pythonw.exe' and commandline like '%%p5bubble.py%%'" call terminate >nul
    wmic process where "name='python.exe' and commandline like '%%p5bubble.py%%'" call terminate >nul
    echo Da tat thanh cong!
) else (
    echo P5 Bubble chua chay. Dang KHOI DONG...
    start "" pythonw "%~dp0p5bubble.py"
    echo Da khoi dong thanh cong!
)

timeout /t 2 >nul
