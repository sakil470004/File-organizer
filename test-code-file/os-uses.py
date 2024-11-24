import os

# Examples of os library usage:
# Get current working directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# List files in a directory
files = os.listdir('.')
print(f"Files in directory: {files}")

# Join paths (works on both Windows and Mac)
path = os.path.join('folder', 'subfolder', 'file.txt')
print(f"Joined path: {path}")

# Check if path exists
exists = os.path.exists(path)
print(f"Path exists: {exists}")