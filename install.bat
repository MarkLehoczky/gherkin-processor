@echo off
set PACKAGE_NAME=gherkin-processor


:: Check if pip is installed; otherwise exit with an error message
pip --version >nul 2>&1

if %errorlevel% neq 0 (
    echo ERROR: pip is not installed!
    echo Please install pip before running this script.
    echo.
    echo.
    echo.
    echo Exiting...
    timeout /t 5 /nobreak >nul
    exit /b 1
)

:: Check if the package is already installed
pip show %PACKAGE_NAME% >nul 2>&1

:: If the package is installed, upgrade it; otherwise install it
if %errorlevel% equ 0 (
    echo Package '%PACKAGE_NAME%' is already installed. Upgrading package...
    echo.
    pip install --quiet --upgrade --compile .

    :: Check if pip upgrade was successful
    if %errorlevel% equ 0 (
        echo.
        echo Upgrade completed successfully!
    ) else (
        echo.
        echo ERROR: Upgrade failed!
        echo.
        echo.
        echo.
        echo Exiting...
        timeout /t 5 /nobreak >nul
        exit /b 2
    )
) else (
    echo Installing package...
    echo.
    pip install --compile .

    :: Check if pip installation was successful
    if %errorlevel% equ 0 (
        echo.
        echo Installation completed successfully!
        echo.
        echo.
        echo.
        echo Exiting...
        timeout /t 5 /nobreak >nul
        exit
    ) else (
        echo.
        echo ERROR: Installation failed!
        echo.
        echo.
        echo.
        echo Exiting...
        timeout /t 5 /nobreak >nul
        exit /b 2
    )
)
