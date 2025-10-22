from sys import argv as sys_argv
from sys import exit as sys_exit, executable as path_python
from src.lib import config_read, config_write, cmd_help, cmd_config, cmd_install, cmd_list, cmd_uninstall, cmd_debug, psrun
from os import getcwd
from os.path import exists as path_exists
from src.pydt._data_ import data_get

# Path
path_workdir: str = getcwd().replace("\\", "/") # 工作区基准路径
path_python: str = path_python.replace("\\", "/") # python可执行文件路径
path_pyScript: str = sys_argv[0].replace("\\", "/") # python脚本文件路径
path_callBat: str = sys_argv[1].replace("\\", "/")[:-1] # bat脚本文件被调用位置

# params
params: list[str] = sys_argv[2:]

# data
result_data: tuple[bool, dict[str, str], dict[str, dict|str]] = data_get(path_workdir, path_python, path_pyScript, path_callBat)
if not result_data[0]: print(result_data[1]); sys_exit(1)

filespath: dict[str, str] = result_data[1]
filesdata: dict[str, dict] = result_data[2]
path_base: dict[str, str] = {
    "path_workdir": path_workdir,
    "path_python": path_python,
    "path_pyScript": path_pyScript,
    "path_callBat": path_callBat
}

# command
match params[0].lower() if params.__len__() != 0 else "help":
    case "help":
        cmd_help("all")
    case "list":
        cmd_list(path_base, filespath, filesdata, params[1:])
    case "config":
        cmd_config(path_base, filespath, filesdata, params[1:])
    case "install":
        cmd_install(path_base, filespath, filesdata, params[1:])
    case "uninstall":
        cmd_uninstall(path_base, filespath, filesdata, params[1:])
    case "debug":
        cmd_debug(path_base, filespath, filesdata, params[1:])
    case _:
        cmd_help("all")