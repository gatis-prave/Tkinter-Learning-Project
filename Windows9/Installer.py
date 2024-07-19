import tkinter as tk
import customtkinter as ctk
import ctypes
import json
from platform import system, release
import os
from subprocess import call
import shutil
from darkdetect import isDark
from random import choice

ctypes.windll.shcore.SetProcessDpiAwareness(2)

rootDir = os.getcwd()

# Window setup
installer = ctk.CTk()
screenWidth = installer.winfo_screenwidth()
screenHeight = installer.winfo_screenheight()
installer.title('Windows 9 Installer')
installerWidth = int(screenWidth * 0.4)
installerHeight = int(screenHeight * 0.4)

print(f'Installer resolution: {installerWidth}x{installerHeight}')

installer.geometry(f'{installerWidth}x{installerHeight}')
installer.resizable(False, False)


# System information
currentOS = f'{system()} {release()}'
print('System info')
print(f'Current OS: {currentOS}')
print(f'Screen resolution: {screenWidth}x{screenHeight}')

widgetYSpacing = 50
# Screen 1
# Frame
frame1 = ctk.CTkFrame(master=installer)
frame1.pack(side='top', expand=True, fill='both')

# Title
titleText = f'Thank you for choosing Windows 9\nWe promise it\'ll be much better than your useless {currentOS}'
title = ctk.CTkLabel(master=frame1, text=titleText, justify='center')
titleY = 20
title.place(relx=0.5, y=titleY, anchor='center')

# Editions
editions = ['Windows 9 Home', 'Windows 9 Pro', 'Windows 9+', "Windows 9 Home+", 'Windows 9 Pro+',
            'Windows 9 HomePro', 'Windows 9 HomePro+']
editionsString = tk.StringVar(value='Choose edition')
editionsSelect = ctk.CTkComboBox(master=frame1, variable=editionsString, values=editions, state='readonly')
editionsY = titleY + widgetYSpacing
editionsSelect.place(relx=0.5, y=editionsY, relwidth=0.3, anchor='center')

# Username
usernameLabel = ctk.CTkLabel(master=frame1, text='Username:')
usernameString = tk.StringVar()
usernameEntry = ctk.CTkEntry(master=frame1, textvariable=usernameString)
userEntryY = editionsY + widgetYSpacing
usernameEntry.place(relx=0.5, y=userEntryY, anchor='center')
userLabelY = userEntryY - 22
usernameLabel.place(relx=0.5, y=userLabelY, anchor='center')

# Light/Dark mode
def switch_ld_mode():
    if darkModeVar.get():
        ctk.set_appearance_mode('dark')
    else:
        ctk.set_appearance_mode('light')


darkModeVar = tk.BooleanVar(value=False)
if isDark():
    darkModeVar.set(True)

ldModeSwitch = ctk.CTkSwitch(master=frame1, text='Dark Mode', variable=darkModeVar, command=switch_ld_mode)
ldModeX = 15
ldModeY = installerHeight - 15
ldModeSwitch.place(x=ldModeX, y=ldModeY, anchor='sw')

# Buttons
buttonWidth = int(screenWidth / 27)
buttonHeight = int(screenHeight / 50)
buttonSpacing = 5

buttonFrame = ctk.CTkFrame(master=frame1, fg_color='transparent')
buttonFrameX = installerWidth - 15
buttonFrameY = installerHeight - 15
buttonFrame.place(x=installerWidth - 15, y=installerHeight - 15, anchor='se')


# Install button
errorText = tk.StringVar(master=frame1)
error = ctk.CTkLabel(master=frame1, textvariable=errorText, justify='center')
errorY = installerHeight - 20
error.place(relx=0.5, y=errorY, anchor='center')
error.lower()

def install_func():
    editions_string = editionsString.get()
    username_string = usernameString.get().strip(',./;: ')

    if editions_string == 'Choose edition' and username_string == '':
        errorText.set('Please choose an edition and enter your username')
        error.lift()
    elif editions_string == 'Choose edition':
        errorText.set('Please choose an edition')
        error.lift()
    elif username_string == '':
        errorText.set('Please enter your username')
        error.lift()
    else:
        print('\nInstaller settings')
        print(f'Edition: {editions_string}')
        print(f'Username: {username_string}')

        if not os.path.exists('System33'):
            os.makedirs('System33')
        os.chdir('System33')

        if not os.path.exists('System Info'):
            os.makedirs('System Info')
        os.chdir('System Info')

        sys_info = {'Screen Width': screenWidth, 'Screen Height': screenHeight, 'Old OS': currentOS,
                    'Edition': editions_string}
        with open('sysinfo.json', 'w') as sysinfo:
            json.dump(sys_info, sysinfo)

        settings_dict = {'Username': username_string, 'Dark Mode': darkModeVar.get()}
        print(settings_dict)
        with open('settings.json', 'w') as settings:
            json.dump(settings_dict, settings)
        os.chdir(f'{rootDir}\\System33')

        if not os.path.exists('Programs'):
            os.makedirs('Programs')

        shutil.copyfile(f'{rootDir}\\Settings.py', f'{rootDir}\\System33\\Programs\\Settings.py')

        if not os.path.exists('Desktop'):
            os.makedirs('Desktop')
        os.chdir('Desktop')

        files_dict = {}
        with open('files.json', 'w') as files:
            json.dump(files_dict, files)

        installer.destroy()

        os.chdir(rootDir)
        call(["python", 'Desktop.py'])



installButton = ctk.CTkButton(master=buttonFrame,
                              text='Install',
                              width=buttonWidth,
                              height=buttonHeight,
                              command=install_func)

installButton.pack(side='right', padx=5)

# Lazy button
def lazy_func():
    editionsString.set(choice(editions))
    usernameString.set(os.getlogin())
    darkModeVar.set(True)
    ctk.set_appearance_mode('dark')


lazyButton = ctk.CTkButton(master=buttonFrame,
                           text='I\'m lazy',
                           width=buttonWidth,
                           height=buttonHeight,
                           command=lazy_func)
lazyButton.pack(side='right')

installer.mainloop()