# This file contains utility and helper funtions for use

def print_dict_items(d, indent=0):
    for key, value in d.items():
        if isinstance(value, dict):
            print("  " * indent + str(key) + ":")
            print_dict_items(value, indent + 1)
        else:
            print("  " * indent + str(key) + ": " + str(value))