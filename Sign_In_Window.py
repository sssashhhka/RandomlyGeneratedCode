import customtkinter as gui
import db_handler
import passwd
from assets.fonts import *


def sign_up():
    from Sign_Up_Window import start
    app.withdraw()
    start()


class SignInWindow(gui.CTk):
    def __init__(self):
        super().__init__()

        self.title('Sign In')
        self.geometry('300x400')
        self.minsize(300, 400)

        self.label = gui.CTkLabel(self, text='Sign In', font=hi_label_font)
        self.login = gui.CTkEntry(self, placeholder_text='Username', font=button_font)
        self.passwd = gui.CTkEntry(self, placeholder_text='Password', font=button_font)
        self.sign_in = gui.CTkButton(self, text='Sign In', font=button_font, command=self.sign_in)
        self.sign_up = gui.CTkButton(self, text='Sign Up', font=button_font, command=sign_up)
        self.exit = gui.CTkButton(self, text='Exit', font=button_font)
        self.info_frame = gui.CTkFrame(self, corner_radius=10)
        self.info = gui.CTkLabel(self.info_frame, text='Sign in an existing account', font=button_font)

        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='new')
        self.login.grid(row=1, column=0, padx=10, pady=(10, 5), sticky='new')
        self.passwd.grid(row=2, column=0, padx=10, pady=(5, 5), sticky='new')
        self.sign_in.grid(row=3, column=0, padx=10, pady=(5, 5), sticky='sew')
        self.info_frame.grid(row=4, column=0, padx=10, pady=(5, 10), sticky='ew')
        self.info.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        self.sign_up.grid(row=5, column=0, padx=10, pady=(10, 5), sticky='sew')
        self.exit.grid(row=6, column=0, padx=10, pady=(5, 10), sticky='sew')

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
                self.withdraw()
                from Main_Window import start
                start()
            else:
                self.info.configure(text='Incorrect username or password!')
        else:
            self.info.configure(text='Both fields must be filled!')


app = SignInWindow()


def startsi():
    app.mainloop()
    app.deiconify()


if __name__ == '__main__':
    app.mainloop()
