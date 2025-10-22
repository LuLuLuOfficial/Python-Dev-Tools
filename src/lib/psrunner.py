from subprocess import run # type: ignore
from os import remove

def psrun(
        envars: dict[str, str],
        cmd: list[str] | str,
        path_workdir: str,
        cwd: str
) -> tuple[bool, Exception | None]:
    ps1path: str = f"{path_workdir}/temp/temp.ps1"
    try:
        with open(file=ps1path, mode="w", encoding="utf-8") as File:
            File.write(
                "".join([f"$env:{key} = \"{path_workdir+value if value.startswith("/") else value}\"\n" for key, value in envars.items() if value != ""]) + 
                (cmd if isinstance(cmd, str) else "\n".join(cmd).strip())
            )
    except Exception as E:
        return False, E
    try:
        cmd = [
            "powershell.exe",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            ps1path
        ]
        run(
            cmd,
            cwd=cwd
        )
        remove(ps1path)
    except Exception as E:
        print(E)
        return False, E
    else:
        return True, None