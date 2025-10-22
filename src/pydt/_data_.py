from os.path import exists as path_exists
from src.lib import config_read, config_write

def data_get(path_workdir: str, path_python: str, path_pyScript: str, path_callBat: str) -> tuple[bool, dict[str, str], dict[str, dict|str]]:
    filespath: dict[str, str] = {
        "config": "_Config/config.json",
        "pkglist": "_Config/pkglist.json",
        "envars": "_Config/envars.json",
    }
    filesdata: dict[str, dict|str] = {
        "config": {
            "urls": {
                "python_standalone": "",
                "pyenv_win": "",
                "pipx": ""
            },
            "path": {
                "python_standalone": f"{path_workdir}/python_standalone/python.exe",
                "pyenv_win": f"{path_workdir}/pyenv_win/pyenv-win/bin/pyenv.bat",
                "pipx": f"{path_workdir}/pipx/pipx-app.pyz"
            },
            "installed": {}
        },
        "pkglist": ["poetry"],
        "envars": {
            "pipx": {
                "PIPX_HOME": "./pipx/home",
                "PIPX_GLOBAL_HOME": "",
                "PIPX_BIN_DIR": "./pipx/scripts",
                "PIPX_GLOBAL_BIN_DIR": "",
                "PIPX_MAN_DIR": "./pipx/man",
                "PIPX_GLOBAL_MAN_DIR": "",
                "PIPX_SHARED_LIBS": "",
                "PIPX_DEFAULT_PYTHON": "./python_standalone/python.exe",
                "PIPX_FETCH_MISSING_PYTHON": "",
                "PIPX_USE_EMOJI": "",
                "PIPX_HOME_ALLOW_SPACE": ""
            },
            "poetry": {
                "POETRY_CONFIG_DIR": "./pipx/home/venvs/poetry/pypoetry/config",
                "POETRY_DATA_DIR": "./pipx/home/venvs/poetry/pypoetry",
                "POETRY_CACHE_DIR": "./pipx/home/venvs/poetry/pypoetry/cache",
                "POETRY_VIRTUALENVS_IN_PROJECT": "true"
            },
            "pyenv-win": {
                "PYENV": "/pyenv_win",
                "PYENV_HOME": "/pyenv_win",
                "PYENV_ROOT": "/pyenv_win",
                "HTTP_PROXY": "http://127.0.0.1:7890",
                "HTTPS_PROXY": "https://127.0.0.1:7890"
            }
        },
    }

    # read file
    for key, path in filespath.items():
        if not path_exists(path):
            state, result = config_write(path, filesdata[key])
            if not state: return False, result, None

        state, result = config_read(path)
        if not state: return False, result, None

        filesdata[key] = result
    
    return True, filespath, filesdata