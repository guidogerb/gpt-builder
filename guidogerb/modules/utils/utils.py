from colorama import Fore
from yaml import safe_load, YAMLError

def validate_yaml_file(file: str) -> (bool, str):
    try:
        with open(file, encoding="utf-8") as fp:
            data = safe_load(fp)
    except FileNotFoundError:
        return False, f"The file {Fore.CYAN}`{file}`{Fore.RESET} wasn't found"
    except YAMLError as e:
        return (
            False,
            f"There was an issue while trying to read with your file: {e}",
        )

    return True, f"Successfully validated {Fore.CYAN}`{file}`{Fore.RESET}!"
