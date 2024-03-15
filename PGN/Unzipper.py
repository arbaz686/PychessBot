import zipfile
import pathlib

for path in pathlib.Path("PGN_ZIPS").iterdir():
    if path.is_file():
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall("PGN_files")
