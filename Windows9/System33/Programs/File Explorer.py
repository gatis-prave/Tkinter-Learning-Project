import os
import json
import tkinter as tk
import customtkinter as ctk

rootDir = 'C:\\Users\\Gatis\\Documents\\GitHub\\Tkinter-Learning-Project\\Windows9\\System33'  # Temp. solution
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

os.chdir(f'{rootDir}\\Files')

# Window Setup
window = ctk.CTk()
window.title('File Explorer')
winWidth = int(screenWidth * 0.3)
winHeight = int(screenHeight * 0.3)
window.geometry(f'{winWidth}x{winHeight}')

class Menu(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=window)
        self.place(x=0, y=0, relwidth=1, relheight=0.15)

        self.back = ctk.CTkButton(self, text='<-', command=self.go_back)
        self.back.place(relx=0.01, rely=0.5, relwidth=0.05, relheight=0.5, anchor='w')

        self.forward = ctk.CTkButton(self, text='->', command=self.go_forward)
        self.forward.place(relx=0.06, rely=0.5, relwidth=0.05, relheight=0.5, anchor='w')

        self.up = ctk.CTkButton(self, text='^', command=self.go_up)
        self.up.place(relx=0.12, rely=0.5, relwidth=0.05, relheight=0.5, anchor='w')

        self.refresh = ctk.CTkButton(self, text='@', command=Menu.refresh)
        self.refresh.place(relx=0.18, rely=0.5, relwidth=0.05, relheight=0.5, anchor='w')

        self.directory = tk.StringVar(value=os.getcwd())
        self.dirEntry = ctk.CTkEntry(self, textvariable=self.directory)
        self.dirEntry.place(relx=0.25, rely=0.5, relwidth=0.7, relheight=0.3, anchor='w')

        self.dirHist = [f'{rootDir}\\Files']
        self.fwdDirs = []

    def go_back(self):
        if len(self.dirHist) > 1:
            self.directory.set(self.dirHist[-1])
            self.fwdDirs.append(os.getcwd())
            self.dirHist.remove(self.dirHist[-1])

            os.chdir(self.directory.get())
            Item.update_items()
        elif len(self.dirHist) == 1 and not self.dirHist[0] == os.getcwd():
            self.directory.set(self.dirHist[-1])
            self.fwdDirs.append(os.getcwd())

            os.chdir(self.directory.get())
            Item.update_items()

        print('\nDirectory History:')
        for directory in self.dirHist:
            print(directory)

        print('\nForward Directories:')
        for directory in self.fwdDirs:
            print(directory)

    def go_forward(self):
        print('\nForward Directories:')
        for directory in self.fwdDirs:
            print(directory)

        if len(self.fwdDirs) > 0:
            self.directory.set(self.fwdDirs[-1])

            if not os.getcwd() == menu.dirHist[-1]:
                menu.dirHist.append(os.getcwd())

            self.fwdDirs.remove(self.fwdDirs[-1])

            os.chdir(self.directory.get())

        Item.update_items()

    def go_up(self):
        up_dir = self.directory.get()[:self.directory.get().rindex('\\')]
        print(up_dir)

        if not up_dir == rootDir:
            if not os.getcwd() == menu.dirHist[-1]:
                menu.dirHist.append(os.getcwd())

            menu.directory.set(up_dir)
            os.chdir(self.directory.get())
            Item.update_items()


    @staticmethod
    def refresh():
        Item.update_items()

menu = Menu()

class Directories(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=window, border_width=2)
        self.place(x=0, rely=0.15, relwidth=0.2, relheight=0.85)

        self.qckAccLabel = ctk.CTkLabel(self, text="Quick Access")
        self.qckAccLabel.place(relx=0.5, rely=0.01, anchor='n')

        self.qckAccFrame = ctk.CTkFrame(self)
        self.qckAccFrame.place(relx=0.5, rely=0.08, relwidth=0.98, relheight=0.3, anchor='n')

directories = Directories()

class QuickAccess(ctk.CTkButton):
    def __init__(self, name):
        super().__init__(master=directories.qckAccFrame,
                         text=name,
                         command=self.switch_directory,
                         anchor='w',
                         fg_color='grey')

        self.name = name
        self.directory = f'{rootDir}\\Files\\{self.name}'

        self.pack(fill='x')

    def switch_directory(self):
        if not os.getcwd() == menu.dirHist[-1]:
            menu.dirHist.append(os.getcwd())

        menu.directory.set(self.directory)
        os.chdir(self.directory)

        Item.update_items()

desktopBtn = QuickAccess('Desktop')

class Main(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=window, border_width=2)
        self.place(relx=0.2, rely=0.15, relwidth=0.8, relheight=0.85)

    items = []

main = Main()

class Item(ctk.CTkButton):
    def __init__(self, name):
        super().__init__(master=main,
                         text=name,
                         command=self.change_directory,
                         anchor='w',
                         fg_color='grey')

        self.pack(fill='x')

        self.name = name
        self.directory = f'{os.getcwd()}\\{self.name}'

    @classmethod
    def update_items(cls):
        for item in main.items:
            item.destroy()

        main.items.clear()

        for item in os.listdir():
            main.items.append(Item(item))

        print(f'\n{main.items}')

    def change_directory(self):
        if not os.getcwd() == menu.dirHist[-1]:
            menu.dirHist.append(os.getcwd())

        if os.path.isfile(self.directory):
            os.startfile(self.directory)
        else:
            menu.directory.set(self.directory)
            os.chdir(self.directory)

            Item.update_items()

        print('\nDirectory History:')
        for directory in menu.dirHist:
            print(directory)


Item.update_items()

window.mainloop()