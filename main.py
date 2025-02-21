import shutil
import zipfile
from pathlib import Path
from mokuro.run import run

BASE_DIR = Path("C:/Users/marth/Documents/Manga")

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

def run_mokuro_directly(paths, parent_dir=None, disable_confirmation=False):
    run(*paths, parent_dir=parent_dir, disable_confirmation=disable_confirmation, legacy_html=False, no_cache=True)

def main():
    input_dir = BASE_DIR / "Manga"
    if not input_dir.exists():
        print("No inputs found")
        return
    
    manga_list = []
    for directory in input_dir.iterdir():
        if directory.is_dir():
            manga_list.append(directory)
    
    run_mokuro_directly(manga_list, disable_confirmation=True)

    zip_manga_folders(input_dir)

    output_dir = BASE_DIR / "outputs"
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    move_zips(input_dir, output_dir)

main()