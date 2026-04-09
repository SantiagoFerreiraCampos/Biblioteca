import subprocess
from datetime import datetime
from pathlib import Path
import shutil

REPO_PATH = Path(__file__).parent
BACKUP_DIR = REPO_PATH / "backups"

def main():
    BACKUP_DIR.mkdir(exist_ok=True)

    print("Pulling latest changes from GitHub...")
    subprocess.run(["git", "pull"], cwd=REPO_PATH, shell=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_name = BACKUP_DIR / f"biblioteca_backup_{timestamp}"

    print("Creating backup...")
    shutil.make_archive(str(zip_name), "zip", REPO_PATH / "data")

    print("Backup created successfully:")
    print(zip_name.with_suffix(".zip"))

if __name__ == "__main__":
    main()