import tkinter as tk
import customtkinter as ctk
from platform import system, release
from os import getlogin
from darkdetect import isDark
from random import choice

def create_window(title, width, height):
    window = ctk.CTk()
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    window.title(title)
    windowWidth = int(screenWidth * width)
    windowHeight = int(screenHeight * height)
    window.geometry(f'{windowWidth}x{windowHeight}')
    window.resizable(False, False)
    return window, windowWidth, windowHeight

def create_label(master, text, y_position, anchor='center'):
    label = ctk.CTkLabel(master=master, text=text, justify='center')
    label.place(relx=0.5, y=y_position, anchor=anchor)
    return label

def create_button(master, text, width, height, command, side='right'):
    button = ctk.CTkButton(master=master, text=text, width=width, height=height, command=command)
    button.pack(side=side, padx=5)
    return button

def create_combobox(master, values, y_position, width=0.3, anchor='center'):
    stringVar = tk.StringVar(value='Choose edition')
    combobox = ctk.CTkComboBox(master=master, variable=stringVar, values=values, state='readonly')
    combobox.place(relx=0.5, y=y_position, relwidth=width, anchor=anchor)
    return combobox, stringVar

def create_entry(master, y_position, label_text):
    label = create_label(master, label_text, y_position - 22)
    stringVar = tk.StringVar()
    entry = ctk.CTkEntry(master=master, textvariable=stringVar)
    entry.place(relx=0.5, y=y_position, anchor='center')
    return entry, stringVar

def create_switch(master, text, variable, command, x_position, y_position, anchor='sw'):
    switch = ctk.CTkSwitch(master=master, text=text, variable=variable, command=command)
    switch.place(x=x_position, y=y_position, anchor=anchor)
    return switch

# Installer
installer, installerWidth, installerHeight = create_window('Windows 9 Installer', 0.4, 0.4)

# System information
currentOS = f'{system()} {release()}'
print('System info')
print(f'Current OS: {currentOS}')
print(f'Screen resolution: {installerWidth}x{installerHeight}')

# GUI Elements
frame1 = ctk.CTkFrame(master=installer)
frame1.pack(side='top', expand=True, fill='both')

titleText = f'Thank you for choosing Windows 9\nWe promise it\'ll be much better than your useless {currentOS}'
title = create_label(frame1, titleText, 20)

editions = ['Windows 9 Home', 'Windows 9 Pro', 'Windows 9+', "Windows 9 Home+", 'Windows 9 Pro+', 'Windows 9 HomePro', 'Windows 9 HomePro+']
editionsSelect, editionsString = create_combobox(frame1, editions, 70)

usernameEntry, usernameString = create_entry(frame1, 120, 'Username:')

darkModeVar = tk.BooleanVar(value=isDark())
ldModeSwitch = create_switch(frame1, 'Dark Mode', darkModeVar, switch_ld_mode, 15, installerHeight - 15)

buttonFrame = ctk.CTkFrame(master=frame1, fg_color='transparent')
buttonFrame.place(x=installerWidth - 15, y=installerHeight - 15, anchor='se')

buttonWidth = int(installerWidth / 27)
buttonHeight = int(installerHeight / 50)

installButton = create_button(buttonFrame, 'Install', buttonWidth, buttonHeight, install_func)
lazyButton = create_button(buttonFrame, 'I don\'t care', buttonWidth, buttonHeight, lazy_func)

installer.mainloop()
