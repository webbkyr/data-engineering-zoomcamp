from pathlib import Path
# library for interacting with the file system

current_dir = Path.cwd() # current working directory
current_file = Path(__file__).name

for filepath in current_dir.iterdir():
    if filepath.name == current_file:
        continue
    print(f" - {filepath.name}")
    if filepath.is_file():
        content = filepath.read_text(encoding="utf-8")
        print(f"   Content: {content}")

