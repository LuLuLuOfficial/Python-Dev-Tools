from subprocess import run # type: ignore
from os import remove

def psrun(envars: dict[str, str], cmd: str) -> tuple[bool, Exception | None]:
    ps1path: str = "temp/temp.ps1"
    # return
    try:
        with open(file=ps1path, mode="w", encoding="utf-8") as File:
            File.write("".join([f"$env:{key} = \"{value}\"\n" for key, value in envars.items() if value != ""]) + cmd)
    except Exception as E:
        return False, E

    try:
        run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps1path], check=True)
        remove(ps1path)
    except Exception as E:
        return False, E
    else:
        return True, None