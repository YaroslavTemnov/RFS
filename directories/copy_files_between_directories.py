from pathlib import Path
from shutil import move, copy

file_to_move = Path("file_to_move.txt")
file_to_copy = Path("file_to_copy.txt")
target_directory = Path("somedir")
target_directory.mkdir(exist_ok=True)

move(file_to_move, target_directory/file_to_move)
copy(file_to_copy, target_directory/file_to_copy)