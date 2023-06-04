import random
import customtkinter as gui
import smtplib
from utility import passwd, db_handler
from assets.fonts import *


class SignUpWindow(gui.CTk):
    def __init__(self):
        super().__init__()

        self.security_code = None
        self.title('Sign Up')
        self.geometry('300x400')

        self.label = gui.CTkLabel(self, text='Sign Up', font=hi_label_font)
        self.username_entry = gui.CTkEntry(self, placeholder_text='Username', font=button_font)
        self.passwd_entry = gui.CTkEntry(self, placeholder_text='Password', font=button_font)
        self.email_entry = gui.CTkEntry(self, placeholder_text='Email', font=button_font)
        self.sec_code_entry = gui.CTkEntry(self, placeholder_text='Secure code', font=button_font)
        self.next_button = gui.CTkButton(self, text='Next', font=button_font, command=self.check)
        self.info_frame = gui.CTkFrame(self, corner_radius=10)
        self.info = gui.CTkLabel(self.info_frame, text='sign up window v0.1b build 1', font=button_font,
                                 text_color='#444444')
        self.exit_button = gui.CTkButton(self, text='Exit', font=button_font, command=exit)

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
        passwod = self.passwd_entry.get()
        email = self.email_entry.get()
        self.security_code = random.randint(10000, 99999)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('sssashhhka@gmail.com', 'nfxoqckmkocnxvii')

            mime = 'MIME-Version: 1.0'
            charset = 'Content-Type: text/plain; charset=utf-8'
            text = f"Your account username: {username}\n" \
                   f"Your password: {passwod}\n" \
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
            self.withdraw()
            from Main_Window import start
            start()
        else:
            self.info.configure(text='Invalid secure code!', text_color='#ed5151')


def start():
    app.mainloop()


app = SignUpWindow()

if __name__ == '__main__':
    app.mainloop()
