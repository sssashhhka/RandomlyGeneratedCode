import time
import customtkinter as gui
import random
import smtplib
from assets.fonts import *
from utility import passwd, db_handler

version = "0.4 Beta"


class Utility:
    c_user = ""
    c_theme = ""
    c_clr_theme = ""

    def user_init(self):
        self.c_user = db_handler.check(return_param='username', isCurrent='1')
        if self.c_user is None:
            pass
        else:
            self.c_theme = db_handler.get(self.c_user, 'theme')[0]
            self.c_clr_theme = db_handler.get(self.c_user, 'clrtheme')[0]


utility = Utility()
utility.user_init()

current_user = utility.c_user
current_theme = utility.c_theme
current_clr_theme = utility.c_clr_theme


class Main(gui.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("700x500")

        gui.set_appearance_mode(current_theme)
        self.cur_theme = gui.StringVar(value=current_theme)
        self.cur_clrtheme = gui.StringVar(value=current_clr_theme)

        self.version = gui.CTkLabel(self, text=f'Version: {version}', font=button_font, text_color='#444444')
        self.side_bar = gui.CTkFrame(self, corner_radius=0)
        self.menu = gui.CTkLabel(self.side_bar, text='Main menu', font=hi_label_font)
        self.acc_frame = gui.CTkFrame(self.side_bar, corner_radius=10)
        self.acc_username = gui.CTkLabel(self.acc_frame, text=current_user, font=mid_label_font)
        self.acc_settings = gui.CTkButton(self.acc_frame, text='Account settings', font=button_font)
        self.sign_out_button = gui.CTkButton(self.acc_frame, text='Sign Out', font=button_font,
                                             command=self.sign_out)
        self.theme_info = gui.CTkLabel(self.side_bar, text='Theme settings:', font=button_font)
        self.theme_picker = gui.CTkOptionMenu(self.side_bar, values=['Light', 'Dark'], font=button_font,
                                              variable=self.cur_theme, command=self.set_theme)
        self.clrtheme_picker = gui.CTkOptionMenu(self.side_bar, values=['Blue',
                                                                        'Dark-Blue',
                                                                        'Material 3',
                                                                        'Green'],
                                                 font=button_font,
                                                 command=self.set_clrtheme,
                                                 variable=self.cur_clrtheme)
        self.exit_button = gui.CTkButton(self.side_bar, text='Exit', font=button_font, command=finish)

        self.version.grid(row=2, column=4, padx=10, pady=5, sticky='se')
        self.side_bar.grid(row=0, column=0, sticky='nws', rowspan=4)
        self.menu.grid(row=0, column=0, padx=10, pady=10, sticky='new')

        self.acc_frame.grid(row=1, column=0, padx=10, pady=10, sticky='new')
        self.acc_username.grid(row=0, column=0, padx=5, pady=5, sticky='new')
        self.acc_settings.grid(row=1, column=0, padx=10, pady=(5, 5), sticky='sew')
        self.sign_out_button.grid(row=2, column=0, padx=10, pady=(5, 10), sticky='sew')

        self.theme_info.grid(row=2, column=0, sticky='sew')
        self.theme_picker.grid(row=3, column=0, padx=10, pady=(0, 5), sticky='sew')
        self.clrtheme_picker.grid(row=4, column=0, padx=10, pady=(5, 10), sticky='sew')
        self.exit_button.grid(row=5, column=0, padx=10, pady=(10, 10), sticky='sew')

        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)

        self.side_bar.rowconfigure(0, weight=1)
        self.side_bar.rowconfigure(1, weight=1)

        self.acc_frame.columnconfigure(0, weight=1)

    def sign_out(self):
        db_handler.update(user=current_user, isCurrent='0')
        self.withdraw()
        open_sign_in()

    def set_theme(self, choice):
        gui.set_appearance_mode(choice)
        self.cur_theme.set(value=choice)
        db_handler.update(user=current_user, theme=choice)

    def set_clrtheme(self, choice):
        if choice == 'Blue':
            print(choice)
            db_handler.update(user=current_user, clrtheme='Blue')
            gui.set_default_color_theme('blue')
        elif choice == 'Dark-Blue':
            print(choice)
            db_handler.update(user=current_user, clrtheme='Dark-Blue')
            gui.set_default_color_theme('dark-blue')
        elif choice == 'Green':
            print(choice)
            db_handler.update(user=current_user, clrtheme='Green')
            gui.set_default_color_theme('green')
        elif choice == 'Material 3':
            print(choice)
            db_handler.update(user=current_user, clrtheme='Material 3')
            gui.set_default_color_theme('themes/material_theme.json')
        self.quit()


class SignIn(gui.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sign In Window")
        self.geometry("300x400")
        self.minsize(300, 400)

        self.label = gui.CTkLabel(self, text='Sign In', font=hi_label_font)
        self.login = gui.CTkEntry(self, placeholder_text='Username', font=button_font)
        self.passwd = gui.CTkEntry(self, placeholder_text='Password', font=button_font)
        self.sign_in = gui.CTkButton(self, text='Sign In', font=button_font, command=self.sign_in)
        self.sign_up = gui.CTkButton(self, text='Sign Up', font=button_font, command=self.sign_up)
        self.exit_button = gui.CTkButton(self, text='Exit', font=button_font, command=finish)
        self.info_frame = gui.CTkFrame(self, corner_radius=10)
        self.info = gui.CTkLabel(self.info_frame, text='Sign in an existing account', font=button_font)

        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='new')
        self.login.grid(row=1, column=0, padx=10, pady=(10, 5), sticky='new')
        self.passwd.grid(row=2, column=0, padx=10, pady=(5, 5), sticky='new')
        self.sign_in.grid(row=3, column=0, padx=10, pady=(5, 5), sticky='sew')
        self.info_frame.grid(row=4, column=0, padx=10, pady=(5, 10), sticky='ew')
        self.info.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        self.sign_up.grid(row=5, column=0, padx=10, pady=(10, 5), sticky='sew')
        self.exit_button.grid(row=6, column=0, padx=10, pady=(5, 10), sticky='sew')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)
        self.info_frame.columnconfigure(0, weight=1)

    def sign_in(self):
        password = self.passwd.get()
        hash_pass = passwd.passwd(password)
        username = self.login.get()
        if password != '' and username != '':
            if db_handler.check(return_param='Boolean', username=username) and db_handler.check(return_param='Boolean',
                                                                                                passwd=hash_pass):
                db_handler.update(user=username, isCurrent='1')
                open_main()
            else:
                self.info.configure(text='Incorrect username or password!')
        else:
            self.info.configure(text='Both fields must be filled!')

    def sign_up(self):
        open_sign_up()


class SignUp(gui.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sign Up Window")
        self.geometry("300x400")
        self.minsize(300, 400)
        self.security_code = None

        self.label = gui.CTkLabel(self, text='Sign Up', font=hi_label_font)
        self.username_entry = gui.CTkEntry(self, placeholder_text='Username', font=button_font)
        self.passwd_entry = gui.CTkEntry(self, placeholder_text='Password', font=button_font)
        self.email_entry = gui.CTkEntry(self, placeholder_text='Email', font=button_font)
        self.sec_code_entry = gui.CTkEntry(self, placeholder_text='Secure code', font=button_font)
        self.next_button = gui.CTkButton(self, text='Next', font=button_font, command=self.check)
        self.info_frame = gui.CTkFrame(self, corner_radius=10)
        self.info = gui.CTkLabel(self.info_frame, text=f'sign up window {version}', font=button_font,
                                 text_color='#444444')
        self.exit_button = gui.CTkButton(self, text='Exit', font=button_font, command=finish)

        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='new')
        self.username_entry.grid(row=1, column=0, padx=10, pady=(10, 5), sticky='new')
        self.passwd_entry.grid(row=2, column=0, padx=10, pady=(5, 5), sticky='new')
        self.email_entry.grid(row=3, column=0, padx=10, pady=(5, 5), sticky='new')
        self.info_frame.grid(row=6, column=0, padx=10, pady=10, sticky='new')
        self.info.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        self.next_button.grid(row=5, column=0, padx=10, pady=10, sticky='new')
        self.exit_button.grid(row=7, column=0, padx=10, pady=10, sticky='sew')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(7, weight=1)
        self.info_frame.columnconfigure(0, weight=1)

    def check(self):
        username = self.username_entry.get()
        password = self.passwd_entry.get()
        email = self.email_entry.get()
        if username != '' and password != '' and email != '':
            self.info.configure(text='Proceeding...', text_color='#777777')
            if not db_handler.check(return_param='Boolean', username=username):
                self.send_code()
            else:
                self.info.configure(text='An account with this username\nalready exists',
                                    text_color='#edbf5c')
        else:
            self.info.configure(text='All fields must be filled!', text_color='#FFFFFF')

    def send_code(self):
        username = self.username_entry.get()
        password = self.passwd_entry.get()
        email = self.email_entry.get()
        self.security_code = random.randint(10000, 99999)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('sssashhhka@gmail.com', 'nfxoqckmkocnxvii')

            mime = 'MIME-Version: 1.0'
            charset = 'Content-Type: text/plain; charset=utf-8'
            text = f"Your account username: {username}\n" \
                   f"Your password: {password}\n" \
                   f"Security code: {self.security_code}"
            msg = "\r\n".join((f"From: sssashhhka@gmail.com", f"To: {email}",
                               f"Subject: Email verification", mime, charset, "", text))

            server.sendmail('sssashhhka@gmail.com', email, msg.encode('utf-8'))

            server.quit()
        except smtplib.SMTPRecipientsRefused:
            self.info.configure(text='Invalid email format!', text_color='#ed5151')
        else:
            self.info.configure(text='Check your mailbox\nfor security code we sent', text_color='#FFFFFF')
            self.sec_code_entry.grid(row=4, column=0, padx=10, pady=(5, 10), sticky='new')
            self.next_button.configure('Sign Up', command=self.check_code)

    def check_code(self):
        password = passwd.passwd(self.passwd_entry.get())
        if self.sec_code_entry.get() == str(self.security_code):
            db_handler.insert(username=self.username_entry.get(), passwd=password,
                              email=self.email_entry.get())
            open_main()
        else:
            self.info.configure(text='Invalid secure code!', text_color='#ed5151')


def open_main():
    sign_in.withdraw()
    sign_up.withdraw()
    time.sleep(0.1)
    main.deiconify()
    main.mainloop()


def open_sign_in():
    main.withdraw()
    sign_up.withdraw()
    time.sleep(0.1)
    sign_in.deiconify()
    sign_in.mainloop()


def open_sign_up():
    sign_in.iconify()
    time.sleep(0.1)
    sign_up.deiconify()
    sign_up.mainloop()


def finish():
    time.sleep(0.1)
    exit(0)


main = Main()
sign_in = SignIn()
sign_up = SignUp()


if __name__ == '__main__':
    print(f"User: {current_user}, Appearance: {current_theme}, Theme: {current_clr_theme}")
    if current_user is None:
        open_sign_in()
    else:
        main.set_clrtheme(current_clr_theme)
        main.mainloop()
