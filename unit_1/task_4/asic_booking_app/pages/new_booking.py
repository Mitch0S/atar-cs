import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
from .sql import SQL
from tkinter.messagebox import showinfo

class NewBookingScreen:
    def __init__(self, **kwargs):
        pass

    def load(self, **kwargs):
        self.root = kwargs['root']
        root = self.root
        self.x = kwargs['x']
        self.y = kwargs['y']

        self.data = kwargs['data']

        x = self.x
        y = self.y

        self.new_booking_screen_elements = []

        # Places the Purple-Blue Gradient on Background
        background_gradient = Image.open("./resources/images/app_gradient.png")
        background_gradient = background_gradient.resize((x + 15, y))
        background_gradient = ImageTk.PhotoImage(background_gradient)
        background_label = tkinter.ttk.Label(root, image=background_gradient)
        background_label.place(x=x / 2, y=y / 2, anchor='center')

        # Places the element background image on Background
        element_box = Image.open("./resources/images/element_box.png")
        element_box = element_box.resize((500, 700))
        element_box = ImageTk.PhotoImage(element_box)
        element_box_label = tkinter.ttk.Label(root, image=element_box)
        self.new_booking_screen_elements.append(element_box_label)
        element_box_label.place(x=x / 2, y=y / 2, anchor='center')

        # Place ASIC Logo on the top left of the screen
        asic_logo = Image.open("./resources/images/asic_logo.png")
        asic_logo = asic_logo.resize((100, 100))
        asic_logo = ImageTk.PhotoImage(asic_logo)
        asic_logo_label = tkinter.ttk.Label(root, image=asic_logo)
        self.new_booking_screen_elements.append(asic_logo_label)
        asic_logo_label.place(x=x / 2 - 175, y=y / 2 - 275, anchor='center')

        # Places "ASIC Booking App" Text below Logo
        asic_login_text = tkinter.ttk.Label(root, text='ASIC Booking App', font=('catamaran', 40, 'italic'), )
        self.new_booking_screen_elements.append(asic_login_text)
        asic_login_text.place(x=x / 2 + 55, y=y / 2 - 275, anchor='center')

        # Places "Home" Text below Logo
        asic_login_text = tkinter.ttk.Label(root, text='Home', font=('catamaran', 20, 'italic'), )
        self.new_booking_screen_elements.append(asic_login_text)
        asic_login_text.place(x=x / 2, y=y / 2 - 200, anchor='center')

        back_to_home = customtkinter.CTkButton(root, text="Cancel", fg_color='gray', hover_color='dark gray', command=self.back_to_home_button)
        self.new_booking_screen_elements.append(back_to_home)
        back_to_home.place(x=x / 2, y=y / 2 + 300, anchor='center')


        root.mainloop()

    def back_to_home_button(self, **kwargs):
        from .home import HomeScreen
        for element in self.new_booking_screen_elements:
            try:
                element.destroy()
            except:
                print(f'[DEBUG] Element `{element}` could not be destroyed.')

        HomeScreen().load(root=self.root, x=self.x, y=self.y, data=self.data)



    def confirm_booking(self, **kwargs):
        query = SQL().get_booking_availability(workshop_id=kwargs['workshop_id'])



