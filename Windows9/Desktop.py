import os
from subprocess import call
import ctypes
import json
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from time import strftime

ctypes.windll.shcore.SetProcessDpiAwareness(2)

# Check if system files exist
if not os.path.exists('System33'):
    print('Windows 9 is not installed! Please run the installer!')
    exit()

rootDir = f'{os.path.dirname(__file__)}\\System33'
os.chdir(f'{rootDir}\\System Info')

# Load system info
with open('sysinfo.json', 'r') as sysinfo:
    sysInfo = json.load(sysinfo)

    screenWidth = sysInfo['Screen Width']
    screenHeight = sysInfo['Screen Height']
    edition = sysInfo['Edition']

    print('\n\nSystem info')
    for item in sysInfo.items():
        print(item)

# Desktop
# Window setup
window = ctk.CTk()
window.title(edition)
window.geometry(f'{screenWidth}x{screenHeight}')
minWidth = int(screenWidth * 0.5)
minHeight = int(screenHeight * 0.5)
window.attributes('-fullscreen', 1)

# Load user settings
with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

    username = settings['Username']
    darkMode = settings['Dark Mode']

    print('\nSettings')
    for item in settings.items():
        print(item)

os.chdir(rootDir)

if darkMode:
    ctk.set_appearance_mode('dark')
else:
    ctk.set_appearance_mode('light')

def update_list(value, outdated_list):
    outdated_list.clear()
    for list_item in range(value):
        outdated_list.append(list_item)
    return outdated_list


class Desktop(ctk.CTkFrame):
    def __init__(self, column_count, row_count):
        super().__init__(master=window)
        self.place(x=0, y=0, relwidth=1, relheight=1)

        self.columns = column_count
        column_list = []
        column_list = update_list(self.columns, column_list)
        self.columnSize = int(screenWidth / self.columns)
        self.columnconfigure(column_list, weight=1, uniform='a')

        self.rows = row_count
        row_list = []
        row_list = update_list(self.rows, row_list)
        self.rowSize = int(screenHeight / self.rows)
        self.rowconfigure(row_list, weight=1, uniform='a')

        self.tiles = []

print('\nLoading desktop...')
desktop = Desktop(24, 15)

class Tile(ctk.CTkFrame):
    def __init__(self, tile_column, tile_row):
        super().__init__(master=desktop, fg_color='transparent', border_width=0)
        self.column = tile_column
        self.row = tile_row
        self.name = f'Tile {tile_column}-{tile_row}'
        self.empty = True

        self.pinned = False
        self.pinnedShortcut = None

        self.icon = ctk.CTkLabel(self, text='', fg_color='white')

        self.file_name = tk.StringVar(value='')
        self.file_label = ctk.CTkLabel(self,
                                       text=self.file_name.get(), font=('Helvetica', 10),
                                       justify='center')
        self.extension = ''

        self.entry = ctk.CTkEntry(self, textvariable=self.file_name, font=('Helvetica', 10))

        self.grid(row=tile_row, column=tile_column, sticky='nsew')

    selected_tile = None

    def __str__(self):
        return self.name

    @classmethod
    def create_tiles(cls, column_count, row_count):
        desktop.tiles = [[[] for _ in range(row_count)] for _ in range(column_count)]
        tile_column = 0
        tile_row = 0
        for current_row in range(row_count):
            for current_column in range(column_count):
                desktop.tiles[current_column][current_row].append(cls(tile_column, tile_row))
                tile_column += 1
            tile_column = 0
            tile_row += 1

    @classmethod
    def find_tile(cls, x_pos, y_pos):
        tile_column = int(x_pos / desktop.columnSize)
        if tile_column < 1:
            tile_column = 0
        if tile_column > desktop.columns:
            tile_column = desktop.columns

        tile_row = int(y_pos / desktop.rowSize)
        if tile_row < 1:
            tile_row = 0
        if tile_row > desktop.rows - 2:
            tile_row = desktop.rows - 2
        cls.selected_tile = desktop.tiles[tile_column][tile_row][0]
        return desktop.tiles[tile_column][tile_row][0]

    @staticmethod
    def load_desktop_files():
        print('\nLoading desktop files...\n')
        os.chdir(f'{rootDir}\\System Info')
        with open('files.json', 'r') as files:
            file_dict = json.load(files)

        files_found = 0
        for item in file_dict:
            column = int(file_dict[item].split('-')[0])
            row = int(file_dict[item].split('-')[1])

            tile = desktop.tiles[column][row][0]

            print(f'{item} in {tile.name}')

            tile.empty = False

            split_file_name = item.split('.')

            if len(split_file_name) > 1:
                match split_file_name[1]:
                    case 'txt':
                        tile.icon.configure(text='Txt')
                        tile.icon.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.5, anchor='n')
                        tile.extension = '.txt'
                    case 'docx':
                        tile.icon.configure(text='W')
                        tile.icon.configure(text_color='white')
                        tile.icon.configure(fg_color='blue')
                        tile.icon.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.5, anchor='n')
                    case 'xlsx':
                        tile.icon.configure(text='E')
                        tile.icon.configure(text_color='white')
                        tile.icon.configure(fg_color='green')
                        tile.icon.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.5, anchor='n')
                    case 'pptx':
                        tile.icon.configure(text='P')
                        tile.icon.configure(text_color='white')
                        tile.icon.configure(fg_color='orange')
                        tile.icon.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.5, anchor='n')
            else:
                tile.icon.configure(fg_color='khaki')
                tile.icon.place(relx=0.5, rely=0.1, relwidth=0.7, relheight=0.5, anchor='n')

            tile.file_name.set(item)
            tile.file_label.configure(textvariable=tile.file_name)
            tile.file_label.place(relx=0.5, rely=0.7, anchor='n', relwidth=1, relheight=0.2)

            files_found += 1
        if files_found == 0:
            print('No files found.')
        else:
            print(f'\nLoaded {files_found} files')
            print('Done')

    @classmethod
    def open_file(cls):
        selected_tile = cls.selected_tile
        os.chdir(f'{rootDir}\\Files\\Desktop')
        file_name = selected_tile.file_name.get()
        file_path = f'{os.getcwd()}\\{file_name}'
        os.startfile(file_path)
        os.chdir(rootDir)

    # Desktop file creation
    # noinspection PyUnusedLocal
    @classmethod
    def hide_entry(cls, event):
        name_entry = cls.selected_tile.entry.get()
        extension = cls.selected_tile.extension
        name_entry = name_entry.translate({ord(i): None for i in '*"/\\<>:|?'})
        name_entry = name_entry.strip(' ')

        if name_entry == '':
            match cls.selected_tile.extension:
                case '':
                    name_entry = 'New Folder'
                    cls.selected_tile.entry.insert(0, name_entry)
                case '.txt':
                    name_entry = 'New Text File'
                    cls.selected_tile.entry.insert(0, name_entry)

        os.chdir(f'{rootDir}\\System Info')
        with open('files.json', 'r') as files:
            file_dict = json.load(files)

        if f'{name_entry}{extension}' in file_dict:
            messagebox.showerror('Error', 'File name taken')
            raise Exception('File name taken')
        else:
            cls.selected_tile.file_name.set(f'{name_entry}{extension}')

        cls.selected_tile.entry.place_forget()
        cls.selected_tile.file_label.configure(textvariable=cls.selected_tile.file_name)
        cls.selected_tile.file_label.place(relx=0.5, rely=0.7, anchor='n', relwidth=1, relheight=0.2)

    @classmethod
    def name_file(cls):
        if cls.selected_tile.entry.place_info():
            window.after(50, cls.name_file)

            if len(cls.selected_tile.entry.get()) > 10:
                cls.selected_tile.entry.delete(10, tk.END)
        else:
            os.chdir(f'{rootDir}\\Files\\Desktop')
            if cls.selected_tile.extension == '':
                os.makedirs(cls.selected_tile.file_name.get())
            else:
                with open(cls.selected_tile.file_name.get(), 'w'):
                    pass

            os.chdir(f'{rootDir}\\System Info')
            with open('files.json', 'r') as files:
                file_dict = json.load(files)
            file_dict.update({cls.selected_tile.file_name.get(): f'{cls.selected_tile.column}-{cls.selected_tile.row}'})
            with open('files.json', 'w') as files:
                json.dump(file_dict, files)

            os.chdir(rootDir)

            window.config(cursor='')

    @classmethod
    def create_file(cls, extension):
        selected_tile = cls.selected_tile

        selected_tile.extension = extension
        selected_tile.empty = False

        match extension:
            case '':
                selected_tile.icon.configure(fg_color='khaki')
                selected_tile.icon.place(relx=0.5, rely=0.1, relwidth=0.7, relheight=0.5, anchor='n')

                selected_tile.file_name.set('New Folder')
            case '.txt':
                selected_tile.icon.configure(text='Txt')
                selected_tile.icon.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.5, anchor='n')

                selected_tile.file_name.set('New Text File')
            case '.docx':
                selected_tile.icon.configure(text='W')
                selected_tile.icon.configure(text_color='white')
                selected_tile.icon.configure(fg_color='blue')
                selected_tile.icon.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.5, anchor='n')

                selected_tile.file_name.set('New Word Document')
            case '.xlsx':
                selected_tile.icon.configure(text='E')
                selected_tile.icon.configure(text_color='white')
                selected_tile.icon.configure(fg_color='green')
                selected_tile.icon.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.5, anchor='n')

                selected_tile.file_name.set('New Excel Document')
            case '.pptx':
                selected_tile.icon.configure(text='P')
                selected_tile.icon.configure(text_color='white')
                selected_tile.icon.configure(fg_color='orange')
                selected_tile.icon.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.5, anchor='n')

                selected_tile.file_name.set('New PowerPoint Document')

        selected_tile.entry.place(relx=0.5, rely=0.65, relheight=0.35, relwidth=0.99, anchor='n')
        window.bind('<Return>', cls.hide_entry)
        selected_tile.entry.focus_force()
        selected_tile.entry.select_range(0, tk.END)

        window.config(cursor='none')

        Tile.name_file()

    @classmethod
    def delete_file(cls):
        selected_tile = cls.selected_tile

        os.chdir(f'{rootDir}\\Files\\Desktop')
        file_name = selected_tile.file_name.get()
        file_path = f'{os.getcwd()}\\{file_name}'

        if selected_tile.extension == '':
            os.rmdir(file_path)
        else:
            os.remove(file_path)

        os.chdir(f'{rootDir}\\System Info')
        with open('files.json', 'r') as files:
            file_dict = json.load(files)
        del file_dict[selected_tile.file_name.get()]
        with open('files.json', 'w') as files:
            json.dump(file_dict, files)

        os.chdir(rootDir)

        selected_tile.icon.place_forget()
        selected_tile.file_label.place_forget()
        selected_tile.empty = True

        if selected_tile.pinned:
            selected_tile.pinned = False

            selected_tile.pinnedShortcut.empty = True
            selected_tile.pinnedShortcut.configure(text='Empty Shortcut')
            selected_tile.pinnedShortcut.configure(state='disabled')


Tile.create_tiles(desktop.columns, desktop.rows - 1)
print('Done')
Tile.load_desktop_files()

# Taskbar
class Taskbar(ctk.CTkFrame):
    def __init__(self):
        super().__init__(window, border_width=1)
        self.place(x=0, rely=0.955, relwidth=1, relheight=0.05)

        self.timeLabel = ctk.CTkLabel(master=self)
        self.timeLabel.pack(side='right', padx=5)
        self.timeLabel.bind('<Activate>', self.update_time)
        self.update_time()

        self.startButton = ctk.CTkButton(master=self, text='Start')
        self.startButton.pack(side='left', padx=5)

    def update_time(self):
        time_string = strftime('%H:%M:%S')
        self.timeLabel.configure(text=time_string)
        self.timeLabel.after(1000, self.update_time)

taskbarWid = Taskbar()

# Start menu
class StartMenu(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=window,
                         border_width=1)
        # self.place(x=0, rely=0.555, relwidth=0.15, relheight=0.4)
        self.place(x=0, rely=0.555, relwidth=0.2, relheight=0.4)

        self.starMenuText = f'{edition} Edition'
        self.startLabel = ctk.CTkLabel(master=self, text=self.starMenuText, anchor='center')
        self.startLabel.place(relx=0.02, rely=0.01)

        self.itemContainer = ctk.CTkFrame(master=self)
        self.itemContainer.place(x=0, rely=0.1, relwidth=1, relheight=0.75)

        self.shutDownButton = ctk.CTkButton(master=self,
                                            text='Shut down',
                                            command=lambda: window.destroy())
        self.shutDownButton.place(relx=0.05, rely=0.95, anchor='sw')

        self.appsButton = ctk.CTkButton(master=self, text='Apps')
        self.appsButton.place(relx=0.95, rely=0.95, anchor='se')

        self.lower()

    startMenuEnabled = False

    def toggle_start_menu(self):
        if self.startMenuEnabled:
            self.startMenuEnabled = False
            self.lower()

            appMenu.lower()
            Apps.appsEnabled = False
        else:
            self.startMenuEnabled = True
            self.lift()


startMenu = StartMenu()
taskbarWid.startButton.configure(command=startMenu.toggle_start_menu)

class Shortcut(ctk.CTkButton):
    def __init__(self, number):
        super().__init__(master=startMenu.itemContainer,
                         text='Empty Shortcut',
                         command=self.open_shortcut,
                         state='disabled',
                         anchor='w')
        self.pack(expand=True, fill='both', padx=1, pady=1)

        self.name = f'StartItem{number}'
        self.empty = True
        self.fileName = ''
        self.path = ''

    def __str__(self):
        return self.name

    ItemList = []

    @classmethod
    def load_shortcuts(cls):
        os.chdir(f'{rootDir}\\System Info')

        with open('files.json', 'r') as files:
            file_dict = json.load(files)

        with open('start.json', 'r') as files:
            start_dict = json.load(files)

        print('\nLoading Start Menu shortcuts:')
        for item in start_dict:
            print(f'{item} in {start_dict[item]}')

            column = int(file_dict[item].split('-')[0])
            row = int(file_dict[item].split('-')[1])
            tile = desktop.tiles[column][row][0]

            shortcut = cls.ItemList[int(start_dict[item].replace('StartItem', '')) - 1]

            tile.pinned = True
            tile.pinnedShortcut = shortcut

            path = f'{rootDir}\\Files\\Desktop\\{tile.file_name.get()}'
            shortcut.empty = False
            shortcut.fileName = tile.file_name.get()
            shortcut.path = path
            shortcut.configure(state='normal')
            shortcut.configure(text=tile.file_name.get())

        print('Done')

    def open_shortcut(self):
        os.startfile(self.path)

    @classmethod
    def pin_to_start(cls):
        tile = Tile.selected_tile
        for shortcut in cls.ItemList:
            if shortcut.empty:
                print(tile)
                path = f'{rootDir}\\Files\\Desktop\\{tile.file_name.get()}'
                print(tile)
                print(path)

                tile.pinned = True
                tile.pinnedShortcut = shortcut

                shortcut.empty = False
                shortcut.fileName = tile.file_name.get()
                shortcut.path = path
                shortcut.configure(state='normal')
                shortcut.configure(text=tile.file_name.get())

                os.chdir(f'{rootDir}\\System Info')
                with open('start.json', 'r') as files:
                    start_dict = json.load(files)

                start_dict.update({tile.file_name.get(): str(shortcut)})

                with open(f'start.json', 'w') as start:
                    json.dump(start_dict, start)
                break
            else:
                print(f'{shortcut} taken')

    @classmethod
    def remove_shortcut(cls):
        shortcut = contextMenu.selected_widget

        os.chdir(f'{rootDir}\\System Info')
        with open('files.json', 'r') as files:
            file_dict = json.load(files)

        column = int(file_dict[shortcut.fileName].split('-')[0])
        row = int(file_dict[shortcut.fileName].split('-')[1])

        tile = desktop.tiles[column][row][0]
        tile.pinned = False

        shortcut.empty = True
        shortcut.configure(text='Empty Shortcut')
        shortcut.configure(state='disabled')

        with open('start.json', 'r') as files:
            start_dict = json.load(files)

        del start_dict[shortcut.fileName]
        with open('start.json', 'w') as files:
            json.dump(start_dict, files)

for item in range(1, 7):
    Shortcut.ItemList.append(Shortcut(item))

Shortcut.load_shortcuts()
print('------------------------------------------------')

class Apps(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=window)
        self.place(relx=0.2, rely=0.555, relwidth=0.175, relheight=0.4)

        self.appsLabel = ctk.CTkLabel(master=self, text='Apps', anchor='center', fg_color='grey')
        self.appsLabel.pack(pady=2)

        self.appItemContainer = ctk.CTkFrame(master=self)
        self.appItemContainer.pack(expand=True, fill='both', padx=1, pady=2)

        self.lower()

        self.appsEnabled = False

    def toggle_app_menu(self):
        if self.appsEnabled:
            self.lower()
            self.appsEnabled = False
        else:
            self.lift()
            self.appsEnabled = True
            print(self.appsEnabled)

appMenu = Apps()
startMenu.appsButton.configure(command=appMenu.toggle_app_menu)

class AppButton(ctk.CTkButton):
    def __init__(self, app_name):
        super().__init__(master=appMenu.appItemContainer, text=app_name, command=self.open_app)

        self.pack(pady=1)

        self.fileName = f'{app_name}.py'

    def open_app(self):
        os.chdir(f'{rootDir}\\Programs')

        call(["python", f'{self.fileName}'])

        os.chdir(rootDir)

settingsButton = AppButton('Settings')
fileExplorerButton = AppButton('File Explorer')

# Context Menu
# noinspection PyUnusedLocal
class ContextMenu(tk.Menu):
    def __init__(self):
        super().__init__(window, tearoff=0)
        self.cMenuX = tk.IntVar(value=0)
        self.cMenuY = tk.IntVar(value=0)

        self.newSubMenu = tk.Menu(self, tearoff=False)

        self.selected_widget = None
        self.widget_class = None

    def select_widget(self, event):
        self.cMenuX.set(event.x_root)
        self.cMenuY.set(event.y_root)

        self.selected_widget = event.widget.winfo_containing(self.cMenuX.get(), self.cMenuY.get())
        print(f'\nInitial Widget: {self.selected_widget}')

        while self.selected_widget is not None:
            if isinstance(self.selected_widget, Taskbar) or isinstance(self.selected_widget, Shortcut)\
                    or isinstance(self.selected_widget, StartMenu) or isinstance(self.selected_widget, Apps)\
                    or isinstance(self.selected_widget, Tile):
                break
            self.selected_widget = self.selected_widget.master

        print(f'Selected widget: {self.selected_widget}')

        self.widget_class = self.selected_widget.__class__.__name__
        if self.widget_class == 'Tile':
            Tile.selected_tile = self.selected_widget
        print(f'Widget class: {self.widget_class}')

    def add_options(self):
        self.delete(0, tk.END)
        self.newSubMenu.delete(0, tk.END)
        match self.widget_class:
            case 'Tile':
                if self.selected_widget.empty:
                    self.add_cascade(label='New', menu=self.newSubMenu)
                    self.newSubMenu.add_command(label='Folder', command=lambda: Tile.create_file(''))
                    self.newSubMenu.add_separator()
                    self.newSubMenu.add_command(label='Text File', command=lambda: Tile.create_file('.txt'))
                    self.newSubMenu.add_command(label='Word Document', command=lambda: Tile.create_file('.docx'))
                    self.newSubMenu.add_command(label='Excel Document', command=lambda: Tile.create_file('.xlsx'))
                    self.newSubMenu.add_command(label='PowerPoint Document', command=lambda: Tile.create_file('.pptx'))

                else:
                    self.add_command(label='Open', command=Tile.open_file)
                    self.add_command(label='Delete', command=Tile.delete_file)
                    self.add_separator()
                    if not self.selected_widget.pinned:
                        self.add_command(label='Pin to Start ', command=Shortcut.pin_to_start)
                    else:
                        self.add_command(label='Pin to Start ', command=Shortcut.pin_to_start, state='disabled')
            case 'Taskbar':
                self.add_command(label='Taskbar test')
            case 'StartMenu':
                self.add_command(label='StarMenu test')
            case 'Shortcut':
                if self.selected_widget.empty:
                    self.add_command(label='Empty shortcut test')
                else:
                    self.add_command(label='Remove Shortcut', command=Shortcut.remove_shortcut)
            case 'Apps':
                self.add_command(label='Apps menu test')
            case 'NoneType':
                selected_tile = Tile.find_tile(contextMenu.cMenuX.get(), contextMenu.cMenuY.get())
                if selected_tile.empty:
                    self.add_cascade(label='New', menu=self.newSubMenu)
                    self.newSubMenu.add_command(label='Folder', command=lambda: Tile.create_file(''))
                    self.newSubMenu.add_separator()
                    self.newSubMenu.add_command(label='Text File', command=lambda: Tile.create_file('.txt'))
                    self.newSubMenu.add_command(label='Word Document', command=lambda: Tile.create_file('.docx'))
                    self.newSubMenu.add_command(label='Excel Document', command=lambda: Tile.create_file('.xlsx'))
                    self.newSubMenu.add_command(label='PowerPoint Document', command=lambda: Tile.create_file('.pptx'))
                else:
                    self.add_command(label='Settings', command=ContextMenu.open_settings)
        menu_length = self.index('end') + 1
        if menu_length > 0:
            self.add_separator()
        self.add_command(label='Settings', command=ContextMenu.open_settings)
        print(f'\nMenu length: {menu_length}')

    def open_menu(self, event):
        self.add_options()
        try:
            contextMenu.tk_popup(self.cMenuX.get(), self.cMenuY.get())
        finally:
            contextMenu.grab_release()

    @staticmethod
    def open_settings():
        os.chdir(f'{rootDir}\\Programs')

        call(["python", 'Settings.py'])

        os.chdir(rootDir)

contextMenu = ContextMenu()

window.bind('<Button-3>', contextMenu.select_widget)
window.bind('<ButtonRelease-3>', contextMenu.open_menu)

# Debug menu and button
class Debug(ctk.CTkFrame):
    def __init__(self):
        super().__init__(window, border_width=1)
        self.enabled = False
        self.place(x=0, y=0)
        self.lower()

        self.debug_button = ctk.CTkButton(master=taskbarWid, text='Debug Menu', command=self.toggle_menu)
        self.debug_button.pack(side='left')

        self.fullscreenBool = tk.BooleanVar(value=True)
        self.fullscreenCheck = ctk.CTkCheckBox(
            master=self,
            text='Fullscreen',
            command=self.fullscreen_toggle,
            variable=self.fullscreenBool)
        self.fullscreenCheck.pack(side='top', padx=5, pady=5)

        self.taskbarBool = tk.BooleanVar(value=True)
        self.taskbarCheck = ctk.CTkCheckBox(
            master=self,
            text='Taskbar',
            command=self.taskbar_toggle,
            variable=self.taskbarBool)
        self.taskbarCheck.pack(side='top', padx=5, pady=5)

        self.tileLabel = ctk.CTkLabel(self, text='Tile Options')
        self.tileLabel.pack(side='top', padx=5, pady=5)

        self.bordersBool = tk.BooleanVar(value=False)
        self.bordersCheck = ctk.CTkCheckBox(
            master=self,
            text='Tile Borders',
            command=self.toggle_tile_borders,
            variable=self.bordersBool)
        self.bordersCheck.pack(side='top', padx=5, pady=5)

        self.labelsBool = tk.BooleanVar(value=False)
        self.labelsCheck = ctk.CTkCheckBox(
            master=self,
            text='Label Background',
            command=self.toggle_label_background,
            variable=self.labelsBool)
        self.labelsCheck.pack(side='top', padx=5, pady=5)

    def toggle_menu(self):
        if self.enabled:
            self.enabled = False
            self.lower()
        else:
            self.enabled = True
            self.lift()
    def fullscreen_toggle(self):
        if self.fullscreenBool.get():
            window.attributes('-fullscreen', 1)
            self.fullscreenBool.set(True)
        else:
            window.attributes('-fullscreen', 0)
            self.fullscreenBool.set(False)
        print(window.winfo_width())
    def taskbar_toggle(self):
        if self.taskbarBool.get():
            self.taskbarBool.set(True)
            taskbarWid.place(x=0, rely=0.955, relwidth=1, relheight=0.045)
            taskbarWid.startButton.pack(side='left', padx=5)
            self.debug_button.pack(side='left')
            taskbarWid.timeLabel.pack(side='right', padx=5)
        else:
            self.taskbarBool.set(False)
            taskbarWid.place_forget()

    def toggle_tile_borders(self):
        if self.bordersBool.get():
            self.bordersBool.set(True)
            for row in desktop.tiles:
                for tile in row:
                    tile = tile[0]
                    tile.configure(border_width=1)
        else:
            self.bordersBool.set(False)
            for row in desktop.tiles:
                for tile in row:
                    tile = tile[0]
                    tile.configure(border_width=0)

    def toggle_label_background(self):
        if self.labelsBool.get():
            self.labelsBool.set(True)
            for row in desktop.tiles:
                for tile in row:
                    tile = tile[0]
                    if not tile.empty:
                        tile.file_label.configure(bg_color='red')
        else:
            self.labelsBool.set(False)
            for row in desktop.tiles:
                for tile in row:
                    tile = tile[0]
                    if not tile.empty:
                        tile.file_label.configure(bg_color='transparent')
debugMenu = Debug()


window.mainloop()
