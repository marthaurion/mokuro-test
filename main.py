import shutil
import zipfile
from pathlib import Path
from mokuro.run import run

BASE_DIR = Path("E:/Downloads")

def zip_manga_folders(input_directory: Path):
    # Loop through each folder in the input directory
    for folder in input_directory.iterdir():
        if folder.stem == "_ocr":
            continue
        if folder.is_dir():  # Only process directories
            zip_file_path = input_directory / f"{folder.name}.zip"

            # Create a zip file
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file in folder.rglob("*"):  # Recursively get all files
                    if file.is_file():
                        zipf.write(file, file.relative_to(folder))  # Keep relative path inside zip

            print(f"✔ {folder.name} zipped successfully!")

def move_zips(source_directory: Path, destination_directory: Path):
    # Ensure destination directory exists
    destination_directory.mkdir(parents=True, exist_ok=True)

    for file in source_directory.iterdir():
        if file.is_dir():
            if file.stem == "_ocr":
                shutil.move(file, destination_directory / file.name)
            else:
                continue
        else:
            shutil.move(file, destination_directory / file.name)
            print(f"📦 Moved {file.name} to {destination_directory}")

def run_mokuro_directly(input_folder):
    run(parent_dir=input_folder)

# Example usage
input_dir = BASE_DIR / "Manga Inputs/"
if not input_dir.exists():
    input_dir.mkdir(parents=True)

run_mokuro_directly(input_dir)

zip_manga_folders(input_dir)

output_dir = BASE_DIR / "Manga Outputs"
if not output_dir.exists():
    output_dir.mkdir(parents=True)

move_zips(input_dir, output_dir)