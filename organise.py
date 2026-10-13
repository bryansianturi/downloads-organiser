from pathlib import Path
import shutil

FOLDER = Path("test-downloads")  # later: Path.home() / "Downloads"
DRY_RUN = True  # True = only print, don't move anything

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".heic", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".md", ".pptx", ".xlsx", ".csv"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Audio": [".mp3", ".wav", ".m4a"],
    "Video": [".mp4", ".mov", ".mkv"],
    "Code": [".py", ".java", ".js", ".html", ".css", ".json"],
    "Installers": [".dmg", ".pkg"],
}


def category_for(file):
    """Return the folder name a file belongs in, based on its extension."""
    ext = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def unique_path(path):
    """If a file with this name already exists, add (1), (2)... so nothing gets overwritten."""
    new_path = path
    counter = 1
    while new_path.exists():
        new_path = path.with_name(f"{path.stem} ({counter}){path.suffix}")
        counter += 1
    return new_path


moved = 0
for file in list(FOLDER.iterdir()):
    if file.is_dir() or file.name.startswith("."):
        continue  # skip folders and hidden files like .DS_Store

    category = category_for(file)
    destination = unique_path(FOLDER / category / file.name)

    if DRY_RUN:
        print(f"[dry run] {file.name}  ->  {category}/")
    else:
        destination.parent.mkdir(exist_ok=True)
        shutil.move(file, destination)
        print(f"Moved {file.name}  ->  {category}/{destination.name}")
    moved += 1

print(f"\n{moved} file(s) {'would be' if DRY_RUN else ''} organised.")
