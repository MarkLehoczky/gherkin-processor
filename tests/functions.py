from os import listdir, remove
from os.path import isfile, join


def empty_output_directory():
    output_dir = "tests/data/output"
    for item in listdir(output_dir):
        item_path = join(output_dir, item)
        if isfile(item_path):
            remove(item_path)
