from pathlib import Path

# Examples of Path usage:
# Create path object
path = Path('folder/subfolder/file.txt')

# Get file name
print(f"File name: {path.name}")

# Get file extension
print(f"Extension: {path.suffix}")

# Get parent directory
print(f"Parent directory: {path.parent}")

# Join paths
new_path = path.parent / 'another_file.txt'
print(f"New path: {new_path}")

# Create directory
Path('new_directory').mkdir(exist_ok=True)

# List all files in directory
for file in Path('.').glob('*.txt'):
    print(f"Found text file: {file}")