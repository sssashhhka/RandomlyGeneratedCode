import time
import customtkinter as gui
import db_handler

from PIL import Image

theme_mode_icon = gui.CTkImage(light_image=Image.open('icons/moon.png'),
                               dark_image=Image.open('icons/sun.png'), size=(20, 20))


def delete_account():
    delete_dialog = gui.CTkInputDialog(text='Are you sure you want to delete your account?\nType "Yes" or "No"',
                                            title='Confirmation')
    if delete_dialog.get_input() == 'Yes':
        db_handler.delete(user=app.current_user)
    else:
        pass


class ProfileWindow(gui.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title('Profile')
        self.geometry('340x340')

        self.hiLabel_font = gui.CTkFont(family='Segoe UI Variable', size=25, weight='normal')
        self.midLabel_font = gui.CTkFont(family='Segoe UI Variable', size=20, weight='normal')
        self.button_font = gui.CTkFont(family='Segoe UI Variable', size=15, weight='normal')

        self.info = gui.CTkLabel(self, text='Signed in by:', font=self.button_font)
        self.account_frame = gui.CTkFrame(self, corner_radius=10, border_width=1)
        self.account = gui.CTkLabel(self.account_frame, text=app.current_user, font=self.hiLabel_font)
        self.new_email = gui.CTkEntry(self, placeholder_text='New Email', font=self.button_font)
        self.new_passwd = gui.CTkEntry(self, placeholder_text='New Password', font=self.button_font)
        self.account_delete = gui.CTkButton(self, text='Delete Account', fg_color='#ff4040',
                                            text_color='#000000', font=self.button_font,
                                            hover_color='#cc3333', border_width=2, border_color='#f75959',
                                            command=delete_account)
        self.account_sign_out = gui.CTkButton(self, text='Sign Out', font=self.button_font)
        self.account_update_email = gui.CTkButton(self, text='Update Email', font=self.button_font,
                                                  command=self.update_email)
        self.account_update_passwd = gui.CTkButton(self, text='Update Password', font=self.button_font,
                                                   command=self.update_passwd)

        self.info.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='new', columnspan=2)
        self.account_frame.grid(row=1, column=0, padx=10, pady=(0, 10), columnspan=2, sticky='n')
        self.account.grid(row=1, column=0, padx=10, pady=3, sticky='new')
        self.new_email.grid(row=2, column=0, padx=10, pady=10, sticky='new', columnspan=2)
        self.new_passwd.grid(row=3, column=0, padx=10, pady=10, sticky='new', columnspan=2)
        self.account_update_email.grid(row=4, column=0, padx=10, pady=10, sticky='sew')
        self.account_update_passwd.grid(row=4, column=1, padx=10, pady=10, sticky='sew')
        self.account_sign_out.grid(row=5, column=0, padx=10, pady=10, sticky='sew')
        self.account_delete.grid(row=5, column=1, padx=10, pady=10, sticky='sew')

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def update_passwd(self):
        if self.new_passwd.get() != '':
            new_passwd = self.new_passwd.get()
            db_handler.update(user=app.current_user, passwd=new_passwd)
        else:
            print('Nothing to update')

    def update_email(self):
        if self.new_email.get() != '':
            new_email = self.new_email.get()
            db_handler.update(user=app.current_user, email=new_email)
        else:
            print('Nothing to update')


class MainWindow(gui.CTk):
    def __init__(self):
        super().__init__()

        self.current_user = db_handler.get('admin', 'username')[0]
        self.current_theme = db_handler.get('admin', 'theme')[0]

        self.hiLabel_font = gui.CTkFont(family='Segoe UI Variable', size=25, weight='normal')
        self.midLabel_font = gui.CTkFont(family='Segoe UI Variable', size=20, weight='normal')
        self.button_font = gui.CTkFont(family='Segoe UI Variable', size=15, weight='normal')

        self.title('Main Window')
        self.geometry('500x350')

        gui.set_appearance_mode(self.current_theme)

        self.bottom_bar = gui.CTkFrame(self, corner_radius=0)
        self.username_frame = gui.CTkFrame(self.bottom_bar, corner_radius=10, border_width=1)
        self.main_frame = gui.CTkFrame(self)

        self.label = gui.CTkLabel(self, text='Main Window', font=self.hiLabel_font)
        self.username = gui.CTkLabel(self.username_frame, text=self.current_user, font=self.midLabel_font)
        self.theme_button = gui.CTkButton(self.bottom_bar, image=theme_mode_icon, text='', fg_color='transparent',
                                          width=20, command=self.set_theme, height=35, hover=False)
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

    def open_profile(self, event_name):
        print(event_name)
        if self.profile_window is None or not self.profile_window.winfo_exists():
            self.profile_window = ProfileWindow()
            time.sleep(0.5)
            self.profile_window.focus_force()
        else:
            self.profile_window.focus()

    def set_theme(self):
        if self.current_theme == 'dark':
            self.current_theme = 'light'
            db_handler.update(user=self.current_user, theme='light')
            gui.set_appearance_mode('light')
        else:
            self.current_theme = 'dark'
            db_handler.update(user=self.current_user, theme='dark')
            gui.set_appearance_mode('dark')


app = MainWindow()

if __name__ == '__main__':
    app.mainloop()
