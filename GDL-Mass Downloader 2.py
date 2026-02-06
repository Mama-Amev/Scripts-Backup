# Modified version of the original script that downloads 
# multiple tags at once.

import subprocess
import os
import sys
import traceback
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = r"PATH\TO\FOLDER"
LOG_DIR = os.path.join(BASE_DIR, "Logs")

FOLDERS = [
    "Folder Name",
    "Folder Name",
    "Folder Name",
]

GALLERY_CMD = "gallery-DL Command"

def ensure_logs():
    os.makedirs(LOG_DIR, exist_ok=True)

def log_error(folder, error):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"{folder}_error_{timestamp}.log")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(error)

def run_command(command, cwd):
    process = subprocess.Popen(
        command,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(
            f"Command failed:\n{command}\n\n"
            f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"
        )

def process_folder(folder):
    folder_path = os.path.join(BASE_DIR, folder)
    ps1_script = os.path.join(folder_path, f"{folder}.ps1")

    try:
        # Run gallery-dl
        run_command(GALLERY_CMD, cwd=folder_path)

        # Run PowerShell script after download
        if not os.path.isfile(ps1_script):
            raise FileNotFoundError(f"Missing PowerShell script: {ps1_script}")

        run_command(
            f'powershell -ExecutionPolicy Bypass -File "{ps1_script}"',
            cwd=folder_path
        )

        return f"{folder}: completed successfully"

    except Exception as e:
        error_details = (
            f"Folder: {folder}\n"
            f"Time: {datetime.now()}\n\n"
            f"{str(e)}\n\n"
            f"Traceback:\n{traceback.format_exc()}"
        )
        log_error(folder, error_details)
        raise

def main():
    ensure_logs()

    with ThreadPoolExecutor(max_workers=len(FOLDERS)) as executor:
        futures = {executor.submit(process_folder, folder): folder for folder in FOLDERS}

        for future in as_completed(futures):
            folder = futures[future]
            try:
                print(future.result())
            except Exception:
                print(f"{folder}: failed, see log file")

if __name__ == "__main__":
    main()
