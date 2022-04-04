import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb


class TextEditor:
    def __init__(self, window, *args):
        self.window = window
        self.current_file = None
        self.file_types = (
            ('text files', '*.txt'), ("Python Files", "*.py"),
            ('All files', '*.*'))
        self.window.geometry("1000x700")
        self.window.title("TextEditor")
        self.scrollbar = self.create_scroll_bar(window)
        self.text = tk.Text(self.window, bg="#333333", fg="#ffa500",
                            font=("times new roman", "16", "bold"),
                            state="normal",
                            relief=tk.GROOVE, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)
        self.text.pack(fill=tk.BOTH, expand=1)
        self.status = tk.StringVar()
        self.statusbar = tk.Label(window, textvariable=self.status, bd=1,
                                  relief=tk.SUNKEN, anchor=tk.N)
        self.set_status_bar()
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
                              accelerator="Ctrl+A")
        file_menu.add_separator()
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
        edit_menu.add_command(label='Undo', command=self.undo,
                              accelerator="Ctrl+U")
        edit_menu.add_separator()
        edit_menu.add_command(label='Buffer', command=self.show_buffer,
                              accelerator="Ctrl+B")
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        help_menu = tk.Menu(self.menubar)
        help_menu.add_command(label="About", command=TextEditor.about)
        self.menubar.add_cascade(label="Help", menu=help_menu)

    @staticmethod
    def about(*args):
        mb.showinfo(message="Text editor for python review\n version 1.1.1")

    def set_hot_keys(self):
        self.window.bind('<Control-s>', self.save)
        self.window.bind('<Control-o>', self.open_file_dialog)
        self.window.bind('<Control-a>', self.save_as_file)
        self.window.bind('<Control-e>', self.exit)
        self.window.bind('<Control-c>', self.copy)
        self.window.bind('<Control-v>', self.paste)
        self.window.bind('<Control-x>', self.cut)
        self.window.bind('<Control-b>', self.show_buffer)
        self.window.bind('<Control-u>', self.undo)

    def open_file_dialog(self, *args):
        self.status.set('Opening a file...')
        new_file = filedialog.askopenfilename(title="Open file",
                                              filetypes=self.file_types)
        if new_file == "":
            return
        self.current_file = new_file
        self.open_file()

    def open_file(self):
        self.text.delete("1.0", tk.END)
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

    @staticmethod
    def create_scroll_bar(window):
        scrollbar = tk.Scrollbar(window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return scrollbar

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

    def undo(self, *args):
        self.open_file()

    def show_buffer(self, *args):
        if len(self.buffer) == 0:
            mb.showinfo("", "Exchange buffer is empty")
            return
        buffer_window = tk.Tk()
        buffer_window.title("Exchange buffer")
        summary_length = 0
        for text in self.buffer:
            summary_length += max(2, len(text) // 48 + 1)
        buffer_window.geometry("360x{}".format(str(min(summary_length * 21,
                                                       600))))
        buffer_frame = tk.Frame(buffer_window)
        buffer_frame.pack(fill=tk.BOTH, expand=1)
        buffer_canvas = tk.Canvas(buffer_frame)
        buffer_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        buffer_scroll_bar = tk.Scrollbar(buffer_frame, orient=tk.VERTICAL,
                                         command=buffer_canvas.yview)
        buffer_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        buffer_canvas.configure(yscrollcommand=buffer_scroll_bar.set)
        buffer_canvas.bind('<Configure>',
                           lambda e: buffer_canvas.configure(
                               scrollregion=buffer_canvas.bbox("all")))
        second_frame = tk.Frame(buffer_canvas)
        buffer_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        cnt = 0
        for text in self.buffer[::-1]:
            cropped_text = text
            tk.Button(second_frame,
                      text=cropped_text,
                      command=self.make_button_func(text, buffer_window),
                      height=max(2, len(cropped_text) // 48 + 1),
                      width=32,
                      padx=0, pady=0, wraplength=300).grid(
                row=cnt, column=0, pady=0, padx=10)
            cnt += 1

    def add_to_buffer(self, text):
        self.buffer.append(text)

    def make_button_func(self, text_to_insert, buffer_window):
        def func():
            index = self.text.index(tk.INSERT)
            self.text.insert(index, text_to_insert)
            buffer_window.destroy()

        return func
