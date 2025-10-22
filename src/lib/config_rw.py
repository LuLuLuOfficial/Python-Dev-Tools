from os.path import exists as path_exists
from json import load as json_load, dump as json_dump

def config_read(file: str):
    if not path_exists(file):
        return False, f"File Not Exist: {file}"
    data: dict = {}
    try:
        with open(file=file, mode="r", encoding="utf-8") as File:
            data = json_load(File)
    except Exception as E:
        return False, f"Read Config Error[{file}]: {E}"
    else:
        return True, data

def config_write(file: str, data: dict | list):
    try:
        with open(file=file, mode="w", encoding="utf-8") as File:
            json_dump(obj=data, fp=File, indent=4, ensure_ascii=False)
    except Exception as E:
        return False, f"Write Config Error[{file}]: {E}"
    else:
        return True, data