from sys import argv as sys_argv
from sys import exit as sys_exit, executable as path_python
from src.lib import config_read, config_write, cmd_help, cmd_config, cmd_install, cmd_list, cmd_uninstall
from os import getcwd
from os.path import exists as pathExists

def checkdata():
    changed_config: bool = False
    changed_envars: bool = False
    if python_standalone:=filesdata["config"]["path"]["python_standalone"] == "" or not pathExists(python_standalone):
        filesdata["config"]["path"]["python_standalone"] = (path_python).replace("\\", "/")
        changed_config = True
    if pyenv_win:=filesdata["config"]["path"]["pyenv_win"] == "" or not pathExists(pyenv_win):
        filesdata["config"]["path"]["pyenv_win"] = (workdir + "/pyenv_win").replace("\\", "/")
        changed_config = True
    if pipx:=filesdata["config"]["path"]["pipx"] == "" or not pathExists(pipx):
        filesdata["config"]["path"]["pipx"] = (workdir + "/pipx/pipx-app.pyz").replace("\\", "/")
        changed_config = True
    
    if PIPX_DEFAULT_PYTHON:=filespath["envars"]["pipx"]["PIPX_DEFAULT_PYTHON"] == "" or not pathExists(PIPX_DEFAULT_PYTHON):
        filespath["envars"]["pipx"]["PIPX_DEFAULT_PYTHON"] == path_python
        changed_envars = True

    if changed_config: config_write(filespath["config"], data=filesdata["config"])
    if changed_envars: config_write(filespath["envars"], data=filesdata["config"])

# params
workdir: str = getcwd()
path_python: str = path_python
pyScriptPath: str = sys_argv[0]
params: list[str] = sys_argv[1:]

filespath: dict[str, str] = {
    "config": "_Config/config.json",
    "pkglist": "_Config/pkglist.json",
    "envars": "_Config/envars.json",
}
filesdata: dict[str, dict|str] = {
    "config": {},
    "pkglist": [],
    "envars": {},
}

# read file
for key, path in filespath.items():
    state, filesdata[key] = config_read(path)
    if not state: print(filesdata[key]); sys_exit(1)
else:
    checkdata()

match params[0].lower() if params.__len__() != 0 else "help":
    case "help":
        cmd_help("all")
        sys_exit(0)
    case "list":
        cmd_list(filesdata["pkglist"], params[1:])
        sys_exit(0)
    case "config":
        cmd_config(filesdata["config"], params[1:])
        sys_exit(0)
    case "install":
        cmd_install(filesdata["config"], filesdata["pkglist"], filesdata["envars"], params[1:])
        sys_exit(0)
    case "uninstall":
        cmd_uninstall(filesdata["config"], filesdata["pkglist"], filesdata["envars"], params[1:])
        sys_exit(0)
    case _:
        cmd_help("all")
        sys_exit(0)