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
        self.root.title("File Organizer")  # Simpler title, Mac-style
        self.root.geometry("680x700")  # More compact Mac dimensions
        
        # Configure theme for Mac-like appearance
        self.root.tk.call('tk', 'scaling', 1.7)  # Better scaling for Retina displays
        
        # Default groups (same as before)
        self.default_groups = {
            "Documents": ["pdf", "doc", "docx", "txt", "rtf", "odt"],
            "Images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff"],
            "Videos": ["mp4", "avi", "mkv", "mov", "wmv"],
            "Audio": ["mp3", "wav", "flac", "m4a", "aac"],
            "Archives": ["zip", "rar", "7z", "tar", "gz"],
            "Code": ["py", "java", "cpp", "html", "css", "js"]
        }
        
        # Load saved settings
        self.config_file = "organizer_config.json"
        self.extension_groups = self.load_config()
        
        # Style configuration for Mac look
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('SF Pro Text', 13))
        self.style.configure('Header.TLabel', font=('SF Pro Display', 15, 'bold'))
        self.style.configure('TButton', font=('SF Pro Text', 13), padding=6)
        self.style.configure('TEntry', font=('SF Pro Text', 13), padding=4)
        self.style.configure('TCombobox', font=('SF Pro Text', 13), padding=4)
        self.style.configure('Treeview', font=('SF Pro Text', 13))
        
        # Main container with Mac-like padding
        self.main_container = ttk.Frame(root, padding="20 20 20 20")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_container.columnconfigure(0, weight=1)
        
        self.create_mac_ui()
    
    def create_mac_ui(self):
        # Source Selection - Mac style
        ttk.Label(self.main_container, text="Source", style='Header.TLabel').grid(
            row=0, column=0, sticky="w", pady=(0, 10))
        
        source_frame = ttk.Frame(self.main_container)
        source_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        source_frame.columnconfigure(0, weight=1)
        
        self.folder_path = tk.StringVar(value=self.extension_groups.get("last_path", ""))
        path_entry = ttk.Entry(source_frame, textvariable=self.folder_path)
        path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        choose_btn = ttk.Button(source_frame, text="Choose...", 
                              command=self.browse_folder)
        choose_btn.grid(row=0, column=1)
        
        # Groups Section - Mac style
        ttk.Label(self.main_container, text="File Groups", 
                 style='Header.TLabel').grid(row=2, column=0, 
                 sticky="w", pady=(20, 10))
        
        # Predefined Groups
        group_frame = ttk.Frame(self.main_container)
        group_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        group_frame.columnconfigure(1, weight=1)
        
        self.predefined_group = tk.StringVar()
        group_combo = ttk.Combobox(group_frame, 
                                 textvariable=self.predefined_group,
                                 values=list(self.default_groups.keys()),
                                 width=25,
                                 state="readonly")
        group_combo.grid(row=0, column=0, padx=(0, 8))
        group_combo.bind('<<ComboboxSelected>>', self.on_group_selected)
        
        add_btn = ttk.Button(group_frame, text="Add Group", 
                           command=self.add_predefined_group)
        add_btn.grid(row=0, column=1, sticky="w")
        
        # Custom Group
        custom_frame = ttk.Frame(self.main_container)
        custom_frame.grid(row=4, column=0, sticky="ew", pady=(10, 10))
        custom_frame.columnconfigure(2, weight=1)
        
        self.new_group_name = tk.StringVar()
        name_entry = ttk.Entry(custom_frame, textvariable=self.new_group_name,
                             width=20)
        name_entry.insert(0, "Group Name")
        name_entry.bind('<FocusIn>', lambda e: name_entry.delete(0, 'end'))
        name_entry.grid(row=0, column=0, padx=(0, 8))
        
        self.new_group_extensions = tk.StringVar()
        ext_entry = ttk.Entry(custom_frame, textvariable=self.new_group_extensions)
        ext_entry.insert(0, "Extensions (comma-separated)")
        ext_entry.bind('<FocusIn>', lambda e: ext_entry.delete(0, 'end'))
        ext_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        
        add_custom_btn = ttk.Button(custom_frame, text="Add Custom", 
                                  command=self.add_extension_group)
        add_custom_btn.grid(row=0, column=2, sticky="w")
        
        # Current Groups
        ttk.Label(self.main_container, text="Current Groups", 
                 style='Header.TLabel').grid(row=5, column=0, 
                 sticky="w", pady=(20, 10))
        
        self.groups_text = tk.Text(self.main_container, height=6, width=50,
                                font=('SF Mono', 13))
        self.groups_text.grid(row=6, column=0, sticky="ew", pady=(0, 20))
        
        # Organization Options - Mac style
        options_frame = ttk.Frame(self.main_container)
        options_frame.grid(row=7, column=0, sticky="ew", pady=(0, 20))
        
        ttk.Label(options_frame, text="Organization Method", 
                 style='Header.TLabel').grid(row=0, column=0, 
                 sticky="w", pady=(0, 10))
        
        self.org_method = tk.StringVar(value="extension")
        ttk.Radiobutton(options_frame, text="By File Type", 
                       variable=self.org_method, 
                       value="extension").grid(row=1, column=0, 
                       sticky="w", padx=20)
        ttk.Radiobutton(options_frame, text="By Date", 
                       variable=self.org_method, 
                       value="date").grid(row=2, column=0, 
                       sticky="w", padx=20)
        
        # Primary Action Button - Mac style
        organize_btn = ttk.Button(options_frame, text="Organize Files",
                               command=self.organize_files)
        organize_btn.grid(row=3, column=0, sticky="w", padx=20, pady=(20, 0))
        
        # Status Area - Mac style
        ttk.Label(self.main_container, text="Status", 
                 style='Header.TLabel').grid(row=8, column=0, 
                 sticky="w", pady=(20, 10))
        
        status_frame = ttk.Frame(self.main_container)
        status_frame.grid(row=9, column=0, sticky="ew")
        status_frame.columnconfigure(0, weight=1)
        
        self.status_text = tk.Text(status_frame, height=6, width=50,
                                font=('SF Mono', 13), wrap='word',
                                background='#F5F5F5')
        self.status_text.grid(row=0, column=0, sticky="ew")
        
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical",
                               command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.update_groups_display()
        
    def create_group_management(self):
        # Group Management Section
        group_frame = ttk.LabelFrame(self.main_container, text="Extension Groups", padding="10", style='Group.TLabelframe')
        group_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Predefined groups dropdown
        ttk.Label(group_frame, text="Select Predefined Group:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.predefined_group = tk.StringVar()
        group_dropdown = ttk.Combobox(group_frame, textvariable=self.predefined_group, values=list(self.default_groups.keys()))
        group_dropdown.grid(row=0, column=1, padx=5)
        group_dropdown.bind('<<ComboboxSelected>>', self.on_group_selected)
        
        # Add group button
        ttk.Button(group_frame, text="Add Selected Group", command=self.add_predefined_group).grid(row=0, column=2, padx=5)
        
        # Custom group addition
        ttk.Label(group_frame, text="Or Create Custom Group:", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # Custom group entry fields
        custom_frame = ttk.Frame(group_frame)
        custom_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(custom_frame, text="Group Name:").grid(row=0, column=0, padx=5)
        self.new_group_name = tk.StringVar()
        ttk.Entry(custom_frame, textvariable=self.new_group_name, width=20).grid(row=0, column=1, padx=5)
        
        ttk.Label(custom_frame, text="Extensions (comma-separated):").grid(row=0, column=2, padx=5)
        self.new_group_extensions = tk.StringVar()
        ttk.Entry(custom_frame, textvariable=self.new_group_extensions, width=30).grid(row=0, column=3, padx=5)
        
        ttk.Button(custom_frame, text="Add Custom Group", command=self.add_extension_group).grid(row=0, column=4, padx=5)
        
        # Current groups display
        ttk.Label(group_frame, text="Current Groups:", style='Header.TLabel').grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.groups_text = tk.Text(group_frame, height=6, width=80)
        self.groups_text.grid(row=4, column=0, columnspan=3, pady=5)
        self.update_groups_display()
        
    def create_organization_options(self):
        # Organization Options Section
        options_frame = ttk.LabelFrame(self.main_container, text="Organization Options", padding="10", style='Group.TLabelframe')
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.org_method = tk.StringVar(value="extension")
        ttk.Radiobutton(options_frame, text="Organize by Extension Groups", variable=self.org_method, 
                       value="extension").grid(row=0, column=0, padx=10)
        ttk.Radiobutton(options_frame, text="Organize by Date", variable=self.org_method, 
                       value="date").grid(row=0, column=1, padx=10)
        
        # Organize button
        ttk.Button(options_frame, text="Organize Files", command=self.organize_files,
                  style='Accent.TButton').grid(row=1, column=0, columnspan=2, pady=10)
        
    def create_status_area(self):
        # Status Section
        status_frame = ttk.LabelFrame(self.main_container, text="Status", padding="10", style='Group.TLabelframe')
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.status_text = tk.Text(status_frame, height=8, width=80)
        self.status_text.grid(row=0, column=0, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
    
    def on_group_selected(self, event):
        """Handle group selection from dropdown"""
        selected = self.predefined_group.get()
        if selected in self.default_groups:
            self.new_group_extensions.set(','.join(self.default_groups[selected]))
    
    def add_predefined_group(self):
        """Add the currently selected predefined group"""
        selected = self.predefined_group.get()
        if selected and selected in self.default_groups:
            if "groups" not in self.extension_groups:
                self.extension_groups["groups"] = {}
            self.extension_groups["groups"][selected] = self.default_groups[selected]
            self.save_config()
            self.update_groups_display()
            self.update_status(f"Added predefined group: {selected}")
    
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
        for group, extensions in self.extension_groups.get("groups", {}).items():
            self.groups_text.insert(tk.END, f"{group}: {', '.join(extensions)}\n")
    
    def add_extension_group(self):
        group_name = self.new_group_name.get().strip()
        extensions = [ext.strip().lower() for ext in self.new_group_extensions.get().split(',') if ext.strip()]
        
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
        self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
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
                extension = file_path.suffix[1:].lower()
                group_name = self.get_group_for_extension(extension)
                
                new_folder = Path(folder_path) / group_name
                new_folder.mkdir(exist_ok=True)
                
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