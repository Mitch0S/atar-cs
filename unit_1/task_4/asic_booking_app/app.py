"""
Task 4 - Managing Data (Year 11 ATAR Computer Science)

Database and App written by Mitch Naake, Butler College
"""
import tkinter
from tkinter import ttk
import customtkinter

import pages


class App:
    global x
    global y
    global root

    # Window Settings
    x = 1000
    y = 750
    tkinter.ttk.title = "Test123"

    root = tkinter.Tk()
    root.geometry(f"{x}x{y}")
    root.resizable(False, False)

    def __init__(self):
        pages.LoginScreen().load(root=root, x=x, y=y)

App()