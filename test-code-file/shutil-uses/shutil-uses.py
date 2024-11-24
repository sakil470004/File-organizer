import shutil

# Examples of shutil usage:
# Copy file
shutil.copy('source.txt', 'destination.txt')

# Move file
shutil.move('old_location.txt', 'new_location.txt')

# Copy entire directory
shutil.copytree('old_folder', 'new_folder')

# Remove directory and contents
shutil.rmtree('folder_to_delete')