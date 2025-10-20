from sys import argv as params, exit, executable
from os.path import exists as pathexist
from json import load as JSONload
import subprocess
from pathlib import Path

environments: str | dict[str, str] = f"{str(Path(__file__).parent.parent.resolve()).replace('\\', '/')}/environments.json"
path_script: str = f"{str(Path(__file__).parent.resolve()).replace('\\', '/')}/_poetry.exe"
# --------------------------------------------------
# 读取并检查配置文件
# --------------------------------------------------
if pathexist(environments):
    try:
        with open(file=environments, mode="r", encoding="utf-8") as File:
            environments: dict[str, str] = JSONload(fp=File)
    except Exception as E:
        print(E)
        exit(1)
# --------------------------------------------------
# 执行命令
# --------------------------------------------------
    env: str = "".join([f"$env:{key} = \"{value}\"\n" for key, value in environments.items() if value != ""])
    psScript: str = env+" ".join([path_script] + params[1:]).strip()
else:
    psScript: str = " ".join([path_script] + params[1:]).strip()

subprocess.run(["powershell", "-NoProfile", "-Command", psScript])