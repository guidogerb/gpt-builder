import os

def load_queue(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return set(file.read().splitlines())
    return set()
