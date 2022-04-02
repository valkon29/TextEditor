import tkinter as tk
import sys

from text_editor import TextEditor

window = tk.Tk()

TextEditor(window, sys.argv)

window.mainloop()
