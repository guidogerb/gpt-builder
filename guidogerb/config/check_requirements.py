import os
import sys
import argparse
from distutils.version import LooseVersion
from importlib.metadata import version as get_version, PackageNotFoundError

def main(arguments):
    """
    Check if required packages are installed and their versions match with the specified versions.

    :param arguments: Command-line arguments passed to the script.
                      Should include the path to the file containing the list of required packages.
    :return: None

    :raises: SystemExit: If the file specified in `arguments` doesn't exist or is not readable.

    :example:
    >>> main(parser.parse_args(['--file', 'requirements.txt']))
    All packages are installed.
    """

    if os.path.exists(arguments.file) and os.access(arguments.file, os.R_OK):
        with open(arguments.file, "r") as f:
            required_packages = [
                line.split("#")[0].strip() for line in f
                if line.strip() and not line.strip().startswith('#')
            ]
    else:
        print(f"Cannot access the file: {arguments.file}")
        sys.exit(2)

    missing_packages = []
    print(f"Checking {len(required_packages)} packages:")
    for required_package in required_packages:
        print(f"Checking {required_package}...")
        if '==' in required_package:
            package_name, required_version = required_package.split('==')
        else:
            package_name = required_package
            required_version = None

        try:
            installed_version = get_version(package_name)
        except PackageNotFoundError:
            missing_packages.append(required_package)
            continue

        if required_version:
            if LooseVersion(installed_version) != LooseVersion(required_version):
                missing_packages.append(required_package)

    if missing_packages:
        print("Missing or wrong version packages:")
        print(", ".join(missing_packages))
        sys.exit(1)
    else:
        print("All packages are installed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check requirements file against installed packages.')
    parser.add_argument('file', type=str, help='Path to the requirements file.')
    arguments = parser.parse_args()
    main(arguments)