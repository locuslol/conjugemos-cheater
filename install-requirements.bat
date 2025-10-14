@echo off
echo ================================================
echo   Installing required Python packages...
echo ================================================
echo.

REM Ensure pip is up to date
python -m pip install --upgrade pip

REM Install all dependencies
pip install pyautogui pytesseract pillow google-genai pyperclip keyboard

echo.
echo ================================================
echo   Installation complete!
echo ================================================
pause