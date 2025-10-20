from os.path import exists as path_exists
from json import load as json_load, dump as json_dump

def read(file: str):
    if not path_exists(file):
        return False, f"File Not Exist: {file}"
    data: dict = {}
    try:
        with open(file=file, mode="r", encoding="utf-8") as File:
            data = json_load(File)
    except Exception as E:
        return False, f"Read Config Error[{pydtconfig_path}]: {E}"
    else:
        return True, data