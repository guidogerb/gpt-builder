@echo off
SETLOCAL EnableDelayedExpansion

python -c "import importlib_metadata" >nul 2>&1
if errorlevel 1 (
    echo importlib_metadata not found, installing...
    pip install importlib_metadata
    if errorlevel 1 (
        echo Failed to install importlib_metadata, please check your Python and pip installations.
        exit /B
    )
)

:: Define the minimum supported Python version.
set "minver=3.12"

:: Check if the PYTHON3_12_0 environment variable exists
if defined PYTHON3_12_0 (
    :: If it exists, use it as the path to the Python executable
    set "python_cmd=%PYTHON3_12_0%\python.exe"
) else (
    :: If it is not set, output error message and exit
    echo "You must set an environment variable PYTHON3_12_0 to the path of the Python 3.12.0 root directory."
    goto :eof
)

:: Get installed Python version
for /f "tokens=* delims= " %%a in ('!python_cmd! -c "import sys; print(str(sys.version_info[0]) + '.' + str(sys.version_info[1]))"') do (
	set "ver=%%a"
)


:: Compare the installed Python version with the minimum version.
(for %%v in (!ver!) do if %%v LSS !minver! (
	echo Unsupported Python version. Please upgrade to Python 3.12.0 or later.
	goto :eof
	))

:: Check if all required packages are installed
for /f "tokens=* delims= " %%a in ('!python_cmd! guidogerb/config/check_requirements.py guidogerb/config/requirements.txt') do (
    if %%a=='1' (
	    echo Installing missing packages...
        set "pip_status=1"
        :: If any requirement is not met, attempt to install the missing packages from `requirements.txt`
        !python_cmd! -m pip install -r guidogerb/config/requirements.txt || goto :pip_error
	)
)

:: Run the main script with all arguments
!python_cmd! -m main config.ini

:: Pause for user input before closing the window
pause

:: End of file reached, exit the script
goto :eof

:pip_error
:: If pip install fails, output an error message
echo An error occurred while installing Python packages. Please check the errors displayed above.
goto :eof

:eof