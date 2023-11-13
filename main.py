import configparser
import shutil
import sys
import os
from pathlib import Path

from guidogerb.app.app_main import run_guidogerb_gpt

def main():
    """
    Executes the main functionality of the program.

    :return: None
    """
    try:
        # Check if argument is provided
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        else:
            print("Please pass path to the configuration file as an argument.")
            sys.exit()

        # Try reading the config file
        if not os.path.exists(config_file):
            print("Config file does not exist.")
            sys.exit()

        config = configparser.ConfigParser()
        config.read(config_file)

        # Check if 'myconfig' section exists:
        if 'myconfig' not in config.sections():
            print("Missing 'myconfig' section in the config file.")
            sys.exit()

        # Check if 'project_name' and 'clean' options exist in 'myconfig' section
        if not 'PROJECT_NAME' in config['myconfig'] or not 'CLEAN' in config['myconfig']:
            print("Missing 'PROJECT_NAME' or 'CLEAN' in 'myconfig' section of the config file.")
            sys.exit()

        # Check if 'git' section exists:
        if 'git' not in config.sections():
            print("Missing 'git' section in the config file.")
            sys.exit()

        # Check if 'project_name' and 'clean' options exist in 'myconfig' section
        if not 'GIT_PYTHON_GIT_EXECUTABLE' in config['git']:
            print("Missing 'GIT_PYTHON_GIT_EXECUTABLE' in 'git' section of the config file.")
            sys.exit()

        project_name = config.get('myconfig', 'PROJECT_NAME')
        clean = config.getboolean('myconfig', 'CLEAN')
        git = config.get('git','GIT_PYTHON_GIT_EXECUTABLE')

        print(f"Config.ini attributes: {config_file}, Project name: {project_name}, Clean: {clean}, Git: {git}")

        output_dir = f"{os.getcwd()}/output"

        # Check if 'clean' is set to True, if so, delete the output directory
        if clean:
            if os.path.exists(output_dir):
                try:
                    shutil.rmtree(output_dir)
                    print(f"The output directory '{output_dir}' has been cleaned (deleted).")
                except OSError as e:
                    print(f"Error: {e.filename} - {e.strerror}.")
            else:
                print(f"No output directory at '{output_dir}' to clean (delete)!")
        else:
            print("Config file indicates not to clean output directory.")

        # execute guidogerb.app.run_guidogerb_gpt
        run_guidogerb_gpt(True,
                          10,
                          "ai_settings",
                          "prompt_settings",
                          False,
                          True,
                          False,
                          False,
                          False,
                          "memory",
                          "Chrome",
                          True,
                          False,
                          Path("/guidogerb/workspace"),
                          "workspace_directory",
                          False)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()