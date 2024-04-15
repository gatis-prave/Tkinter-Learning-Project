import tkinter as tk
import customtkinter as ctk
from time import strftime
from random import choice
import Installer

screenWidth = Installer.screenWidth
screenHeight = Installer.screenHeight
edition = Installer.editionsString.get()
username = Installer.usernameString.get()

class NewWindow(ctk.CTkToplevel):  # The widget always minimizes on creation for some reason
    def __init__(self, window_title, width, height, min_width, min_height):
        super().__init__()
        self.title(window_title)
        self.geometry(f'{width}x{height}')
        self.minsize(min_width, min_height)


# Desktop
# Window setup
minWidth = int(screenWidth * 0.5)
minHeight = int(screenHeight * 0.5)
deskWindow = ctk.CTk()
deskWindow.title(edition)
deskWindow.geometry(f'{minWidth}x{minHeight}')
deskWindow.attributes('-fullscreen', 1)
deskWindow.minsize(minWidth, minHeight)


def update_list(value, outdated_list):
    outdated_list.clear()
    for grid_item in range(value):
        outdated_list.append(grid_item)
    return outdated_list


class Desktop(ctk.CTkFrame):
    def __init__(self, column_count, row_count):
        super().__init__(master=deskWindow)
        self.place(x=0, y=0, relwidth=1, relheight=1)

        self.columns = column_count
        column_list = []
        column_list = update_list(self.columns, column_list)
        self.columnSize = int(screenWidth / self.columns)
        print(f'\nSmall column size: {self.columnSize}')
        self.columnconfigure(column_list, weight=1, uniform='a')

        self.rows = row_count
        row_list = []
        row_list = update_list(self.rows, row_list)
        self.rowSize = int(screenHeight / self.rows)
        print(f'Small row size: {self.rowSize}')
        self.rowconfigure(row_list, weight=1, uniform='a')

        self.tiles = []

desktopSml = Desktop(28, 17)
desktopMed = Desktop(24, 15)
desktopLrg = Desktop(20, 13)

class Tile(ctk.CTkFrame):
    def __init__(self, tile_column, tile_row, parent):
        super().__init__(master=parent)
        self.name = f'{tile_column}:{tile_row}'
        self.empty = True

        self.label_text = f'C:{tile_column}, R:{tile_row}'
        self.label = ctk.CTkLabel(self, text=self.label_text)
        self.label.pack(expand=True, fill='both')

        rand_col = choice(('red', 'green', 'blue'))
        self.icon_label = ctk.CTkLabel(self, text="Icon", fg_color=rand_col)
        rand_name = choice(("Filename", 'File\'s name', 'Name of File'))
        self.name_label = ctk.CTkLabel(self, text=rand_name)

        self.grid(row=tile_row, column=tile_column, sticky='nsew', padx=1, pady=1)

    def __str__(self):
        return self.name

    @classmethod
    def create_tiles(cls, column_count, row_count, parent):
        parent.tiles = [[[] for _ in range(row_count)] for _ in range(column_count)]
        tile_column = 0
        tile_row = 0
        for current_row in range(row_count):
            for current_column in range(column_count):
                parent.tiles[current_column][current_row].append(cls(tile_column, tile_row, parent))
                tile_column += 1
            tile_column = 0
            tile_row += 1
        print('\n')
        for row in parent.tiles:
            print(row)

    @classmethod
    def refresh_tiles(cls):
        for row in currentDesktop.tiles:
            for tile in row:
                tile = tile[0]
                if not tile.empty:
                    tile.icon_label.pack_forget()
                    tile.name_label.pack_forget()
                    tile.empty = True
                    tile.label.pack(expand=True, fill='both')

    @classmethod
    def find_tile(cls, x_pos, y_pos, desktop):
        tile_column = int(x_pos / desktop.columnSize)
        if tile_column < 1:
            tile_column = 0
        if tile_column > desktop.columns:
            tile_column = desktop.columns
        print('\nTile Found:')
        print(f'Column: {tile_column}')

        tile_row = int(y_pos / desktop.rowSize)
        if tile_row < 1:
            tile_row = 0
        if tile_row > desktop.rows - 2:
            tile_row = desktop.rows - 2
        print(f'Row: {tile_row}')
        return desktop.tiles[tile_column][tile_row][0]

    @classmethod
    def create_file_test(cls):
        selected_tile = cls.find_tile(contextMenu.cMenuX.get(), contextMenu.cMenuY.get(), currentDesktop)
        if selected_tile.empty:
            selected_tile.label.pack_forget()
            selected_tile.icon_label.pack(expand=True, fill='both', padx=5, pady=3)
            selected_tile.name_label.pack()
            selected_tile.empty = False

    @classmethod
    def delete_file(cls):
        selected_tile = cls.find_tile(contextMenu.cMenuX.get(), contextMenu.cMenuY.get(), currentDesktop)
        if not selected_tile.empty:
            selected_tile.icon_label.pack_forget()
            selected_tile.name_label.pack_forget()
            selected_tile.empty = True
            selected_tile.label.pack(expand=True, fill='both')

Tile.create_tiles(desktopSml.columns, desktopSml.rows - 1, desktopSml)
Tile.create_tiles(desktopMed.columns, desktopMed.rows - 1, desktopMed)
Tile.create_tiles(desktopLrg.columns, desktopLrg.rows - 1, desktopLrg)

# Context Menu
class ContextMenu(tk.Menu):
    def __init__(self):
        super().__init__(deskWindow, tearoff=0)
        self.add_command(label='New File', command=Tile.create_file_test)
        self.add_command(label='Delete', command=Tile.delete_file)
    cMenuX = tk.IntVar(value=0)
    cMenuY = tk.IntVar(value=0)
    @classmethod
    def get_widget_under_cursor(cls, event):
        # Get the x, y coordinates of the mouse pointer relative to the root window
        print('get widget event triggered')
        cls.cMenuX.set(event.x_root)
        cls.cMenuY.set(event.y_root)

        # Find the widget under the mouse pointer
        widget = event.widget.winfo_containing(cls.cMenuX.get(), cls.cMenuY.get())

        print(widget)
    @classmethod
    def open_menu(cls, event):
        try:
            contextMenu.tk_popup(cls.cMenuX.get(), cls.cMenuY.get())
        finally:
            contextMenu.grab_release()

contextMenu = ContextMenu()

deskWindow.bind('<Button-3>', contextMenu.get_widget_under_cursor)
deskWindow.bind('<ButtonRelease-3>', contextMenu.open_menu)

# Taskbar
taskbar = ctk.CTkFrame(master=deskWindow,
                       border_width=1)
taskbar.place(x=0, rely=0.955, relwidth=1, relheight=0.05)


# Date/Time
def update_time():
    time_string = strftime('%H:%M:%S')  # time format
    timeLabel.configure(text=time_string)
    timeLabel.after(1000, update_time)


timeLabel = ctk.CTkLabel(master=taskbar)
timeLabel.bind('<Activate>', update_time())
timeLabel.pack(side='right', padx=5)


# Start menu and button
class StartMenuItem(ctk.CTkFrame):
    def __init__(self, label_text):
        super().__init__(master=startItemContainer)
        self._border_width = 1
        self._border_color = 'black'
        self._fg_color = '#D3D3D3'

        rand_col = choice(('red', 'green', 'blue'))
        icon = ctk.CTkLabel(master=self, text=f'{label_text}\nIcon', fg_color=rand_col)
        icon.pack(side='left', padx=7)
        name = ctk.CTkLabel(master=self, text=f'{label_text} name', text_color='black', fg_color='pink', anchor='w')
        name.pack(side='left', expand=True, fill='both', padx=5, pady=10)


def start_menu():
    global startMenuEnabled
    if startMenuEnabled:
        startMenuEnabled = False
        startMenu.lower()
    else:
        startMenuEnabled = True
        startMenu.lift()


startButton = ctk.CTkButton(master=taskbar, text='Start', command=start_menu)
startButton.pack(side='left', padx=5)

startMenuEnabled = False
startMenu = ctk.CTkFrame(master=deskWindow)
startMenu.place(x=0, rely=0.555, relwidth=0.15, relheight=0.4)

starMenuText = f'Hello, {username}!\n{edition} Edition'
startLabel = ctk.CTkLabel(master=startMenu, text=starMenuText, anchor='center')
startLabel.place(relx=0.02, rely=0.02)

startItemContainer = ctk.CTkFrame(master=startMenu)
startItemContainer.columnconfigure(1, weight=1)
startItemContainer.place(x=0, rely=0.1, relwidth=1, relheight=0.75)

max_items = 6  # Anything above 6 breaks it, don't understand why
row_list = []
row_list = update_list(max_items, row_list)
# startItemContainer.rowconfigure(rowList, weight=1, uniform='a')
for item in range(max_items):
    # StartMenuItem(f'Item {item}').grid(column=1, row=item, sticky='nsew')
    StartMenuItem(f'Item {item}').pack(expand=True, fill='both', padx=2, pady=1)

shutDownButton = ctk.CTkButton(master=startMenu, text='Shut down', command=lambda: deskWindow.destroy())
shutDownButton.place(relx=0.05, rely=0.95, anchor='sw')

startMenu.lower()

# Debug menu and button
class Debug(ctk.CTkFrame):
    def __init__(self):
        super().__init__(deskWindow)
        self.enabled = False
        self.place(x=0, y=0)
        self.lower()

    def toggle_menu(self):
        if self.enabled:
            self.enabled = False
            debugMenu.lower()
        else:
            self.enabled = True
            debugMenu.lift()
    @staticmethod
    def fullscreen_toggle():
        if fullscreenBool.get():
            deskWindow.attributes('-fullscreen', 1)
            fullscreenBool.set(True)
        else:
            deskWindow.attributes('-fullscreen', 0)
            fullscreenBool.set(False)
        print(deskWindow.winfo_width())
    @staticmethod
    def taskbar_toggle():
        if taskbarBool.get():
            taskbarBool.set(True)
            taskbar.place(x=0, rely=0.955, relwidth=1, relheight=0.045)
            startButton.pack(side='left', padx=5)
            debugButton.pack(side='left')
            timeLabel.pack(side='right', padx=5)
        else:
            taskbarBool.set(False)
            taskbar.place_forget()
    @staticmethod
    def select_icon_size(value):
        iconSizeVar.set(int(value))
    @staticmethod
    def change_icon_size():
        global currentDesktop
        if iconSizeVar.get() == 0:
            desktopSml.lift()
            taskbar.lift()
            if startMenuEnabled:
                startMenu.lift()
            if debugMenu.enabled:
                debugMenu.lift()
            currentDesktop = desktopSml
        elif iconSizeVar.get() == 1:
            desktopMed.lift()
            taskbar.lift()
            if startMenuEnabled:
                startMenu.lift()
            if debugMenu.enabled:
                debugMenu.lift()
            currentDesktop = desktopMed
        else:
            desktopLrg.lift()
            taskbar.lift()
            if startMenuEnabled:
                startMenu.lift()
            if debugMenu.enabled:
                debugMenu.lift()
            currentDesktop = desktopLrg
        print(f'\nDesktop info:\nCurrent desktop: {currentDesktop}')

    @staticmethod
    def open_terminal():
        window = NewWindow('Python Terminal', minWidth, minHeight, minWidth, minHeight)
        terminal_text = ctk.CTkTextbox(window)
        text_scroll = ctk.CTkScrollbar(master=window, orientation='vertical', command=terminal_text.yview)
        terminal_text.configure(yscrollcommand=text_scroll.set)
        text_scroll.place(relx=1, rely=0, relheight=1, anchor='ne')
        terminal_text.pack(expand=True, fill='both')
        

debugMenu = Debug()
debugButton = ctk.CTkButton(master=taskbar, text='Debug Menu', command=debugMenu.toggle_menu)
debugButton.pack(side='left')

fullscreenBool = tk.BooleanVar(value=True)
fullscreenCheck = ctk.CTkCheckBox(
    master=debugMenu,
    text='Fullscreen',
    command=Debug.fullscreen_toggle,
    variable=fullscreenBool)
fullscreenCheck.pack(side='top', padx=5, pady=5)

taskbarBool = tk.BooleanVar(value=True)
taskbarCheck = ctk.CTkCheckBox(
    master=debugMenu,
    text='Taskbar',
    command=Debug.taskbar_toggle,
    variable=taskbarBool)
taskbarCheck.pack(side='top', padx=5, pady=5)

iconSizeVar = tk.IntVar(value=1)
currentDesktop = desktopMed
desktopMed.lift()
taskbar.lift()

iconSizeFrame = ctk.CTkFrame(master=debugMenu)
iconSizeFrame.pack(side='top', padx=5, pady=5)
iconSizeLabel = ctk.CTkLabel(master=iconSizeFrame, text='Icon Size:')
iconSizeLabel.pack()
iconSizeSlider = ctk.CTkSlider(master=iconSizeFrame,
                               command=Debug.select_icon_size,
                               variable=iconSizeVar,
                               from_=0,
                               to=2,
                               number_of_steps=2,
                               progress_color='transparent')
iconSizeSlider.pack()
selectSizeButton = ctk.CTkButton(iconSizeFrame, text='Select Size', command=Debug.change_icon_size)
selectSizeButton.pack(pady=5)

refreshTilesButton = ctk.CTkButton(debugMenu, text='Refresh Tiles', command=Tile.refresh_tiles)
refreshTilesButton.pack(side='top', padx=5, pady=5)

pTerminalButton = ctk.CTkButton(master=debugMenu, text='Open Terminal', command=Debug.open_terminal)
pTerminalButton.pack(side='top', padx=5, pady=5)

deskWindow.mainloop()
