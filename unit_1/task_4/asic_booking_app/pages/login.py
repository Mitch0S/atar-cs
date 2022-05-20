import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
from .sql import SQL
from .home import HomeScreen

class LoginScreen:
    def __init__(self, **kwargs):
        pass

    def load(self, **kwargs):
        self.root = kwargs['root']
        root = self.root
        self.x = kwargs['x']
        self.y = kwargs['y']

        x = self.x
        y = self.y

        self.login_screen_elements = []

        # Places the Purple-Blue Gradient on Background
        background_gradient = Image.open("./resources/images/app_gradient.png")
        background_gradient = background_gradient.resize((x + 15, y))
        background_gradient = ImageTk.PhotoImage(background_gradient)
        background_label = tkinter.ttk.Label(root, image=background_gradient)
        background_label.place(x=x / 2, y=y / 2, anchor='center')

        # Places the element background image on Background
        element_box = Image.open("./resources/images/element_box.png")
        element_box = element_box.resize((300, 500))
        element_box = ImageTk.PhotoImage(element_box)
        element_box_label = tkinter.ttk.Label(root, image=element_box)
        self.login_screen_elements.append(element_box_label)
        element_box_label.place(x=x / 2, y=y / 2 - 75, anchor='center')

        # Places ASIC Logo on login screen
        asic_logo = Image.open("./resources/images/asic_logo.png")
        asic_logo = asic_logo.resize((150, 150))
        asic_logo = ImageTk.PhotoImage(asic_logo)
        asic_logo_label = tkinter.ttk.Label(root, image=asic_logo)
        self.login_screen_elements.append(asic_logo_label)
        asic_logo_label.place(x=x/2, y=y/2-200, anchor='center')

        # Places Login Text below Logo
        asic_login_text = tkinter.ttk.Label(root, text='ASIC Booking App', font='catamaran')
        self.login_screen_elements.append(asic_login_text)
        asic_login_text.place(x=x / 2, y=y / 2 - 80, anchor='center')

        # Places Membership Number Entry box on login screen
        self.membership_number_entry = customtkinter.CTkEntry(root, width=240, placeholder_text="Membership Number", fg_color='white', text_color='black', placeholder_text_color='gray')
        self.login_screen_elements.append(self.membership_number_entry)
        membership_number_entry_label = self.membership_number_entry.place(x=x / 2, y=y / 2, anchor='center')

        # Places Membership Number Submit button on login screen
        login_submit_button = customtkinter.CTkButton(root, text="Login", fg_color='gray', hover_color='dark gray', command=self.do_login)
        self.login_screen_elements.append(login_submit_button)
        login_submit_button.place(x=x / 2, y=y / 2 + 100, anchor='center')

        self.root.mainloop()

    def do_login(self):
        membership_number = self.membership_number_entry.get()
        query = SQL().check_membership_number(membership_number=membership_number)
        try:
            self.error_text.destroy()
            self.success_text.destroy()
        except:
            pass

        if query['status'] == 'ok':
            for element in self.login_screen_elements:
                try:
                    element.destroy()
                except:
                    print(f'[DEBUG] Element `{element}` could not be destroyed.')


            HomeScreen().load(membership_number=membership_number, root=self.root, x=self.x, y=self.y, data={'membership_number': membership_number})

            print('[DEBUG] Loading home page')


        else:
            print(f"[DEBUG] Error: {query['reason'].strip()}")
            self.error_text = tkinter.ttk.Label(text=f'Error, {query["reason"]}', foreground='red')
            self.login_screen_elements.append(self.error_text)
            self.error_text.place(x=self.x/2, y=self.y/2+40, anchor='center')
