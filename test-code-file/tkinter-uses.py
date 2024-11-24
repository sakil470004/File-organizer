import tkinter as tk
from tkinter import ttk, filedialog

# Example of basic tkinter window with common widgets
class TkinterDemo:
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        self.window.title("Tkinter Demo")
        
        # Label - displays text
        label = ttk.Label(self.window, text="This is a label")
        label.pack()
        
        # Entry - text input field
        entry = ttk.Entry(self.window)
        entry.pack()
        
        # Button
        button = ttk.Button(self.window, text="Click Me", 
                           command=self.button_clicked)
        button.pack()
        
        # File dialog button
        file_button = ttk.Button(self.window, text="Choose File", 
                                command=self.choose_file)
        file_button.pack()
        
        # Radiobuttons
        self.radio_var = tk.StringVar()
        radio1 = ttk.Radiobutton(self.window, text="Option 1", 
                                variable=self.radio_var, value="1")
        radio2 = ttk.Radiobutton(self.window, text="Option 2", 
                                variable=self.radio_var, value="2")
        radio1.pack()
        radio2.pack()
        
        # Text widget - multiline text display
        self.text_area = tk.Text(self.window, height=5, width=30)
        self.text_area.pack()
        
    def button_clicked(self):
        self.text_area.insert(tk.END, "Button clicked!\n")
        
    def choose_file(self):
        filename = filedialog.askopenfilename()
        self.text_area.insert(tk.END, f"Selected file: {filename}\n")

# Run the demo
if __name__ == "__main__":
    demo = TkinterDemo()
    demo.window.mainloop()