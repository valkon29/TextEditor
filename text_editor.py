import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb


class TextEditor:
    def __init__(self, window, *args):
        print(args)
        self.window = window
        self.current_file = None
        self.file_types = (
            ('text files', '*.txt'), ("Python Files", "*.py"),
            ('All files', '*.*'))
        self.window.geometry("1000x700")
        self.window.title("TextEditor")
        self.text = tk.Text(self.window, bg="#333333", fg="#ffa500",
                            font=("Helvetica", "16"), state="normal",
                            relief=tk.GROOVE)
        self.text.pack(fill=tk.BOTH, expand=1)
        self.status = tk.StringVar()
        self.statusbar = tk.Label(window, textvariable=self.status, bd=1,
                                  relief=tk.SUNKEN, anchor=tk.N)
        self.status.set('Untitled')
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.menubar = tk.Menu(window)
        self.set_menu(window)
        self.set_hot_keys()
        self.buffer = list()
        self.check_for_file_in_args(args)

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
        file_menu.add_command(label='Open', command=self.open_file_dialog,
                              accelerator="Ctrl+O")
        file_menu.add_command(label='Save', command=self.save,
                              accelerator="Ctrl+S")
        file_menu.add_command(label='Save as', command=self.save_as_file,
                              accelerator="Ctrl+Q")
        file_menu.add_command(label='Exit', command=self.exit,
                              accelerator="Ctrl+E")
        self.menubar.add_cascade(label="File", menu=file_menu)
        edit_menu = tk.Menu(self.menubar)
        edit_menu.add_command(label='Copy', command=self.copy,
                              accelerator="Ctrl+C")
        edit_menu.add_command(label='Paste', command=self.paste,
                              accelerator="Ctrl+V")
        edit_menu.add_command(label='Cut', command=self.cut,
                              accelerator="Ctrl+X")
        edit_menu.add_command(label='Buffer', command=self.show_buffer,
                              accelerator="Ctrl+B")
        self.menubar.add_cascade(label="Edit", menu=edit_menu)

    def set_hot_keys(self):
        self.window.bind('<Control-s>', self.save)
        self.window.bind('<Control-o>', self.open_file_dialog)
        self.window.bind('<Control-a>', self.save_as_file)
        self.window.bind('<Control-e>', self.exit)
        self.window.bind('<Control-c>', self.copy)
        self.window.bind('<Control-v>', self.paste)
        self.window.bind('<Control-x>', self.cut)
        self.window.bind('<Control-b>', self.show_buffer)

    def open_file_dialog(self, *args):
        self.status.set('Opening a file...')
        self.text.delete("1.0", tk.END)
        self.current_file = filedialog.askopenfilename(title="Open file",
                                                       filetypes=self.file_types)
        self.open_file()

    def open_file(self):
        file_to_read = open(self.current_file, 'r')
        stuff = file_to_read.read()
        self.text.insert(tk.END, stuff)
        self.status.set(self.current_file)
        file_to_read.close()
        self.set_status_bar()

    def save(self, *args):
        if self.current_file is not None:
            input_file = open(self.current_file, 'w')
            input_file.truncate(0)
            input_file.write(self.text.get(1.0, tk.END))
            input_file.close()

    def save_as_file(self, *args):
        self.current_file = filedialog.asksaveasfilename(defaultextension=".*",
                                                         filetypes=self.file_types)
        text_file = open(self.current_file, 'w')
        text_file.write(self.text.get(1.0, tk.END))
        text_file.close()
        self.set_status_bar()

    def exit(self, *args):
        if not self.is_changes():
            self.window.destroy()
            return
        msg_box = mb.askquestion('Exit Text Editor',
                                 'You have unsaved changes. Do you want to save them?',
                                 icon='warning')
        if msg_box == 'yes':
            self.save()
        self.window.destroy()

    def set_status_bar(self):
        if self.current_file is None:
            self.status.set('Untitled')
            return
        self.status.set(self.current_file)
        
    def check_for_file_in_args(self, *args):
        if len(args[0]) > 1:
            print('hello')
            self.current_file = args[0][1]
            self.open_file()

    def cut(self, *args):
        text = self.text.selection_get()
        self.add_to_buffer(text)
        self.text.event_generate("<<Cut>>")

    def copy(self, *args):
        text = self.text.selection_get()
        self.add_to_buffer(text)
        self.text.event_generate("<<Copy>>")

    def paste(self, *args):
        self.text.event_generate("<<Paste>>")

    def show_buffer(self, *args):
        if len(self.buffer) == 0:
            mb.showinfo("", "Exchange buffer is empty")
            return
        buffer_window = tk.Tk()

        buffer_window.geometry("360x{}".format(str(40 * len(self.buffer))))
        buffer_window.title("Exchange buffer")

        cnt = 0
        for text in self.buffer[::-1]:
            if len(text) > 100:
                cropped_text = text[:100] + "..."
            else:
                cropped_text = text
            new_button = tk.Button(buffer_window,
                                   text=cropped_text,
                                   command=self.make_button_func(text, buffer_window),
                                   height=2,
                                   width=32,
                                   padx=0, pady=0, wraplength=320)
            new_button.place(x=20, y=cnt * 40)
            cnt += 1

    def add_to_buffer(self, text):
        self.buffer.append(text)

    def make_button_func(self, text_to_insert, buffer_window):
        def func():
            index = self.text.index(tk.INSERT)
            self.text.insert(index, text_to_insert)
            buffer_window.destroy()
        return func
