import os
import json
import tkinter as tk
import customtkinter as ctk


print(f'Current dir (Settings): {os.getcwd()}')
rootDir = 'C:\\Users\\Gatis\\Documents\\GitHub\\Tkinter-Learning-Project\\Windows9\\System33\\'  # Temp. solution
os.chdir(rootDir)

# Load system info
with open('sysinfo.json', 'r') as sysinfo:
    sysInfo = json.load(sysinfo)

    print('System info')
    for item in sysInfo.items():
        print(item)

screenWidth = sysInfo['Screen Width']
screenHeight = sysInfo['Screen Height']
edition = sysInfo['Edition']


# Window Setup
window = ctk.CTk()
window.title('Settings')
winWidth = int(screenWidth * 0.3)
winHeight = int(screenHeight * 0.4)
window.geometry(f'{winWidth}x{winHeight}')

# Load user settings
with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

    print('\nSettings')
    for setting in settings.items():
        print(setting)
    print('\n')

username = settings['Username']
darkMode = settings['Dark Mode']

if darkMode:
    ctk.set_appearance_mode('dark')
else:
    ctk.set_appearance_mode('light')

# Categories
categoryFrame = ctk.CTkFrame(window)
categoryFrame.place(x=0, y=0, relwidth=0.3, relheight=1)

class Category(ctk.CTkFrame):
    def __init__(self, name):
        super().__init__(master=window, fg_color='black')
        self.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

        self.name = name

        self.label = ctk.CTkLabel(self, text=self.name)
        self.label.pack()

        self.button = ctk.CTkButton(master=categoryFrame,
                                    command=self.switch_categories,
                                    text=self.name)
        self.button.pack(pady=2, padx=1, fill='x')

    def switch_categories(self):
        self.lift()

system = Category('System')
display = Category('Display')
users = Category('Users')

system.lift()


# Settings
class Options(ctk.CTkFrame):
    def __init__(self, name, variable, category, set_type):
        super().__init__(master=category)
        self.pack(fill='both')

        self.label = ctk.CTkLabel(self, text=name)
        self.label.pack(side='left', padx=5)

        self.type = set_type

        match self.type:
            case 'switch':
                self.variable = tk.BooleanVar(value=variable)
                self.switch = ctk.CTkSwitch(self, variable=self.variable)
                self.switch.pack(side='right')
            case 'entry':
                self.variable = tk.StringVar(value=variable)
                self.entry = ctk.CTkEntry(self, textvariable=self.variable)
                self.entry.pack(side='right')


darkModeSet = Options('Dark Mode', darkMode, display, 'switch')
usernameSet = Options('Username', username, users, 'entry')

def save_settings():
    os.chdir(f'{rootDir}\\System Info')
    with open('settings.json', 'r') as settings_file:
        settings_dict = json.load(settings_file)

    settings_dict['Username'] = usernameSet.variable.get()
    settings_dict['Dark Mode'] = darkModeSet.variable.get()

    print('New Settings:')
    for item in settings_dict.items():
        print(item)

    with open('settings.json', 'w') as settings_file:
        json.dump(settings_dict, settings_file)

    os.chdir(rootDir)

saveButton = ctk.CTkButton(categoryFrame, text='Save', command=save_settings)
saveButton.pack(side='bottom', pady=2)


window.mainloop()
