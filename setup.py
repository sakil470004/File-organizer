from setuptools import setup

APP = ['file_organizer.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'json', 'pathlib', 'datetime'],
    'includes': ['tkinter', 'tkinter.ttk'],
    'iconfile': 'app_icon.icns',  # Optional, remove if you don't have an icon
    'plist': {
        'CFBundleName': "File Organizer",
        'CFBundleShortVersionString': "1.0.0",
        'CFBundleIdentifier': "com.yourname.fileorganizer",
        'NSHighResolutionCapable': 'True',
    }
}

setup(
    name="FileOrganizer",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)