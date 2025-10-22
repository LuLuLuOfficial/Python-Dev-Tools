from typing import Literal # type: ignore
from sys import executable as pyth_python
from os.path import exists as path_exists
from .config_rw import config_read, config_write
from .psrunner import psrun

def cmd_help(level: Literal["all", "config", "install", "uninstall"]):
    match level:
        case "all":
            print("\n".join([
                "Warm Reminder:",
                "\tPlease do not manually modify or delete any pydt files unless you really understand what they do.",
                "",
                "Command:",
                "\tpydt config \"KEY\"",
                "\tpydt config \"KEY\" \"VALUE\"",
                "\tpydt install \"PKG\"",
                "\tpydt uninstall \"PKG\""
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

def cmd_list(path_base: dict, filespath: dict, filesdata: dict, args: list[str]):
    # args: params after "list"

    pkglist: list[str] = filesdata["pkglist"]

    match args.__len__():
        case 0: # print mode
            print("Available Packages:")
            for pkg in pkglist: print("\t" + pkg)
        case _: # unexpected
            cmd_help("list")

def cmd_config(path_base: dict, filespath: dict, filesdata: dict, args: list[str]):
    # args: params after "config"

    config: dict = filesdata["config"]

    match args.__len__():
        case 0: # help mode
            cmd_help("config")
        case 1: # read mode
            pass
        case 2: # write mode
            pass
        case _: 
            cmd_help("config")

def cmd_install(path_base: dict, filespath: dict, filesdata: dict, args: list[str]):
    # args: params after "install"

    config: dict = filesdata["config"]
    pkglist: list[str] = filesdata["pkglist"]
    envars: dict[str, dict[str, str]] = filesdata["envars"]

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
                f"{config["path"]["python_standalone"]} {config["path"]["pipx"]} install poetry"
            ]

            state, result = psrun(
                envars["pipx"] | envars["poetry"],
                cmd,
                path_base["path_workdir"],
                path_base["path_callBat"]
            )

            if not state or not path_exists(f"{path_base["path_workdir"]}{envars["pipx"]["PIPX_BIN_DIR"]}/poetry.exe"):
                print("poetry install failed.")
                if not state: print(result)
                return

            config["installed"]["poetry"] = f"{path_base["path_workdir"]}{envars["pipx"]["PIPX_BIN_DIR"]}/poetry.exe"
            config_write(filespath["config"], filesdata["config"])

def cmd_uninstall(path_base: dict, filespath: dict, filesdata: dict, args: list[str]):
    # args: params after "install"

    config: dict = filesdata["config"]
    pkglist: list[str] = filesdata["pkglist"]
    envars: dict[str, dict[str, str]] = filesdata["envars"]

    match args.__len__():
        case 0: # help mode
            cmd_help("install"); return
        case 1: # uninstall mode
            if not args[0] in config["installed"]: print("Requested Package Is Not Installed Yet."); return
        case _: # unexpected
            cmd_help("install"); return
    
    # uninstall mode
    match args[0]:
        case "poetry":
            cmd: list[str] = [
                f"{config["path"]["python_standalone"]} {config["path"]["pipx"]} uninstall poetry"
            ]

            state, result = psrun(
                envars["pipx"] | envars["poetry"],
                cmd,
                path_base["path_workdir"],
                path_base["path_callBat"]
            )

            if not state or path_exists(f"{path_base["path_workdir"]}{envars["pipx"]["PIPX_BIN_DIR"]}/poetry.exe"):
                print("poetry uninstall failed.")
                if not state: print(result)
                return

            config["installed"].pop("poetry")
            config_write(filespath["config"], filesdata["config"])

def cmd_update(path_base: dict, filespath: dict, filesdata: dict, args: list[str]):
    # args: params after "install"

    config: dict = filesdata["config"]
    pkglist: list[str] = filesdata["pkglist"]
    envars: dict[str, dict[str, str]] = filesdata["envars"]

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

def cmd_debug(path_base: dict, filespath: dict, filesdata: dict, args: list[str]):
    # args: params after "debug"

    config: dict = filesdata["config"]
    pkglist: list[str] = filesdata["pkglist"]
    envars: dict[str, dict[str, str]] = filesdata["envars"]
    
    if args.__len__() == 0: return
    match args[0]:
        case "pipx":
            cmd: list[str] = [
                f"{config["path"]["python_standalone"]} {config["path"]["pipx"]} {" ".join(args[1:])}"
            ]

            state, result = psrun(
                envars["pipx"] | envars["poetry"],
                cmd,
                path_base["path_workdir"],
                path_base["path_callBat"]
            )

            if not state: print(result); return
        case "poetry":
            cmd: list[str] = [
                f"{config["path"]["python_standalone"]} {config["path"]["pipx"]} {" ".join(args[1:])}"
            ]

            state, result = psrun(
                envars["pipx"] | envars["poetry"],
                cmd,
                path_base["path_workdir"],
                path_base["path_callBat"]
            )

            if not state: print(result); return