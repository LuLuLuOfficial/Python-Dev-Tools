from sys import argv as sys_argv
from sys import exit as sys_exit
from src.lib import config_read

pyScriptPath: str = sys_argv[0]
print(pyScriptPath)
params: list[str] = sys_argv[1:]

# read config
pydtconfig_path: str = "_Config/config.json"
pydtconfig: dict = {}
state, pydtconfig = config_read(pydtconfig_path)
if not state:
    print(pydtconfig)
    sys_exit(1)

def help():
    print("\n".join([
        "pydt config",
        "pydt install",
        "pydt uninstall"
    ]))

def config(args: list[str]):
    # args: params after "config"
    match args.__len__():
        case 0: # help mode
            pass
        case 1: # read mode
            pass
        case 2: # write mode
            pass

match params[0] if params.__len__() != 0 else "help":
    case "help":
        help()
        sys_exit(0)
    case "config":
        config(params[1:])
        sys_exit(0)
    case "install":
        pass
    case "uninstall":
        pass
    case _:
        pass