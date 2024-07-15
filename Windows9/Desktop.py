import os
from subprocess import call
import ctypes
import json
import tkinter as tk
import customtkinter as ctk
from time import strftime
from random import choice

ctypes.windll.shcore.SetProcessDpiAwareness(2)

# Check if system files exist
if not os.path.exists('System33'):
    print('Windows 9 is not installed! Please run the installer!')
    exit()

rootDir = f'{os.getcwd()}\\System33'
os.chdir(rootDir)


# Load system info
with open('sysinfo.json', 'r') as sysinfo:
    sysInfo = json.load(sysinfo)

    screenWidth = sysInfo['Screen Width']
    screenHeight = sysInfo['Screen Height']
    edition = sysInfo['Edition']

    print('\n\nSystem info')
    for item in sysInfo.items():
        print(item)

class NewWindow(ctk.CTkToplevel):  # The window always minimizes on creation for some reason
    def __init__(self, window_title, width, height, min_width, min_height):
        super().__init__()
        self.title(window_title)
        self.geometry(f'{width}x{height}')
        self.minsize(min_width, min_height)


# Window setup
window = ctk.CTk()
window.title(edition)
window.geometry(f'{screenWidth}x{screenHeight}')
minWidth = int(screenWidth * 0.5)
minHeight = int(screenHeight * 0.5)
window.attributes('-fullscreen', 1)

def update_list(value, outdated_list):
    outdated_list.clear()
    for list_item in range(value):
        outdated_list.append(list_item)
    return outdated_list


# Load user settings
with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

    username = settings['Username']
    darkMode = settings['Dark Mode']

    print('\nSettings')
    for item in settings.items():
        print(item)

if darkMode:
    ctk.set_appearance_mode('dark')
else:
    ctk.set_appearance_mode('light')

# Desktop
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
        super().__init__(master=desktop)
        self.column = tile_column
        self.row = tile_row
        self.name = f'Tile-{tile_column}:{tile_row}'
        self.empty = True

        self.label_text = ''
        # self.label_text = f'C:{tile_column}, R:{tile_row}'
        self.label = ctk.CTkLabel(self, text=self.label_text)
        self.label.pack(expand=True, fill='both', padx=1, pady=1)

        rand_col = choice(('red', 'green', 'blue'))
        self.icon_label = ctk.CTkLabel(self, text="Icon", fg_color=rand_col)
        rand_name = choice(("Filename", 'File\'s name', 'Name of File'))
        self.name_label = ctk.CTkLabel(self, text=rand_name)

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
        # print('\n')
        # for row in parent.tiles:
        #     print(row)

    @classmethod
    def refresh_tiles(cls):
        for row in desktop.tiles:
            for tile in row:
                tile = tile[0]
                if not tile.empty:
                    tile.icon_label.pack_forget()
                    tile.name_label.pack_forget()
                    tile.empty = True
                    tile.label.pack(expand=True, fill='both')

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
        return desktop.tiles[tile_column][tile_row][0]

    @staticmethod
    def load_desktop_files():
        print('\nLoading desktop files...')
        os.chdir(f'{rootDir}\\Desktop')
        files_found = 0
        for row in desktop.tiles:
            for tile in row:
                tile = tile[0]
                file_name = f'{tile.column}.{tile.row}.txt'
                file_path = f'{os.getcwd()}\\{file_name}'
                if os.path.exists(file_path):
                    print(f'File found: {file_name}')
                    files_found += 1
                    tile.empty = False
                    tile.label.pack_forget()

                    tile.icon_label.configure(text='Txt', fg_color='white', text_color='black')
                    tile.name_label.configure(text='New Text Document', justify='center')
                    tile.icon_label.pack(expand=True, fill='both', padx=18, pady=3)
                    tile.name_label.pack(padx=5, pady=5)
        if files_found == 0:
            print('No files found.')
        else:
            print('Done')

    @classmethod
    def open_file(cls):
        selected_tile = cls.find_tile(contextMenu.cMenuX.get(), contextMenu.cMenuY.get())
        os.chdir(f'{rootDir}\\Desktop')
        file_name = f'{selected_tile.column}.{selected_tile.row}.txt'
        file_path = f'{os.getcwd()}\\{file_name}'
        if os.path.exists(file_path):
            os.startfile(file_path)
        os.chdir(rootDir)

    @classmethod
    def create_text_file(cls):
        selected_tile = cls.find_tile(contextMenu.cMenuX.get(), contextMenu.cMenuY.get())

        os.chdir(f'{rootDir}\\Desktop')

        file_name = f'{selected_tile.column}.{selected_tile.row}.txt'
        with open(file_name, 'w'):
            pass
        os.chdir(rootDir)

        selected_tile.empty = False
        selected_tile.label.pack_forget()

        selected_tile.icon_label.configure(text='Txt', fg_color='white', text_color='black')
        selected_tile.name_label.configure(text='New Text Document', justify='center')
        selected_tile.icon_label.pack(expand=True, fill='both', padx=18, pady=3)
        selected_tile.name_label.pack(padx=5, pady=5)

    @classmethod
    def delete_file(cls):
        selected_tile = cls.find_tile(contextMenu.cMenuX.get(), contextMenu.cMenuY.get())

        os.chdir(f'{rootDir}\\Desktop')
        file_name = f'{selected_tile.column}.{selected_tile.row}.txt'
        file_path = f'{os.getcwd()}\\{file_name}'
        if os.path.exists(file_path):
            os.remove(file_path)
        os.chdir(rootDir)

        selected_tile.icon_label.pack_forget()
        selected_tile.name_label.pack_forget()
        selected_tile.empty = True
        selected_tile.label.pack(expand=True, fill='both')

Tile.create_tiles(desktop.columns, desktop.rows - 1)
print('Done')
Tile.load_desktop_files()
print('------------------------------------------------')

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

# Start menu and button
class StartMenu(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=window)
        # self.place(x=0, rely=0.555, relwidth=0.15, relheight=0.4)
        self.place(x=0, rely=0.555, relwidth=0.2, relheight=0.4)

        self.starMenuText = f'Hello, {username}!\n{edition} Edition'
        self.startLabel = ctk.CTkLabel(master=self, text=self.starMenuText, anchor='center')
        self.startLabel.place(relx=0.02, rely=0.02)

        self.startItemContainer = ctk.CTkFrame(master=self)
        self.startItemContainer.columnconfigure(1, weight=1)
        self.startItemContainer.place(x=0, rely=0.1, relwidth=1, relheight=0.75)

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

class StartMenuItem(ctk.CTkFrame):
    def __init__(self, label_text):
        super().__init__(master=startMenu.startItemContainer)
        self._border_width = 1
        self._border_color = 'black'
        self._fg_color = '#D3D3D3'

        rand_col = choice(('red', 'green', 'blue'))
        icon = ctk.CTkLabel(master=self, text=f'{label_text}\nIcon', fg_color=rand_col)
        icon.pack(side='left', padx=7)
        name = ctk.CTkLabel(master=self, text=f'{label_text} name', text_color='black', fg_color='pink', anchor='w')
        name.pack(side='left', expand=True, fill='both', padx=5, pady=10)

max_items = 6  # Anything above 6 breaks it, don't understand why
item_list = []
item_list = update_list(max_items, item_list)
# startItemContainer.rowconfigure(rowList, weight=1, uniform='a')
for item in range(max_items):
    # StartMenuItem(f'Item {item}').grid(column=1, row=item, sticky='nsew')
    StartMenuItem(f'Item {item}').pack(expand=True, fill='both', padx=2, pady=1)


# Context Menu
def open_settings():
    print('Settings opened')

def task_manager():
    print('Opened Task Manager')


# noinspection PyUnusedLocal
class ContextMenu(tk.Menu):
    def __init__(self):
        super().__init__(window, tearoff=0)
        self.cMenuX = tk.IntVar(value=0)
        self.cMenuY = tk.IntVar(value=0)
        self.selected_widget = None

    def select_widget(self, event):
        self.cMenuX.set(event.x_root)
        self.cMenuY.set(event.y_root)

        self.selected_widget = event.widget.winfo_containing(self.cMenuX.get(), self.cMenuY.get())

        while self.selected_widget is not None:
            if isinstance(self.selected_widget, Tile):
                break
            self.selected_widget = self.selected_widget.master

        if not isinstance(self.selected_widget, Tile):
            self.selected_widget = event.widget.winfo_containing(self.cMenuX.get(), self.cMenuY.get())
            while self.selected_widget is not None:
                if isinstance(self.selected_widget, Taskbar):
                    break
                self.selected_widget = self.selected_widget.master

        print(f'\nSelected widget: {self.selected_widget}')

    def add_options(self, widget):
        self.delete(0, tk.END)
        if isinstance(widget, Tile):
            selected_tile = Tile.find_tile(contextMenu.cMenuX.get(), contextMenu.cMenuY.get())
            if selected_tile.empty:
                self.add_command(label='New Text File', command=Tile.create_text_file)
            else:
                self.add_command(label='Open File', command=Tile.open_file)
                self.add_command(label='Delete', command=Tile.delete_file)
        elif isinstance(widget, Taskbar):
            self.add_command(label='Settings', command=open_settings)
            self.add_command(label='Task Manager', command=task_manager)
        else:
            self.add_command(label='Settings', command=open_settings)

    def open_menu(self, event):
        self.add_options(self.selected_widget)
        try:
            contextMenu.tk_popup(self.cMenuX.get(), self.cMenuY.get())
        finally:
            contextMenu.grab_release()

contextMenu = ContextMenu()

window.bind('<Button-3>', contextMenu.select_widget)
window.bind('<ButtonRelease-3>', contextMenu.open_menu)

# Debug menu and button
class Debug(ctk.CTkFrame):
    def __init__(self):
        super().__init__(window)
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

        self.refreshTilesButton = ctk.CTkButton(self, text='Refresh Tiles', command=Tile.refresh_tiles)
        self.refreshTilesButton.pack(side='top', padx=5, pady=5)

        self.pTerminalButton = ctk.CTkButton(master=self, text='Open Terminal', command=self.open_terminal)
        self.pTerminalButton.pack(side='top', padx=5, pady=5)

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

    @staticmethod
    def open_terminal():
        window = NewWindow('Python Terminal', minWidth, minHeight, minWidth, minHeight)
        terminal_text = ctk.CTkTextbox(window)
        text_scroll = ctk.CTkScrollbar(master=window, orientation='vertical', command=terminal_text.yview)
        terminal_text.configure(yscrollcommand=text_scroll.set)
        text_scroll.place(relx=1, rely=0, relheight=1, anchor='ne')
        terminal_text.pack(expand=True, fill='both')

debugMenu = Debug()


window.mainloop()
