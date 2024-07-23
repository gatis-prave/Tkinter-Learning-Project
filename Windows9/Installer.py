import customtkinter as ctk
import tkinter as tk
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
window = ctk.CTk()
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
window.title('Windows 9 Installer')
installerWidth = int(screenWidth * 0.4)
installerHeight = int(screenHeight * 0.4)

print(f'Installer resolution: {installerWidth}x{installerHeight}')

window.geometry(f'{installerWidth}x{installerHeight}')
window.resizable(False, False)


# System information
currentOS = f'{system()} {release()}'
print('System info')
print(f'Current OS: {currentOS}')
print(f'Screen resolution: {screenWidth}x{screenHeight}')

widgetYSpacing = 50

editions = ['Windows 9 Home', 'Windows 9 Pro', 'Windows 9+', "Windows 9 Home+", 'Windows 9 Pro+',
            'Windows 9 HomePro', 'Windows 9 HomePro+']

class Installer(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=window)
        self.place(x=0, y=0, relwidth=1, relheight=1)

        self.widgetFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.widgetFrame.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.5, anchor='n')

        # Title
        self.titleText = f'Thank you for choosing Windows 9\nWe promise it\'ll be much better than your useless {currentOS}'
        self.title = ctk.CTkLabel(master=self.widgetFrame, text=self.titleText, justify='center')
        self.title.place(relx=0.5, rely=0.05, anchor='n')

        # Editions
        self.editionsString = tk.StringVar(value='Choose edition')
        self.editionsSelect = ctk.CTkComboBox(master=self.widgetFrame,
                                              variable=self.editionsString,
                                              values=editions,
                                              state='readonly')
        self.editionsSelect.place(relx=0.5, rely=0.2, relwidth=0.4, anchor='n')

        # Username
        self.usernameLabel = ctk.CTkLabel(master=self.widgetFrame, text='Username:')
        self.usernameLabel.place(relx=0.5, rely=0.30, anchor='n')

        self.usernameString = tk.StringVar()
        self.usernameEntry = ctk.CTkEntry(master=self.widgetFrame, textvariable=self.usernameString)
        self.usernameEntry.place(relx=0.5, rely=0.37, anchor='n')

        # Light/Dark mode
        self.darkModeVar = tk.BooleanVar(value=False)
        self.ldModeSwitch = ctk.CTkSwitch(master=self,
                                          text='Dark Mode',
                                          variable=self.darkModeVar,
                                          command=self.switch_ld_mode)

        self.ldModeSwitch.place(relx=0.02, rely=0.98, anchor='sw')


        self.buttonFrame = ctk.CTkFrame(master=self, fg_color='transparent')
        self.buttonFrame.place(x=installerWidth - 15, y=installerHeight - 15, anchor='se')

        # Install button

        self.installButton = ctk.CTkButton(master=self.buttonFrame,
                                           text='Install',
                                           command=self.install_func)

        self.installButton.pack(side='right', padx=5)

        # Lazy button
        self.lazyButton = ctk.CTkButton(master=self.buttonFrame,
                                        text='I\'m lazy',
                                        command=self.lazy_func)
        self.lazyButton.pack(side='right')

        # Error
        self.errorText = tk.StringVar(master=self)
        self.error = ctk.CTkLabel(master=self, textvariable=self.errorText, text_color='red', justify='center')
        self.error.place(relx=0.5, rely=0.3, anchor='center')
        self.error.lower()


    def switch_ld_mode(self):
        if self.darkModeVar.get():
            ctk.set_appearance_mode('dark')
        else:
            ctk.set_appearance_mode('light')

    def install_func(self):
        editions_string = self.editionsString.get()
        username_string = self.usernameString.get().strip(',./;: ')

        if editions_string == 'Choose edition' and username_string == '':
            self.errorText.set('Please choose an edition and enter your username')
            self.error.lift()
        elif editions_string == 'Choose edition':
            self.errorText.set('Please choose an edition')
            self.error.lift()
        elif username_string == '':
            self.errorText.set('Please enter your username')
            self.error.lift()
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

            settings_dict = {'Username': username_string, 'Dark Mode': self.darkModeVar.get()}
            print(settings_dict)
            with open(f'settings.json', 'w') as settings:
                json.dump(settings_dict, settings)

            files_dict = {}
            with open('files.json', 'w') as files:
                json.dump(files_dict, files)
            os.chdir(f'{rootDir}\\System33')

            if not os.path.exists('Programs'):
                os.makedirs('Programs')

            shutil.copyfile(f'{rootDir}\\Settings.py', f'{rootDir}\\System33\\Programs\\Settings.py')
            shutil.copyfile(f'{rootDir}\\File Explorer.py', f'{rootDir}\\System33\\Programs\\File Explorer.py')

            if not os.path.exists('Files'):
                os.makedirs('Files')
            os.chdir(f'Files')

            if not os.path.exists('Desktop'):
                os.makedirs('Desktop')

            window.destroy()

            os.chdir(rootDir)
            call(["python", 'Desktop.py'])

    def lazy_func(self):
        self.editionsString.set(choice(editions))
        self.usernameString.set(os.getlogin())
        self.darkModeVar.set(True)
        ctk.set_appearance_mode('dark')


installer = Installer()

if isDark():
    installer.darkModeVar.set(True)

class Installed(ctk.CTkFrame):
    def __init__(self):
        super().__init__(window)
        self.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = ctk.CTkLabel(self, text='Windows 9 is already installed')
        self.label.place(relx=0.5, rely=0.1, anchor='n')

        self.launchButton = ctk.CTkButton(self, text='Launch Windows 9', command=Installed.launch_windows)
        self.launchButton.place(relx=0.5, rely=0.9, anchor='s')

        self.repairButton = ctk.CTkButton(self, text='Repair Windows 9', command=Installed.repair_windows)
        self.repairButton.place(relx=0.65, rely=0.9, anchor='s')

    @staticmethod
    def launch_windows():
        os.chdir(rootDir)
        window.destroy()
        call(["python", 'Desktop.py'])

    @staticmethod
    def repair_windows():
        pass

installedScreen = Installed()

if not os.path.exists('System33'):
    installedScreen.lower()


window.mainloop()