import os
import json
import shutil
import tkinter as tk
from tkinter import messagebox
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

os.chdir(f'{rootDir}\\Files')

# Window Setup
window = ctk.CTk()
window.title('File Explorer')
winWidth = int(screenWidth * 0.3)
winHeight = int(screenHeight * 0.3)
window.geometry(f'{winWidth}x{winHeight}')
window.resizable(False, False)

class Menu(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=window)
        self.place(x=0, y=0, relwidth=1, relheight=0.15)

        self.back = ctk.CTkButton(self, text='<-', command=self.go_back, state='disabled')
        self.back.place(relx=0.01, rely=0.5, relwidth=0.05, relheight=0.5, anchor='w')

        self.forward = ctk.CTkButton(self, text='->', command=self.go_forward, state='disabled')
        self.forward.place(relx=0.06, rely=0.5, relwidth=0.05, relheight=0.5, anchor='w')

        self.up = ctk.CTkButton(self, text='^', command=self.go_up, state='disabled')
        self.up.place(relx=0.12, rely=0.5, relwidth=0.05, relheight=0.5, anchor='w')

        self.refresh = ctk.CTkButton(self, text='@', command=Menu.refresh)
        self.refresh.place(relx=0.18, rely=0.5, relwidth=0.05, relheight=0.5, anchor='w')

        self.directory = tk.StringVar(value=os.getcwd())
        self.dirEntry = ctk.CTkEntry(self, textvariable=self.directory)
        self.dirEntry.place(relx=0.25, rely=0.5, relwidth=0.7, relheight=0.3, anchor='w')

        self.dirHist = [f'{rootDir}\\Files']
        self.fwdDirs = []

        self.upDir = ''

    def go_back(self):
        up_dir = menu.directory.get()[:menu.directory.get().rindex('\\')]
        if not up_dir == rootDir:
            menu.up.configure(state='normal')

        menu.forward.configure(state='normal')
        if len(self.dirHist) > 1:
            self.directory.set(self.dirHist[-1])
            self.fwdDirs.append(os.getcwd())
            menu.forward.configure(state='normal')
            self.dirHist.remove(self.dirHist[-1])

            os.chdir(self.directory.get())
            Item.update_items()
        elif len(self.dirHist) == 1 and not self.dirHist[0] == os.getcwd():
            menu.back.configure(state='disabled')
            self.directory.set(self.dirHist[-1])
            self.fwdDirs.append(os.getcwd())

            os.chdir(self.directory.get())
            Item.update_items()

        self.update_up_dir()

        print('\nAfter back')
        print('Directory History:')
        for directory in self.dirHist:
            print(directory)
        print('\nForward Directories:')
        for directory in self.fwdDirs:
            print(directory)
        print('\nUp Dir:')
        print(self.upDir)

    def go_forward(self):
        up_dir = menu.directory.get()[:menu.directory.get().rindex('\\')]
        if not up_dir == rootDir:
            menu.up.configure(state='normal')

        menu.back.configure(state='normal')

        if len(self.fwdDirs) > 0:
            print('Fwd Dirs > 1')
            self.directory.set(self.fwdDirs[-1])

            if not os.getcwd() == menu.dirHist[-1]:
                menu.dirHist.append(os.getcwd())

            self.fwdDirs.remove(self.fwdDirs[-1])

            os.chdir(self.directory.get())

        if len(self.fwdDirs) < 1:
            menu.forward.configure(state='disabled')

        Item.update_items()

        self.update_up_dir()

        print('\nAfter forward')
        print('Directory History:')
        for directory in self.dirHist:
            print(directory)
        print('\nForward Directories:')
        for directory in self.fwdDirs:
            print(directory)
        print('\nUp Dir:')
        print(self.upDir)

    def go_up(self):
        menu.back.configure(state='normal')
        menu.forward.configure(state='disabled')

        if not self.upDir == rootDir:
            self.fwdDirs.clear()
            if not os.getcwd() == menu.dirHist[-1]:
                menu.dirHist.append(os.getcwd())

            menu.directory.set(self.upDir)
            os.chdir(self.directory.get())
            Item.update_items()

        self.upDir = menu.directory.get()[:menu.directory.get().rindex('\\')]
        if self.upDir == rootDir:
            menu.up.configure(state='disabled')

        print('\nUp Dir:')
        print(menu.upDir)

    def update_up_dir(self):
        self.upDir = menu.directory.get()[:menu.directory.get().rindex('\\')]
        if self.upDir == rootDir:
            self.up.configure(state='disabled')
        else:
            self.up.configure(state='normal')
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
        menu.back.configure(state='normal')
        if not os.getcwd() == menu.dirHist[-1]:
            menu.dirHist.append(os.getcwd())

        menu.directory.set(self.directory)
        os.chdir(self.directory)

        menu.update_up_dir()
        print('\nUp Dir:')
        print(menu.upDir)

        Item.update_items()

desktopBtn = QuickAccess('Desktop')

class Main(ctk.CTkScrollableFrame):
    def __init__(self):
        super().__init__(master=window, border_width=2)
        self.place(relx=0.2, rely=0.15, relwidth=0.8, relheight=0.85)

        self.file_name = tk.StringVar(value='')
        self.extension = ''
        self.entry = ctk.CTkEntry(self, textvariable=self.file_name)
        self.entry_packed = False


    items = []

    @classmethod
    def hide_entry(cls, event):
        name_entry = main.entry.get()
        extension = main.extension
        name_entry = name_entry.translate({ord(i): None for i in '*"/\\<>:|?.'})
        name_entry = name_entry.strip(' ')

        if name_entry == '':
            match main.extension:
                case '':
                    name_entry = 'New Folder'
                    main.entry.insert(0, name_entry)
                case '.txt':
                    name_entry = 'New Text File'
                    main.entry.insert(0, name_entry)
                case '.docx':
                    name_entry = 'New Word Document'
                    main.entry.insert(0, name_entry)
                case '.xlsx':
                    name_entry = 'New Excel Document'
                    main.entry.insert(0, name_entry)
                case '.pptx':
                    name_entry = 'New PowerPoint Document'
                    main.entry.insert(0, name_entry)

        file_dict = os.listdir(menu.directory.get())

        if f'{name_entry}{extension}' in file_dict:
            messagebox.showerror('Error', 'File name taken')
            raise Exception('File name taken')
        else:
            main.file_name.set(f'{name_entry}{extension}')

        main.entry.pack_forget()
        main.entry_packed = False

    @classmethod
    def name_file(cls):
        if main.entry_packed:
            window.after(10, cls.name_file)
            entry = main.entry.get().translate({ord(i): None for i in '*"/\\<>:|?.'})
            main.entry.delete(0, 'end')
            main.entry.insert(0, entry)
            if len(main.entry.get()) > 24:
                main.entry.delete(24, tk.END)
        else:
            os.chdir(menu.directory.get())
            if main.extension == '':
                os.makedirs(main.file_name.get())
            else:
                with open(main.file_name.get(), 'w'):
                    pass

            Item.update_items()

            if os.getcwd() == f'{rootDir}\\Files\\Desktop':
                print('\nDesktop File:')
                os.chdir(f'{rootDir}\\System Info')

                with open('files.json', 'r') as files:
                    file_dict = json.load(files)

                file_values = file_dict.values()

                column = 0
                row = 0
                value = f'{column}-{row}'

                while not value == '24-13':
                    if value not in file_values:
                        file_dict.update({main.file_name.get(): value})
                        with open('files.json', 'w') as files:
                            json.dump(file_dict, files)
                        break
                    else:
                        print(value)
                        if row < 14:
                            if column < 24:
                                column += 1
                                value = f'{column}-{row}'
                            else:
                                row += 1
                                column = 0
                                value = f'{column}-{row}'
                        else:
                            raise Exception('Too many desktop files')

                print(main.file_name.get())
                os.chdir(menu.directory.get())
                print(os.getcwd())

            window.config(cursor='')

    @classmethod
    def create_file(cls, extension):
        main.entry.pack(fill='x', pady=2, padx=12)
        main.entry_packed = True
        main.extension = extension

        match extension:
            case '':
                main.file_name.set('New Folder')
            case '.txt':
                main.file_name.set('New Text File')
            case '.docx':
                main.file_name.set('New Word Document')
            case '.xlsx':
                main.file_name.set('New Excel Document')
            case '.pptx':
                main.file_name.set('New PowerPoint Document')

        window.bind('<Return>', cls.hide_entry)
        main.entry.focus_force()
        main.entry.select_range(0, tk.END)

        window.config(cursor='none')

        Main.name_file()


main = Main()

class Item(ctk.CTkButton):
    def __init__(self, name):
        super().__init__(master=main,
                         text=name,
                         command=self.change_directory,
                         anchor='w',
                         fg_color='grey')

        self.pack(fill='x', pady=2, padx=12)

        self.name = name
        self.directory = f'{os.getcwd()}\\{self.name}'
        self.extension = ''

    @classmethod
    def update_items(cls):
        for item in main.items:
            item.destroy()

        main.items.clear()

        for item in os.listdir(menu.directory.get()):
            main.items.append(Item(item))

        for button in main.items:
            split_file_name = button.name.split('.')

            if len(split_file_name) > 1:
                extension = split_file_name[1]
                button.extension = f'.{extension}'
                match extension:
                    case 'txt':
                        button.configure(fg_color='white')
                        button.configure(text_color='black')
                    case 'docx':
                        button.configure(fg_color='blue')
                    case 'xlsx':
                        button.configure(fg_color='green')
                    case 'pptx':
                        button.configure(fg_color='orange')
            else:
                button.configure(fg_color='khaki')
                button.configure(text_color='black')


    def change_directory(self):
        up_dir = menu.directory.get()[:menu.directory.get().rindex('\\')]
        if not up_dir == rootDir:
            menu.up.configure(state='normal')

        menu.back.configure(state='normal')
        if not os.getcwd() == menu.dirHist[-1] and not os.path.isfile(self.directory):
            menu.dirHist.append(os.getcwd())

        if os.path.isfile(self.directory):
            os.startfile(self.directory)
        else:
            menu.directory.set(self.directory)
            os.chdir(self.directory)

            Item.update_items()

        menu.update_up_dir()

        print('\nUp Dir:')
        print(menu.upDir)
        print('\nDirectory History:')
        for directory in menu.dirHist:
            print(directory)

    @classmethod
    def delete_file(cls):
        widget = contextMenu.selected_widget

        os.chdir(menu.directory.get())

        file_name = widget.name
        extension = widget.extension
        path = widget.directory

        if os.getcwd() == f'{rootDir}\\Files' and file_name == 'Desktop':
            messagebox.showerror('Error', 'Can\'t delete Desktop')
            raise Exception('Can\'t delete Desktop')

        if extension == '':
            if len(os.listdir(path)) == 0:
                shutil.rmtree(path)
            else:
                sure = tk.messagebox.askokcancel(title='Folder not empty',
                                                 message='This will delete the folder and all of its contents')
                if sure:
                    shutil.rmtree(path)
                else:
                    raise Exception('User not sure')
        else:
            os.remove(path)

        if path in menu.fwdDirs:
            menu.fwdDirs.remove(path)
            menu.forward.configure(state='disabled')

        Item.update_items()

Item.update_items()

class ContextMenu(tk.Menu):
    def __init__(self):
        super().__init__(window, tearoff=0)
        self.cMenuX = tk.IntVar(value=0)
        self.cMenuY = tk.IntVar(value=0)
        self.selected_widget = None
        self.widget_class = None

        self.newSubMenu = tk.Menu(self, tearoff=False)

    def select_widget(self, event):
        self.cMenuX.set(event.x_root)
        self.cMenuY.set(event.y_root)

        self.selected_widget = event.widget.winfo_containing(self.cMenuX.get(), self.cMenuY.get())
        print(f'\nInitial Widget: {self.selected_widget}')

        while self.selected_widget is not None:
            if isinstance(self.selected_widget, Menu) or isinstance(self.selected_widget, Directories)\
                    or isinstance(self.selected_widget, QuickAccess) or isinstance(self.selected_widget, Item)\
                    or isinstance(self.selected_widget, Main):
                break
            self.selected_widget = self.selected_widget.master

        print(f'Selected widget: {self.selected_widget}')

        self.widget_class = self.selected_widget.__class__.__name__
        print(f'Widget class: {self.widget_class}')

    def add_options(self):
        self.delete(0, tk.END)
        self.newSubMenu.delete(0, tk.END)
        match self.widget_class:
            case 'Directories':
                self.add_command(label='Directories test')
            case 'QuickAccess':
                self.add_command(label='QuickAccess test')
            case 'Item':
                self.add_command(label='Delete', command=Item.delete_file)
            case 'NoneType':  # Sometimes selects this instead of 'Main' class, don't know why
                self.add_cascade(label='New', menu=self.newSubMenu)
                self.newSubMenu.add_command(label='Folder', command=lambda: Main.create_file(''))
                self.newSubMenu.add_separator()
                self.newSubMenu.add_command(label='Text File', command=lambda: Main.create_file('.txt'))
                self.newSubMenu.add_command(label='Word Document', command=lambda: Main.create_file('.docx'))
                self.newSubMenu.add_command(label='Excel Document', command=lambda: Main.create_file('.xlsx'))
                self.newSubMenu.add_command(label='PowerPoint Document', command=lambda: Main.create_file('.pptx'))
            case 'Main':
                self.add_cascade(label='New', menu=self.newSubMenu)
                self.newSubMenu.add_command(label='Folder', command=lambda: Main.create_file(''))
                self.newSubMenu.add_separator()
                self.newSubMenu.add_command(label='Text File', command=lambda: Main.create_file('.txt'))
                self.newSubMenu.add_command(label='Word Document', command=lambda: Main.create_file('.docx'))
                self.newSubMenu.add_command(label='Excel Document', command=lambda: Main.create_file('.xlsx'))
                self.newSubMenu.add_command(label='PowerPoint Document', command=lambda: Main.create_file('.pptx'))

    def open_menu(self, event):
        self.add_options()
        try:
            contextMenu.tk_popup(self.cMenuX.get(), self.cMenuY.get())
        finally:
            contextMenu.grab_release()

contextMenu = ContextMenu()

window.bind('<Button-3>', contextMenu.select_widget)
window.bind('<ButtonRelease-3>', contextMenu.open_menu)

window.mainloop()
