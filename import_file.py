import json
from os.path import exists


def import_file(list_automatons):
    """Ask the user for a file path to get the content of the file which contains the JSON of an automaton et add the
    file's content to list_automations"""
    print("You chose to import a automaton from a file. That file must be in JSON. You can have more informations on "
          "the format in the documentation")
    file_exists = False
    file = None
    while not file_exists:  # while the user enter a non-existent file
        path_file = input("Enter the path of the file you want to import :  (stop to quit)")
        if path_file == "stop":
            return 0
        if exists(path_file):
            file = open(path_file, "r")
            file_exists = True
        else:
            print("This file doesn't exist")
    try:
        data = json.load(file)
        list_automatons.append(data)  # add the new automaton to list_automatons
    except json.JSONDecodeError:  # If the JSON file is not correct
        print("File not readable. Verify the format, the file must be in JSON.")
