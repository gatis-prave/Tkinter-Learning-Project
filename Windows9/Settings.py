import os
import json
import tkinter as tk
import customtkinter as ctk

rootDir = f'{os.path.dirname(__file__)}'.strip('\\Programs')
os.chdir(f'{rootDir}\\System Info')

# Load system info
with open('sysinfo.json', 'r') as sysinfo:
    sysInfo = json.load(sysinfo)

    print('System info')
    for item in sysInfo.items():
        print(item)

screenWidth = sysInfo['Screen Width']
screenHeight = sysInfo['Screen Height']
edition = sysInfo['Edition']


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

os.chdir(rootDir)

# Window Setup
window = ctk.CTk()
window.title('Settings')
winWidth = int(screenWidth * 0.2)
winHeight = int(screenHeight * 0.2)
window.geometry(f'{winWidth}x{winHeight}')
window.resizable(False, False)

# Categories

categoryFrame = ctk.CTkFrame(window, fg_color=('gray80', 'gray15'))
categoryFrame.place(x=0, y=0, relwidth=0.3, relheight=1)

class Category(ctk.CTkFrame):
    def __init__(self, name):
        super().__init__(master=window)
        self.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

        self.name = name

        self.label = ctk.CTkLabel(self, text=self.name,
                                  fg_color=('gray15', 'gray80'),
                                  text_color=('gray80', 'gray15'),
                                  corner_radius=4)
        self.label.pack(pady=4)

        self.button = ctk.CTkButton(master=categoryFrame,
                                    command=self.switch_categories,
                                    text=self.name,
                                    fg_color=('gray15', 'gray80'),
                                    text_color=('gray80', 'gray15'),
                                    hover_color=('gray30', 'gray50'))
        self.button.pack(pady=3, padx=2, fill='x')

    def switch_categories(self):
        self.lift()

system = Category('System')
display = Category('Display')
users = Category('Users')
applications = Category('Applications')
accessibility = Category('Accessibility')

system.lift()

# Settings
class Options(ctk.CTkFrame):
    def __init__(self, name, variable, category, set_type):
        super().__init__(master=category, fg_color=('gray15', 'gray80'))
        self.pack(fill='both', pady=2)

        self.label = ctk.CTkLabel(self, text=name, text_color=('gray80', 'gray15'))
        self.label.pack(side='left', padx=5)

        self.type = set_type

        match self.type:
            case 'switch':
                self.variable = tk.BooleanVar(value=variable)
                self.switch = ctk.CTkSwitch(self, variable=self.variable, text='',
                                            progress_color='RoyalBlue4')
                self.switch.pack(side='right')
            case 'entry':
                self.variable = tk.StringVar(value=variable)
                self.entry = ctk.CTkEntry(self, textvariable=self.variable,
                                          fg_color=('gray15', 'gray80'),
                                          text_color=('gray80', 'gray15'))
                self.entry.pack(side='right', pady=1, padx=2)


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

saveButton = ctk.CTkButton(categoryFrame, text='Save', command=save_settings,
                           fg_color=('gray15', 'gray80'),
                           text_color=('gray80', 'gray15'),
                           hover_color=('gray30', 'gray50'))
saveButton.pack(side='bottom', pady=4)


window.mainloop()
