#!/usr/bin/env bash


function find_python_command() {

    # Define the minimum supported Python version.
    minver=(3 12)

    # Try to find 'python' command
    python_cmd=""
    if command -v python &> /dev/null
    then
        python_cmd="python"
    # If 'python' not found, try to find 'python3' command
    elif command -v python3 &> /dev/null
    then
        python_cmd="python3"
    fi

    # No Python command found.
    if [[ -z $python_cmd ]]
    then
        echo "Python not found. Please install Python 3.12.0 or later."
        exit 1
    fi

    # Parse the python version and compare with the minimum version.
    IFS="." read -a ver <<< `$python_cmd -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'`
    for i in "${!ver[@]}"
    do
        if (( "${ver[i]}" < "${minver[i]}" ))
        then
            echo "Unsupported Python version. Please upgrade to Python 3.12.0 or later."
            exit 1
        elif (( "${ver[i]}" > "${minver[i]}" ))
        then
            break
        fi
    done

    echo "$python_cmd"
}

PYTHON_CMD=$(find_python_command)

function install_package_if_needed {
    $PYTHON_CMD -c "import $1" &> /dev/null || (echo "$1 not found, installing..." && pip install $1)
}

# Check if $PYTHON_CMD version is 3.12 or higher
if $PYTHON_CMD -c "import sys; sys.exit(sys.version_info < (3, 12))"; then

    # Check the Python and pip version is installed
    install_package_if_needed importlib_metadata

    # Check if all required packages are installed
    $PYTHON_CMD "guidogerb/config/check_requirements.py" "guidogerb/config/requirements.txt"

    # If any requirement is not met
    if [ $? -eq 1 ]; then
        # Install the missing packages from requirements.txt
        echo Installing required packages...
        $PYTHON_CMD -m pip install -r guidogerb/config/requirements.txt
    fi

    # Check if installation was successful
    if [ $? -ne 0 ]; then
        echo "An error occurred while installing Python packages. Please check the errors displayed above."
        exit 1
    fi

    # Run the main script with all arguments
    $PYTHON_CMD -m main config.ini

    # Wait for user input
    read -p "Press any key to continue..."
else
    # Abort and print error message if Python 3.12 or higher is not installed
    echo "Python 3.12 or higher is required to run GuidoGerb-GPT."
fi
