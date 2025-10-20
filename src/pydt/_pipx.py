from sys import argv as params, exit, executable
from os.path import exists as pathexist
from os import mkdir
from json import load as JSONload, dump as JSONdump

def WriteConfig(file: str, obj: dict):
    try:
        with open(file=file, mode="w", encoding="utf-8") as File:
            JSONdump(obj=Envar, fp=File, indent=4)
    except Exception as E:
        print(f"Write To ConfigFile Failed: {file}")
        return False
    else:
        return True

CallFrom: str = params[0]
CallCmd: list[str] = params[1:]

Envar: dict[str, str] = { # Env Variable
    "PIPX_HOME": "../../pipx/home",
    "PIPX_GLOBAL_HOME": "",
    "PIPX_BIN_DIR": "../../pipx/scripts",
    "PIPX_GLOBAL_BIN_DIR": "",
    "PIPX_MAN_DIR": "../../pipx/man", # manual pages
    "PIPX_GLOBAL_MAN_DIR": "",
    "PIPX_SHARED_LIBS": "",
    "PIPX_DEFAULT_PYTHON": executable,
    "PIPX_FETCH_MISSING_PYTHON": "",
    "PIPX_USE_EMOJI": "",
    "PIPX_HOME_ALLOW_SPACE": ""
}
LstEnvar: list[str] = list(Envar); LstEnvar.sort()

path_ConfigLucas: str = "../../pipx/config-lucas.json"
path_pipxpyz: str = "../../pipx-app.pyz"

# --------------------------------------------------
# 读取并检查配置文件
# --------------------------------------------------
try:
    if not pathexist(path_ConfigLucas):
        raise FileExistsError
    with open(file=path_ConfigLucas, mode="r", encoding="utf-8") as File:
        _Envar: dict[str, str] = JSONload(fp=File)
        _LstEnvar: list[str] = list(_Envar); _LstEnvar.sort()
        if LstEnvar != _LstEnvar: raise ValueError
        _Envar["PIPX_DEFAULT_PYTHON"] = executable
except Exception as E:
    print(E)
    WriteConfig(file=path_ConfigLucas, obj=Envar)
else:
    Envar = _Envar

# --------------------------------------------------
# 检查并执行命令(config-lucas接管)
# --------------------------------------------------
if " ".join(CallCmd).strip().lower().startswith("config-lucas"):
    if all([
        CorrectLen:=(CallCmd.__len__() in [2, 3]),
        CorrectParam:=(CallCmd[1] in LstEnvar if CorrectLen else True)
    ]): # Param Correct
        # get mode
        if CallCmd.__len__() == 2:
            print(f"{CallCmd[1]} = {Envar[CallCmd[1]]}")
            exit(0)

        # set mode
        if not pathexist(CallCmd[2]): # 指定的文件夹路径不存在
            try:
                mkdir(CallCmd[2])
            except Exception as E:
                print(f"Create Folder Failed: {CallCmd[2]}")
                exit(1)
        Envar[CallCmd[1]] = CallCmd[2]
        WriteConfig(file=path_ConfigLucas, obj=Envar)
    else: # Param Error
        if not CorrectLen:
            print(f"Unexpected Parameters: pipx {" ".join(CallCmd).strip()}, Expected: pipx config-lucas [--Envar] [--Path]"); exit(2)
        if not CorrectParam:
            print(f"Incorrect Parameters: {CallCmd[1]}, Expected: {LstEnvar}"); exit(2)
else:
    import subprocess
    env: str = "".join([f"$env:{key} = \"{value}\"\n" for key, value in Envar.items() if value != ""])
    psScript: str = env+" ".join([executable, path_pipxpyz] + CallCmd).strip()
    subprocess.run(["powershell", "-NoProfile", "-Command", psScript])