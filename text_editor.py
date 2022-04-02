import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb


class TextEditor:
    def __init__(self, window, *args):
        self.window = window
        self.current_file = None
        self.file_types = (('text files', '*.txt'), ("Python Files", "*.py"), ('All files', '*.*'))
        self.window.geometry("1000x800")
        self.window.title("TextEditor")
        self.text = tk.Text(self.window, bg="#333333", fg="#ffa500", font=("Helvetica", "16"), state="normal")
        self.text.pack(expand=True)
        self.status = tk.StringVar()
        self.statusbar = tk.Label(window, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.N)
        self.status.set('Ready for work!')
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.menubar = tk.Menu(window)
        self.set_menu(window)
        self.set_hot_keys()

    def is_changes(self):
        if self.current_file is None:
            return False
        file_to_read = open(self.current_file, 'r')
        file_content = file_to_read.read()
        text_area_content = self.text.get(1.0, tk.END)
        return file_content != text_area_content

    def set_menu(self, window):
        window.config(menu=self.menubar)
        file_menu = tk.Menu(self.menubar)
        file_menu.add_command(label='Open', command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label='Save', command=self.save, accelerator="Ctrl+S")
        file_menu.add_command(label='Save as', command=self.save_as_file, accelerator="Ctrl+Q")
        file_menu.add_command(label='Exit', command=self.exit, accelerator="Ctrl+E")
        self.menubar.add_cascade(label="File", menu=file_menu)

    def set_hot_keys(self):
        self.window.bind('<Control-s>', self.save)
        self.window.bind('<Control-o>', self.open_file)
        self.window.bind('<Control-a>', self.save_as_file)
        self.window.bind('<Control-e>', self.exit)

    def open_file(self, *args):
        self.status.set('Opening a file...')
        self.text.delete("1.0", tk.END)
        self.current_file = filedialog.askopenfilename(title="Open file", filetypes=self.file_types)
        print(self.current_file)
        file_to_read = open(self.current_file, 'r')
        stuff = file_to_read.read()
        self.text.insert(tk.END, stuff)
        self.status.set(self.current_file)
        file_to_read.close()

    def save(self, *args):
        if self.current_file is not None:
            input_file = open(self.current_file, 'w')
            input_file.truncate(0)
            input_file.write(self.text.get(1.0, tk.END))
            input_file.close()

    def save_as_file(self, *args):
        self.current_file = filedialog.asksaveasfilename(defaultextension=".*", filetypes=self.file_types)
        text_file = open(self.current_file, 'w')
        text_file.write(self.text.get(1.0, tk.END))
        text_file.close()

    def exit(self, *args):
        if not self.is_changes():
            self.window.destroy()
            return
        msg_box = mb.askquestion('Exit Text Editor', 'You have unsaved changes. Do you want to save them?',
                                 icon='warning')
        if msg_box == 'yes':
            self.save()
        self.window.destroy()


