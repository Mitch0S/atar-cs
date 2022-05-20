import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
from .sql import SQL

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
        element_box = element_box.resize((300, 500))
        element_box = ImageTk.PhotoImage(element_box)
        element_box_label = tkinter.ttk.Label(root, image=element_box)
        self.new_booking_screen_elements.append(element_box_label)
        element_box_label.place(x=x / 2, y=y / 2 - 75, anchor='center')

        # Places ASIC Logo on login screen
        asic_logo = Image.open("./resources/images/asic_logo.png")
        asic_logo = asic_logo.resize((150, 150))
        asic_logo = ImageTk.PhotoImage(asic_logo)
        asic_logo_label = tkinter.ttk.Label(root, image=asic_logo)
        self.new_booking_screen_elements.append(asic_logo_label)
        asic_logo_label.place(x=x/2, y=y/2-200, anchor='center')

        # Places Login Text below Logo
        asic_new_booking_text = tkinter.ttk.Label(root, text='ASIC Booking App', font='catamaran')
        self.new_booking_screen_elements.append(asic_new_booking_text)
        asic_new_booking_text.place(x=x / 2, y=y / 2 - 80, anchor='center')

        back_to_home = customtkinter.CTkButton(root, text="Back", fg_color='gray', hover_color='dark gray',
                                                      command=self.back_to_home_button)
        self.new_booking_screen_elements.append(back_to_home)
        back_to_home.place(x=x / 2, y=y / 2 + 100, anchor='center')


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



