import pathlib


def check_valid_csv(filename):
    return True if filename != '' and pathlib.Path(filename).suffix == '.csv' and filename is not None else False
    