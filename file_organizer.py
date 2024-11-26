import os
import json
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer Pro")
        self.root.geometry("800x600")
        
        # Load saved settings
        self.config_file = "organizer_config.json"
        self.extension_groups = self.load_config()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Source folder selection
        ttk.Label(self.main_frame, text="Select Folder to Organize:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar(value=self.extension_groups.get("last_path", ""))
        self.folder_entry = ttk.Entry(self.main_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.grid(row=1, column=0, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_folder).grid(row=1, column=1)
        
        # Extension group management
        ttk.Label(self.main_frame, text="Extension Groups:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Group management frame
        self.group_frame = ttk.LabelFrame(self.main_frame, text="Manage Groups", padding="5")
        self.group_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Add new group
        ttk.Label(self.group_frame, text="Group Name:").grid(row=0, column=0, padx=5)
        self.new_group_name = tk.StringVar()
        ttk.Entry(self.group_frame, textvariable=self.new_group_name, width=20).grid(row=0, column=1, padx=5)
        
        ttk.Label(self.group_frame, text="Extensions (comma-separated):").grid(row=0, column=2, padx=5)
        self.new_group_extensions = tk.StringVar()
        ttk.Entry(self.group_frame, textvariable=self.new_group_extensions, width=30).grid(row=0, column=3, padx=5)
        
        ttk.Button(self.group_frame, text="Add Group", command=self.add_extension_group).grid(row=0, column=4, padx=5)
        
        # Show existing groups
        self.groups_text = tk.Text(self.main_frame, height=6, width=70)
        self.groups_text.grid(row=4, column=0, columnspan=2, pady=5)
        self.update_groups_display()
        
        # Organization options
        ttk.Label(self.main_frame, text="Organization Method:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.org_method = tk.StringVar(value="extension")
        ttk.Radiobutton(self.main_frame, text="By Extension Groups", variable=self.org_method, 
                       value="extension").grid(row=6, column=0, sticky=tk.W)
        ttk.Radiobutton(self.main_frame, text="By Date", variable=self.org_method, 
                       value="date").grid(row=7, column=0, sticky=tk.W)
        
        # Organize button
        ttk.Button(self.main_frame, text="Organize Files", command=self.organize_files).grid(row=8, column=0, pady=20)
        
        # Status display
        self.status_text = tk.Text(self.main_frame, height=10, width=70)
        self.status_text.grid(row=9, column=0, columnspan=2, pady=5)
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {"groups": {}, "last_path": ""}
        except Exception as e:
            return {"groups": {}, "last_path": ""}
    
    def save_config(self):
        try:
            self.extension_groups["last_path"] = self.folder_path.get()
            with open(self.config_file, 'w') as f:
                json.dump(self.extension_groups, f, indent=4)
        except Exception as e:
            self.update_status(f"Error saving configuration: {str(e)}")
    
    def update_groups_display(self):
        self.groups_text.delete(1.0, tk.END)
        self.groups_text.insert(tk.END, "Current Extension Groups:\n")
        for group, extensions in self.extension_groups.get("groups", {}).items():
            self.groups_text.insert(tk.END, f"{group}: {', '.join(extensions)}\n")
    
    def add_extension_group(self):
        group_name = self.new_group_name.get().strip()
        extensions = [ext.strip().lower() for ext in self.new_group_extensions.get().split(',')]
        
        if group_name and extensions:
            if "groups" not in self.extension_groups:
                self.extension_groups["groups"] = {}
            self.extension_groups["groups"][group_name] = extensions
            self.save_config()
            self.update_groups_display()
            self.new_group_name.set("")
            self.new_group_extensions.set("")
            self.update_status(f"Added group: {group_name}")
    
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.save_config()
    
    def update_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def get_group_for_extension(self, extension):
        extension = extension.lower()
        for group, extensions in self.extension_groups.get("groups", {}).items():
            if extension in extensions:
                return group
        return extension.upper()
    
    def organize_by_extension(self, folder_path):
        for file_path in Path(folder_path).glob('*.*'):
            if file_path.is_file():
                # Get the file extension and corresponding group
                extension = file_path.suffix[1:].lower()
                group_name = self.get_group_for_extension(extension)
                
                # Create folder if it doesn't exist
                new_folder = Path(folder_path) / group_name
                new_folder.mkdir(exist_ok=True)
                
                # Move file
                try:
                    shutil.move(str(file_path), str(new_folder / file_path.name))
                    self.update_status(f"Moved {file_path.name} to {group_name} folder")
                except Exception as e:
                    self.update_status(f"Error moving {file_path.name}: {str(e)}")
    
    def organize_by_date(self, folder_path):
        for file_path in Path(folder_path).glob('*.*'):
            if file_path.is_file():
                timestamp = file_path.stat().st_mtime
                date = datetime.fromtimestamp(timestamp)
                folder_name = date.strftime('%Y-%m')
                
                new_folder = Path(folder_path) / folder_name
                new_folder.mkdir(exist_ok=True)
                
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