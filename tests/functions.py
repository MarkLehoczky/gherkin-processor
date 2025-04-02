from os import listdir, makedirs, remove
from os.path import exists, isfile, join


def empty_output_directory():
    output_dir = "tests/data/output/"
    if not exists(output_dir):
        makedirs(output_dir)
    for item in listdir(output_dir):
        item_path = join(output_dir, item)
        if isfile(item_path):
            remove(item_path)
