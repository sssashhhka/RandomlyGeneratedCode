import time
from PIL import Image
import customtkinter as gui

theme_mode_icon = gui.CTkImage(light_image=Image.open('icons/moon.png'),
                               dark_image=Image.open('icons/sun.png'), size=(20, 20))


class ProfileWindow(gui.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title('Profile')
        self.geometry('340x340')


class MainWindow(gui.CTk):
    def __init__(self):
        super().__init__()

        self.title('Main Window')
        self.geometry('500x350')

        self.current_theme = 'dark'

        gui.set_appearance_mode(self.current_theme)

        self.hiLabel_font = gui.CTkFont(family='Segoe UI Variable', size=25, weight='normal')
        self.midLabel_font = gui.CTkFont(family='Segoe UI Variable', size=20, weight='normal')
        self.button_font = gui.CTkFont(family='Segoe UI Variable', size=15, weight='normal')

        self.bottom_bar = gui.CTkFrame(self, corner_radius=0)
        self.username_frame = gui.CTkFrame(self.bottom_bar, corner_radius=10, border_width=1)
        self.main_frame = gui.CTkFrame(self, corner_radius=15)

        self.label = gui.CTkLabel(self, text='Main Window', font=self.hiLabel_font)
        self.username = gui.CTkLabel(self.username_frame, text='sssashhhka', font=self.midLabel_font)
        self.theme_button = gui.CTkButton(self.bottom_bar, image=theme_mode_icon, text='', fg_color='transparent',
                                          width=20, command=self.set_theme)
        self.exit = gui.CTkButton(self.bottom_bar, text='Exit', font=self.button_font, command=exit)

        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='new')
        self.exit.grid(row=0, column=2, padx=10, pady=10, sticky='e')
        self.username.grid(row=0, column=0, padx=10, pady=2, sticky='w')
        self.theme_button.grid(row=0, column=0, padx=(10, 0), pady=10)

        self.bottom_bar.grid(row=2, column=0, padx=0, pady=0, sticky='sew')
        self.username_frame.grid(row=0, column=1, padx=10, pady=10)
        self.main_frame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.bottom_bar.rowconfigure(0, weight=1)
        self.bottom_bar.columnconfigure(2, weight=1)

        self.username.bind('<Button-1>', self.open_profile)
        self.profile_window = None

    def open_profile(self, *args):
        if self.profile_window is None or not self.profile_window.winfo_exists():
            self.profile_window = ProfileWindow()
            time.sleep(0.5)
            self.profile_window.focus_force()
        else:
            self.profile_window.focus()

    def set_theme(self):
        if self.current_theme == 'dark':
            self.current_theme = 'light'
            gui.set_appearance_mode('light')
            self.username.configure(text_color='#000000')
        else:
            self.current_theme = 'dark'
            self.username.configure(text_color='#FFFFFF')
            gui.set_appearance_mode('dark')


app = MainWindow()

if __name__ == '__main__':
    app.mainloop()
