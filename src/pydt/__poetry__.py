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
result_data: tuple = data_get(path_workdir, path_python, path_pyScript, path_callBat)
if not result_data[0]:
    print(result_data[1]); sys_exit(1)

filespath: dict[str, str] = result_data[1]
filesdata: dict[str, dict] = result_data[2]
path_base: dict[str, str] = {
    "path_workdir": path_workdir,
    "path_python": path_python,
    "path_pyScript": path_pyScript,
    "path_callBat": path_callBat
}

# 一个 Poetry 的 BUG? 也许. 如果基准目录为磁盘根目录, 就无法找到环境变量中 Git 的可执行文件位置.
if path_callBat.endswith(":/") and params[0].lower() == "new" if params.__len__() else False:
    print("poetry cannot created new project in the root directory of the disk.")
    sys_exit(0)

if not "poetry" in filesdata["config"]["installed"]:
    print("poetry not installed yet.")
    sys_exit(0)

cmd: list[str] = [
    filesdata["config"]["installed"]["poetry"] + " " + " ".join(params).strip()
]

state, result = psrun(
    path_workdir = path_workdir,
    cwd = path_callBat,
    envars = filesdata["envars"]["poetry"],
    cmd = cmd
)
if not state: print(result)