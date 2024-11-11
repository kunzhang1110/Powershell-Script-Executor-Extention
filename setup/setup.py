import re
import json
from pathlib import Path


def escape_path(path: Path, quadruple=False):
    # Escape path by replacing backslashes with double or quadruple backslashes
    escape_char = '\\\\\\\\' if quadruple else '\\\\'
    return str(path).replace("\\", escape_char)


def update_text_file(file_path, pattern, replacement):
    if file_path.exists():
        with file_path.open("r") as file:
            content = file.read()

        updated_content = re.sub(pattern, replacement, content)

        with file_path.open("w") as file:
            file.write(updated_content)

        print(f"{file_path.name} has been updated.")
    else:
        print(f"The file {file_path} does not exist.")


cwd = Path.cwd()
nativeMessagingHost_dir_path = Path.cwd() / "nativeMessagingHost"

# extension_id = input("Enter the extension id: ")
extension_id = "mfcnkmpcgclacngkagjlcgdapnaikomk"

reg_path = nativeMessagingHost_dir_path / "nativeMessagingHost.reg"
json_path = nativeMessagingHost_dir_path / "nativeMessagingHost.json"
py_path = nativeMessagingHost_dir_path / "nativeMessagingHost.py"
bat_path = nativeMessagingHost_dir_path / "run.bat"
ps_path = Path.cwd() / "powerShellScripts" / "download_video.ps1"

reg_replace_pattern = r'(@=)"[^"]*"'
py_replace_pattern = r'(defaultPowershellScriptPath\s*=\s*)"[^"]*"'
update_text_file(reg_path, r'(@=)"[^"]*"',
                 rf'\1"{escape_path(str(json_path), quadruple=True)}"')
update_text_file(
    py_path, r'(defaultPowershellScriptPath\s*=\s*)"[^"]*"',
                rf'\1"{escape_path(str(py_path), quadruple=True)}"')

if json_path.exists():
    with json_path.open("r") as json_file:
        json_parsed = json.load(json_file)

        json_parsed["path"] = str(bat_path)
        json_parsed["allowed_origins"][0] = f'chrome-extension://{extension_id}/'

    with json_path.open("w") as json_file:
        json.dump(json_parsed, json_file, indent=4)

    print(f"{json_path.name} has been updated.")
else:
    print(f"The file {json_path} does not exist.")
