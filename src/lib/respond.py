from typing import Literal # type: ignore
from src.lib import config_read
from src.lib import psrun
from sys import executable as pyth_python

def cmd_help(level: Literal["all", "config", "install", "uninstall"]):
    match level:
        case "all":
            print("\n".join([
                "Warm Reminder: Please do not manually modify or delete any pydt files unless you really understand what they do."
                "pydt config",
                "pydt install",
                "pydt uninstall"
            ]))
        case "list":
            pass
        case "config":
            print("pydt config KEY VALUE")
        case "install":
            pass
        case "uninstall":
            pass
        case "update":
            pass

def cmd_list(pkglist: list[str], args: list[str]):
    # args: params after "list"
    match args.__len__():
        case 0: # print mode
            print("Available Packages:")
            for pkg in pkglist: print("\t" + pkg)
        case _: # unexpected
            cmd_help("list")

def cmd_config(config: dict, args: list[str]):
    # args: params after "config"
    match args.__len__():
        case 0: # help mode
            cmd_help("config")
        case 1: # read mode
            pass
        case 2: # write mode
            pass
        case _: 
            cmd_help("config")

def cmd_install(config: dict, pkglist: list[str], envars: dict[str, str], args: list[str]):
    # args: params after "install"
    match args.__len__():
        case 0: # help mode
            cmd_help("install"); return
        case 1: # install mode
            if not args[0] in pkglist: print("Requested Package Is Not Supported Or Not Exist."); return
            if args[0] in config["installed"]: print("Requested Package Already Installed, Use \"pytd update [pkg]\" Or \"pytd update *\" To Update."); return
        case _: # unexpected
            cmd_help("install"); return
    
    # install mode
    match args[0]:
        case "poetry":
            cmd: list[str] = [
                f"{config["path"]["python_standalone"]} {config["path"]["pipx"]} install poetry",
                f"{envars["pipx"]["PIPX_BIN_DIR"]}/poetry config virtualenvs.in-project true"
            ]

def cmd_uninstall(pkglist: list[str], args: list[str]):
    # args: params after "install"
    match args.__len__():
        case 0: # help mode
            cmd_help("install")
        case 1: # uninstall mode
            pass
        case _: # unexpected
            cmd_help("install")

def cmd_update(config: dict, pkglist: list[str], envars: dict[str, str], args: list[str]):
    # args: params after "install"
    match args.__len__():
        case 0: # help mode
            cmd_help("update")
        case 1: # install mode
            if args[0] == "*":
                for pkg in config["installed"]: cmd_update(config, pkglist, envars, pkg)
                return
            if not args[0] in config["installed"]:
                print("Requested Package Not Installed Yet, Use \"pytd install [pkg]\" To Install.")
                return
        case _: # unexpected
            cmd_help("update")