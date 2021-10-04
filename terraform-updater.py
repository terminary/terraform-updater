# A simple updater for terraform

import json
import os
import platform
import re
import subprocess
import sys
import urllib.request
import zipfile

## CONFIG ##
INSTALL_DIR = {
    "Windows": os.path.abspath("C:/program files/terraform/"),
    "Linux": os.path.abspath("/usr/bin/")
}
# Exit early if already on latest version
REDOWNLOAD_SAME_VER = True
## END CONFIG ##

## ERRORS ##
PERMISSION_DENIED = 1
INSTALL_NOT_FOUND = 2
DOWNLOAD_ERROR = 3
UNKNOWN_ERROR = 4
## END ERRORS ##

def get_install_info(bin_path):
    ver_text = subprocess.run([binary_path, "version"], text=True, capture_output=True).stdout
    installed_version = re.search(r"\d+\.\d+\.\d+", ver_text).group()
    machine = re.search(r"(linux|windows)_\w+", ver_text).group()
    return installed_version, machine

print("\nterraform-updater\n=================")

print("Checking installed version...")
system = platform.system()
binary_path = os.path.join(INSTALL_DIR[system], "terraform")
binary_name = f"{binary_path}{'.exe' if system == 'Windows' else ''}"
if not os.path.exists(binary_name):
    print(f"ERROR: The install could not be found at {binary_name}")
    sys.exit(INSTALL_NOT_FOUND)
installed_version, machine = get_install_info(binary_path)
print(f"    {installed_version}")
print(f"    {machine}")

print("Getting latest terraform version number...")
response = urllib.request.urlopen("https://checkpoint-api.hashicorp.com/v1/check/terraform").read()
json_dict = json.loads(response)
current_version = json_dict["current_version"]
print(f"    {current_version}")

if not REDOWNLOAD_SAME_VER and installed_version == current_version:
    print("Already up to date.\n")
    sys.exit(0)

print("Backing up current binary...")
backup_name = f"{binary_path}_{installed_version}{'.exe' if system == 'Windows' else ''}"
try:
    os.replace(binary_name, backup_name)
except PermissionError as e:
    print(f"ERROR: {e}\n\nTry running the script again with admin privilages.\n")
    sys.exit(PERMISSION_DENIED)
print(f"    {backup_name}")
print("    Done")

print("Downloading latest package...")
url_base = json_dict["current_download_url"]
filename = f"terraform_{current_version}_{machine}.zip"
url = f"{url_base}/{filename}"
print(f"    {url}")
try:
    # Using urllib instead of requests to stick to just standard libraries
    package = urllib.request.urlopen(url).read()
except:
    print("An error occurred while downloading. Please try again.")
    sys.exit(DOWNLOAD_ERROR)
try:
    with open(filename, 'wb') as outfile:
        outfile.write(package)
except PermissionError as e:
    print(f"ERROR: {e}\nPermission denied to save file in pwd.\n\nTry running the script again with admin privilages.\n")
    sys.exit(PERMISSION_DENIED)
print("    Done")

print("Extracting archive...")
try:
    with zipfile.ZipFile(filename) as archive:
        archive.extractall(INSTALL_DIR[system])
    if system == 'Linux':
        print("    Making executable...")
        subprocess.run(["sudo", "chmod", "+x", f"{INSTALL_DIR[system]}/terraform"])
except PermissionError as e:
    print(f"ERROR: {e}\n\nTry running the script again with admin privilages.\n")
    sys.exit(PERMISSION_DENIED)
print(f"    Done")

print("Cleaning up...")
os.remove(filename)
print("    Done")

ver, _ = get_install_info(binary_path)
if os.path.exists(binary_name) and ver == current_version:
    print("Successfully completed.")
    sys.exit(0)
else:
    print("An error occurred. Please try again.")
    sys.exit(UNKNOWN_ERROR)
