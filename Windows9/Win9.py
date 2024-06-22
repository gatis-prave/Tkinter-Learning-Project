import tkinter as tk
import customtkinter as ctk
from time import strftime
from random import choice
# import Installer
#
# screenWidth = Installer.screenWidth
# screenHeight = Installer.screenHeight
# edition = Installer.editionsString.get()
# username = Installer.usernameString.get()

screenWidth = 1920
screenHeight = 1080
edition = 'Windows 9 Developer'
username = 'User 1'

class NewWindow(ctk.CTkToplevel):  # The window always minimizes on creation for some reason
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
    for list_item in range(value):
        outdated_list.append(list_item)
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
        self.name = f'Tile-{tile_column}:{tile_row}'
        self.empty = True

        self.label_text = f'C:{tile_column}, R:{tile_row}'
        self.label = ctk.CTkLabel(self, text=self.label_text)
        self.label.pack(expand=True, fill='both')

        rand_col = choice(('red', 'green', 'blue'))
        self.icon_label = ctk.CTkLabel(self, text="Icon", fg_color=rand_col)
        rand_name = choice(("Filename", 'File\'s name', 'Name of File'))
        self.name_label = ctk.CTkLabel(self, text=rand_name)

        self.grid(row=tile_row, column=tile_column, sticky='nsew')

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
        for row in debugMenu.currentDesktop.tiles:
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
        selected_tile = cls.find_tile(contextMenu.cMenuX.get(), contextMenu.cMenuY.get(), debugMenu.currentDesktop)
        if selected_tile.empty:
            selected_tile.label.pack_forget()
            selected_tile.icon_label.pack(expand=True, fill='both', padx=5, pady=3)
            selected_tile.name_label.pack()
            selected_tile.empty = False

    @classmethod
    def delete_file(cls):
        selected_tile = cls.find_tile(contextMenu.cMenuX.get(), contextMenu.cMenuY.get(), debugMenu.currentDesktop)
        if not selected_tile.empty:
            selected_tile.icon_label.pack_forget()
            selected_tile.name_label.pack_forget()
            selected_tile.empty = True
            selected_tile.label.pack(expand=True, fill='both')

[Tile.create_tiles(desktop.columns, desktop.rows - 1, desktop) for desktop in [desktopSml, desktopMed, desktopLrg]]

# Taskbar
class Taskbar(ctk.CTkFrame):
    def __init__(self):
        super().__init__(deskWindow, border_width=1)
        self.place(x=0, rely=0.955, relwidth=1, relheight=0.05)

        self.timeLabel = ctk.CTkLabel(master=self)
        self.timeLabel.pack(side='right', padx=5)
        self.timeLabel.bind('<Activate>', self.update_time)
        self.update_time()

        self.lower()
    def update_time(self):
        time_string = strftime('%H:%M:%S')
        self.timeLabel.configure(text=time_string)
        self.timeLabel.after(1000, self.update_time)

taskbarWid = Taskbar()

# Start menu and button
class StartMenu(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master=deskWindow)
        self.place(x=0, rely=0.555, relwidth=0.15, relheight=0.4)

        self.starMenuText = f'Hello, {username}!\n{edition} Edition'
        self.startLabel = ctk.CTkLabel(master=self, text=self.starMenuText, anchor='center')
        self.startLabel.place(relx=0.02, rely=0.02)

        self.startItemContainer = ctk.CTkFrame(master=self)
        self.startItemContainer.columnconfigure(1, weight=1)
        self.startItemContainer.place(x=0, rely=0.1, relwidth=1, relheight=0.75)

        self.shutDownButton = ctk.CTkButton(master=self, text='Shut down', command=lambda: deskWindow.destroy())
        self.shutDownButton.place(relx=0.05, rely=0.95, anchor='sw')

        self.lower()

    startMenuEnabled = False

startMenu = StartMenu()

def toggle_start_menu():
    if StartMenu.startMenuEnabled:
        StartMenu.startMenuEnabled = False
        startMenu.lower()
    else:
        StartMenu.startMenuEnabled = True
        startMenu.lift()


startButton = ctk.CTkButton(master=taskbarWid, text='Start', command=toggle_start_menu)
startButton.pack(side='left', padx=5)


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

class ContextMenu(tk.Menu):
    def __init__(self):
        super().__init__(deskWindow, tearoff=0)
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
            print('\nWidget not a tile')
            while self.selected_widget is not None:
                if isinstance(self.selected_widget, Taskbar):
                    break
                self.selected_widget = self.selected_widget.master

        print(f'Selected widget: {self.selected_widget}')
        print(type(self.selected_widget))

    def add_options(self, widget):
        self.delete(0, tk.END)
        if isinstance(widget, Tile):
            self.add_command(label='New File', command=Tile.create_file_test)
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

deskWindow.bind('<Button-3>', contextMenu.select_widget)
deskWindow.bind('<ButtonRelease-3>', contextMenu.open_menu)

# Debug menu and button
class Debug(ctk.CTkFrame):
    def __init__(self):
        super().__init__(deskWindow)
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

        self.iconSizeVar = tk.IntVar(value=1)
        self.currentDesktop = desktopMed
        self.currentDesktop.lift()
        taskbarWid.lift()

        self.iconSizeFrame = ctk.CTkFrame(master=self)
        self.iconSizeFrame.pack(side='top', padx=5, pady=5)
        self.iconSizeLabel = ctk.CTkLabel(master=self.iconSizeFrame, text='Icon Size:')
        self.iconSizeLabel.pack()
        self.iconSizeSlider = ctk.CTkSlider(master=self.iconSizeFrame,
                                            command=self.change_icon_size,
                                            variable=self.iconSizeVar,
                                            from_=0,
                                            to=2,
                                            number_of_steps=2,
                                            progress_color='transparent')
        self.iconSizeSlider.pack()

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
            deskWindow.attributes('-fullscreen', 1)
            self.fullscreenBool.set(True)
        else:
            deskWindow.attributes('-fullscreen', 0)
            self.fullscreenBool.set(False)
        print(deskWindow.winfo_width())
    def taskbar_toggle(self):
        if self.taskbarBool.get():
            self.taskbarBool.set(True)
            taskbarWid.place(x=0, rely=0.955, relwidth=1, relheight=0.045)
            startButton.pack(side='left', padx=5)
            self.debug_button.pack(side='left')
            taskbarWid.timeLabel.pack(side='right', padx=5)
        else:
            self.taskbarBool.set(False)
            taskbarWid.place_forget()

    def select_icon_size(self, value):
        self.iconSizeVar.set(int(value))

    def change_icon_size(self, event):
        if self.iconSizeVar.get() == 0:
            desktopSml.lift()
            taskbarWid.lift()
            if startMenu.startMenuEnabled:
                startMenu.lift()
            if debugMenu.enabled:
                debugMenu.lift()
            self.currentDesktop = desktopSml
        elif self.iconSizeVar.get() == 1:
            desktopMed.lift()
            taskbarWid.lift()
            if startMenu.startMenuEnabled:
                startMenu.lift()
            if debugMenu.enabled:
                debugMenu.lift()
            self.currentDesktop = desktopMed
        else:
            desktopLrg.lift()
            taskbarWid.lift()
            if startMenu.startMenuEnabled:
                startMenu.lift()
            if debugMenu.enabled:
                debugMenu.lift()
            self.currentDesktop = desktopLrg
        print(f'\nDesktop info:\nCurrent desktop: {self.currentDesktop}')

    @staticmethod
    def open_terminal():
        window = NewWindow('Python Terminal', minWidth, minHeight, minWidth, minHeight)
        terminal_text = ctk.CTkTextbox(window)
        text_scroll = ctk.CTkScrollbar(master=window, orientation='vertical', command=terminal_text.yview)
        terminal_text.configure(yscrollcommand=text_scroll.set)
        text_scroll.place(relx=1, rely=0, relheight=1, anchor='ne')
        terminal_text.pack(expand=True, fill='both')

debugMenu = Debug()

deskWindow.mainloop()
