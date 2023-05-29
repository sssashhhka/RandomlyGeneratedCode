import customtkinter as gui
import db_handler

version = '0.1 Beta Build 1'

current_user = db_handler.check(return_param='username', isCurrent='1')
if current_user is None:
    from Sign_In_Window import startsi
    startsi()
    exit()
else:
    current_theme = db_handler.get(current_user, 'theme')[0]


def delete_account():
    delete_dialog = gui.CTkInputDialog(text='Are you sure you want to delete your account?\nType your password below:',
                                            title='Confirmation')
    if delete_dialog.get_input() == db_handler.get(current_user, 'passwd')[0]:
        db_handler.delete(user=current_user)
    else:
        pass


class AccountSettings(gui.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title('Account settings')
        self.geometry('340x340')

        self.hiLabel_font = gui.CTkFont(family='Segoe UI Variable', size=25, weight='normal')
        self.midLabel_font = gui.CTkFont(family='Segoe UI Variable', size=20, weight='normal')
        self.button_font = gui.CTkFont(family='Segoe UI Variable', size=15, weight='normal')

        self.top_bar = gui.CTkFrame(self, corner_radius=0)
        self.acc_username = gui.CTkLabel(self.top_bar, text=current_user, font=self.midLabel_font)

        self.account_delete = gui.CTkButton(self, text='Delete Account', fg_color='#ff4040',
                                            text_color='#000000', font=self.button_font,
                                            hover_color='#cc3333', border_width=2, border_color='#f75959',
                                            command=delete_account)

        self.top_bar.grid(row=0, column=0, sticky='new')
        self.acc_username.grid(row=0, column=0, padx=20, pady=10, sticky='nws')

        self.account_delete.grid(row=1, column=0, padx=10, pady=10, sticky='sew', columnspan=2)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.top_bar.columnconfigure(0, weight=1)
        self.top_bar.rowconfigure(0, weight=1)


class MainWindow(gui.CTk):
    def __init__(self):
        super().__init__()
        gui.set_appearance_mode(current_theme)

        self.hiLabel_font = gui.CTkFont(family='Segoe UI Variable', size=25, weight='normal')
        self.midLabel_font = gui.CTkFont(family='Segoe UI Variable', size=20, weight='normal')
        self.button_font = gui.CTkFont(family='Segoe UI Variable', size=15, weight='normal')

        self.cur_theme = gui.StringVar(value=current_theme)

        self.title('Main Window')
        self.geometry('700x500')

        self.version = gui.CTkLabel(self, text=f'Version: {version}', font=self.button_font, text_color='#444444')
        self.side_bar = gui.CTkFrame(self, corner_radius=0)
        self.menu = gui.CTkLabel(self.side_bar, text='Main menu', font=self.hiLabel_font)

        self.acc_frame = gui.CTkFrame(self.side_bar, corner_radius=10)
        self.acc_username = gui.CTkLabel(self.acc_frame, text=current_user, font=self.midLabel_font)
        self.acc_settings = gui.CTkButton(self.acc_frame, text='Account settings', font=self.button_font,
                                          command=self.open_profile)
        self.sign_out_button = gui.CTkButton(self.acc_frame, text='Sign Out', font=self.button_font,
                                             command=self.sign_out)

        self.theme_info = gui.CTkLabel(self.side_bar, text='Theme:', font=self.button_font)
        self.theme_picker = gui.CTkOptionMenu(self.side_bar, values=['Dark', 'Light'], font=self.button_font,
                                              variable=self.cur_theme, command=self.set_theme)
        self.exit_button = gui.CTkButton(self.side_bar, text='Exit', font=self.button_font, command=exit)

        self.version.grid(row=2, column=4, padx=10, pady=5, sticky='se')
        self.side_bar.grid(row=0, column=0, sticky='nws', rowspan=4)
        self.menu.grid(row=0, column=0, padx=10, pady=10, sticky='new')

        self.acc_frame.grid(row=1, column=0, padx=10, pady=10, sticky='new')
        self.acc_username.grid(row=0, column=0, padx=5, pady=5, sticky='new')
        self.acc_settings.grid(row=1, column=0, padx=10, pady=(5, 5), sticky='sew')
        self.sign_out_button.grid(row=2, column=0, padx=10, pady=(5, 10), sticky='sew')

        self.theme_info.grid(row=2, column=0, sticky='sew')
        self.theme_picker.grid(row=3, column=0, padx=10, pady=(0, 5), sticky='sew')
        self.exit_button.grid(row=4, column=0, padx=10, pady=(5, 10), sticky='sew')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.side_bar.rowconfigure(0, weight=1)
        self.side_bar.rowconfigure(1, weight=1)

        self.acc_frame.columnconfigure(0, weight=1)

        self.profile_window = None

    def sign_out(self):
        db_handler.update(user=current_user, isCurrent='0')
        import Sign_In_Window
        self.withdraw()
        app.withdraw()
        Sign_In_Window.startsi()

    def set_theme(self, choice):
        gui.set_appearance_mode(choice)
        self.cur_theme.set(value=choice)
        db_handler.update(user=current_user, theme=choice)

    def open_profile(self):
        if self.profile_window is None or not self.profile_window.winfo_exists():
            self.profile_window = AccountSettings()
        else:
            self.profile_window.focus()


app = MainWindow()


def startmw():
    app.mainloop()


if __name__ == '__main__':
    app.mainloop()
