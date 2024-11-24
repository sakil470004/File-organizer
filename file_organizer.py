import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("600x400")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Source folder selection
        ttk.Label(self.main_frame, text="Select Folder to Organize:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar()
        self.folder_entry = ttk.Entry(self.main_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.grid(row=1, column=0, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_folder).grid(row=1, column=1)
        
        # Organization options
        ttk.Label(self.main_frame, text="Organization Method:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.org_method = tk.StringVar(value="extension")
        ttk.Radiobutton(self.main_frame, text="By Extension", variable=self.org_method, 
                       value="extension").grid(row=3, column=0, sticky=tk.W)
        ttk.Radiobutton(self.main_frame, text="By Date", variable=self.org_method, 
                       value="date").grid(row=4, column=0, sticky=tk.W)
        
        # Organize button
        ttk.Button(self.main_frame, text="Organize Files", command=self.organize_files).grid(row=5, column=0, pady=20)
        
        # Status display
        self.status_text = tk.Text(self.main_frame, height=10, width=50)
        self.status_text.grid(row=6, column=0, columnspan=2, pady=5)
        
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)
    
    def update_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def organize_by_extension(self, folder_path):
        for file_path in Path(folder_path).glob('*.*'):
            if file_path.is_file():
                # Get the file extension and create folder name
                extension = file_path.suffix[1:].upper() if file_path.suffix else 'No Extension'
                new_folder = Path(folder_path) / extension
                
                # Create folder if it doesn't exist
                new_folder.mkdir(exist_ok=True)
                
                # Move file
                try:
                    shutil.move(str(file_path), str(new_folder / file_path.name))
                    self.update_status(f"Moved {file_path.name} to {extension} folder")
                except Exception as e:
                    self.update_status(f"Error moving {file_path.name}: {str(e)}")
    
    def organize_by_date(self, folder_path):
        for file_path in Path(folder_path).glob('*.*'):
            if file_path.is_file():
                # Get file's modification time
                timestamp = file_path.stat().st_mtime
                date = datetime.fromtimestamp(timestamp)
                folder_name = date.strftime('%Y-%m')
                
                # Create folder if it doesn't exist
                new_folder = Path(folder_path) / folder_name
                new_folder.mkdir(exist_ok=True)
                
                # Move file
                try:
                    shutil.move(str(file_path), str(new_folder / file_path.name))
                    self.update_status(f"Moved {file_path.name} to {folder_name} folder")
                except Exception as e:
                    self.update_status(f"Error moving {file_path.name}: {str(e)}")
    
    def organize_files(self):
        folder_path = self.folder_path.get()
        if not folder_path:
            self.update_status("Please select a folder first!")
            return
        
        self.status_text.delete(1.0, tk.END)
        self.update_status(f"Starting organization of {folder_path}")
        
        try:
            if self.org_method.get() == "extension":
                self.organize_by_extension(folder_path)
            else:
                self.organize_by_date(folder_path)
            self.update_status("Organization complete!")
        except Exception as e:
            self.update_status(f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()