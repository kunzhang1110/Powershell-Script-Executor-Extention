import re
import json
from pathlib import Path

"""
This script is used to update the paths in the files nativeMessagingHost.reg, nativeMessagingHost.json, and nativeMessagingHost.py.
"""


def escape_path(path: Path, quadruple=False):
    """ Escape path by replacing backslashes with double or quadruple backslashes"""
    escape_char = '\\\\\\\\' if quadruple else '\\\\'
    return str(path).replace("\\", escape_char)


def update_text_file(file_path, pattern, replacement):
    """ Update a text file by replacing the text found by pattern with the replacement """
    if file_path.exists():
        with file_path.open("r") as file:
            content = file.read()

        updated_content = re.sub(pattern, replacement, content)

        with file_path.open("w") as file:
            file.write(updated_content)

        print(f"{file_path.name} has been updated.")
    else:
        print(f"The file {file_path} does not exist.")


DIR_PATH = Path.cwd() / "nativeMessagingHost"
REG_PATH = DIR_PATH / "nativeMessagingHost.reg"
JSON_PATH = DIR_PATH / "nativeMessagingHost.json"
PY_PATH = DIR_PATH / "nativeMessagingHost.py"
BAT_PATH = DIR_PATH / "run.bat"
PS_PATH = Path.cwd() / "powerShellScripts" / "download_video.ps1"

extension_id = "mfcnkmpcgclacngkagjlcgdapnaikomk"
# extension_id = input("Enter the extension id: ")


REG_REPLACE_PATTERN = r'(@=)"[^"]*"'
PY_REPLACE_PATTERN = r'(defaultPowershellScriptPath\s*=\s*)"[^"]*"'


# Update powershell script path in nativeMessagingHost.py
update_text_file(
    PY_PATH, r'(defaultPowershellScriptPath\s*=\s*)"[^"]*"',
    rf'\1"{escape_path(str(PS_PATH), quadruple=True)}"')
print(f"{PY_PATH.name} has been updated.")

# Update nativeMessagingHost.py path in run.bat
update_text_file(
    BAT_PATH, r'(call\s*python\s*)"[^"]*"',
    rf'\1"{escape_path(str(PY_PATH), quadruple=True)}"')
print(f"{BAT_PATH.name} has been updated.")

# Update run.bat path in nativeMessagingHost.json
with JSON_PATH.open("r") as json_file:
    json_parsed = json.load(json_file)
    json_parsed["path"] = str(BAT_PATH)
    json_parsed["allowed_origins"][0] = f'chrome-extension://{extension_id}/'

with JSON_PATH.open("w") as json_file:
    json.dump(json_parsed, json_file, indent=4)
print(f"{JSON_PATH.name} has been updated.")

# Update nativeMessagingHost.json path in nativeMessagingHost.reg
update_text_file(REG_PATH, r'(@=)"[^"]*"',
                 rf'\1"{escape_path(str(JSON_PATH), quadruple=True)}"')
print(f"{REG_PATH.name} has been updated.")
