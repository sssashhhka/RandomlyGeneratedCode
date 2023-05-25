import customtkinter as gui


class SignUpWindow(gui.CTk):
    def __init__(self):
        super().__init__()

        self.title('Sign Up')
        self.geometry('350x450')

        self.hiLabel_font = gui.CTkFont(family='Segoe UI Variable', size=25, weight='normal')
        self.midLabel_font = gui.CTkFont(family='Segoe UI Variable', size=20, weight='normal')
        self.button_font = gui.CTkFont(family='Segoe UI Variable', size=15, weight='normal')

        self.label = gui.CTkLabel(self, text='Sign Up', font=self.hiLabel_font)

        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='new')

        self.columnconfigure(0, weight=1)


app = SignUpWindow()

if __name__ == '__main__':
    app.mainloop()
