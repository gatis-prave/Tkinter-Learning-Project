import tkinter as tk
import customtkinter as ctk
from platform import system, release
from os import getlogin
from darkdetect import isDark
from random import choice

# Installer
# Window setup
installer = ctk.CTk()
screenWidth = installer.winfo_screenwidth()
screenHeight = installer.winfo_screenheight()
installer.title('Windows 9 Installer')
installerWidth = int(screenWidth * 0.4)
installerHeight = int(screenHeight * 0.4)
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
        darkModeVar.set(True)
    else:
        ctk.set_appearance_mode('light')
        darkModeVar.set(False)


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
def install_func():
    print('\nInstaller settings')
    editions_string = editionsString.get()
    if editions_string == 'Choose edition':
        editionsString.set('Windows 9 Retarded')
    print(f'Edition: {editions_string}')
    username_string = usernameString.get().strip(',./;: ')
    if username_string == '':
        usernameString.set('Retard')
    print(f'Username: {username_string}')
    installer.destroy()


installButton = ctk.CTkButton(master=buttonFrame,
                              text='Install',
                              width=buttonWidth,
                              height=buttonHeight,
                              command=install_func)

installButton.pack(side='right', padx=5)


# Lazy button
def lazy_func():
    random_edition = choice(editions)
    editionsString.set(random_edition)
    usernameString.set(getlogin())
    darkModeVar.set(True)
    ctk.set_appearance_mode('dark')


lazyButton = ctk.CTkButton(master=buttonFrame,
                           text='I don\'t care',
                           width=buttonWidth,
                           height=buttonHeight,
                           command=lazy_func)
lazyButton.pack(side='right')

installer.mainloop()