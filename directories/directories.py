import os

os.makedirs("somedir",exist_ok=True)
os.makedirs("somedir/some_nested_dir", exist_ok=True)
os.makedirs("somedir/some_nested_dir/some_nested_nested_dir", exist_ok=True)
os.makedirs("somedir/some_another_nested_dir", exist_ok=True)
