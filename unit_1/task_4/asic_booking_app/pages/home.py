import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
from .sql import SQL
import time
import datetime

class HomeScreen:
    def __init__(self, **kwargs):
        pass

    def load(self, **kwargs):

        print('[DEBUG] User logged in')

        self.data = kwargs['data']
        data = self.data

        self.root = kwargs['root']
        root = self.root
        self.x = kwargs['x']
        self.y = kwargs['y']

        x = self.x
        y = self.y

        self.home_screen_elements = []

        """
          1) Check if a user has a booking
        
        1.1) Global Elements
               - Logo (TOP LEFT)
               - "Home Page" Label
        
        1.2) If they don't have a booking, load the following:
               - `Create Booking` Button
               - "No booking, create one" label
               
        1.3)  If they do have a booking, load the following:
               - "Your Booking" Label
               - "Booking Details" Label
               - `Change Booking` button
               - `Remove Booking` button
        """


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
        self.home_screen_elements.append(element_box_label)
        element_box_label.place(x=x / 2, y=y / 2, anchor='center')

        # Place ASIC Logo on the top left of the screen
        asic_logo = Image.open("./resources/images/asic_logo.png")
        asic_logo = asic_logo.resize((100, 100))
        asic_logo = ImageTk.PhotoImage(asic_logo)
        asic_logo_label = tkinter.ttk.Label(root, image=asic_logo)
        self.home_screen_elements.append(asic_logo_label)
        asic_logo_label.place(x=x / 2-175, y=y / 2 - 275, anchor='center')

        # Places "ASIC Booking App" Text below Logo
        asic_login_text = tkinter.ttk.Label(root, text='ASIC Booking App', font=('catamaran', 40, 'italic'), )
        self.home_screen_elements.append(asic_login_text)
        asic_login_text.place(x=x / 2+55, y=y / 2 - 275, anchor='center')

        # Places "Home" Text below Logo
        asic_login_text = tkinter.ttk.Label(root, text='Home', font=('catamaran', 20, 'italic'), )
        self.home_screen_elements.append(asic_login_text)
        asic_login_text.place(x=x / 2, y=y / 2 - 200, anchor='center')

        # Places Membership Number Submit button on login screen
        login_submit_button = customtkinter.CTkButton(root, text="Logout", fg_color='gray',
                                                      hover_color='dark gray', command=self.do_logout)
        self.home_screen_elements.append(login_submit_button)
        login_submit_button.place(x=x/2 - 185, y=y/2 + 330, anchor='center')

        query = SQL().get_attendee_booking(membership_number=self.data['membership_number'])
        if query['status'] == 'ok':
            if query['data']['booking_data'] != None:
                self.has_booking(booking_data=query['data']['booking_data'])
                pass

            else:
                # TODO: Load `no booking` function
                self.has_no_booking()
                pass

    def has_booking(self, **kwargs):
        root = self.root
        x = self.x
        y = self.y

        booking_data = kwargs['booking_data']

        self.label_info_1 = customtkinter.CTkLabel(root,
                                                   text=f"""
                       Your Booking
                   --------------------
                
Workshop: {booking_data[2]}
    
Description: {booking_data[3]}
    
Presenter: {booking_data[0]} {booking_data[1]}

Start Time: {datetime.datetime.fromtimestamp(booking_data[4]).strftime( "%d/%m/%Y, %H:%M")}

End Time: {datetime.datetime.fromtimestamp(booking_data[5]).strftime( "%d/%m/%Y, %H:%M")}

Room Number: {booking_data[6]}

""",
                                                   height=325,
                                                   width=200,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.place(x=x/2, y=y/2, anchor='center')

        # Places Membership Number Submit button on login screen
        change_booking_button = customtkinter.CTkButton(root, text="Change Booking", fg_color='gray', hover_color='dark gray')
        self.home_screen_elements.append(change_booking_button)
        change_booking_button.place(x=x / 2-75, y=y / 2 + 200, anchor='center')

        # Places Membership Number Submit button on login screen
        login_submit_button = customtkinter.CTkButton(root, text="Cancel Booking", fg_color='gray', hover_color='dark gray')
        self.home_screen_elements.append(login_submit_button)
        login_submit_button.place(x=x / 2+75, y=y / 2 + 200, anchor='center')

        print('[DEBUG] Home window loaded successfully')

        root.mainloop()

        # Places Membership Number Submit button on login screen

    def has_no_booking(self, **kwargs):
        root = self.root
        x = self.x
        y = self.y

        self.booking_details = customtkinter.CTkLabel(root,
                                                   text=f"""
                               Your Booking
                           --------------------

        You currently do not have a booking, click the 
        "New Booking" button below to book one.

        """,
                                                   height=325,
                                                   width=200,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.home_screen_elements.append(self.booking_details)
        self.booking_details.place(x=x / 2, y=y / 2, anchor='center')

        # Places Membership Number Submit button on login screen
        new_booking_button = customtkinter.CTkButton(root, text="New Booking", fg_color='gray',
                                                        hover_color='dark gray', command=self.do_new_booking_button)
        self.home_screen_elements.append(new_booking_button)
        new_booking_button.place(x=x / 2, y=y / 2 + 200, anchor='center')

        root.mainloop()


    def do_new_booking_button(self, **kwargs):
        from .new_booking import NewBookingScreen
        for element in self.home_screen_elements:
            try:
                element.destroy()
            except:
                print(f'[DEBUG] Element `{element}` could not be destroyed.')

        NewBookingScreen().load(root=self.root, x=self.x, y=self.y, data=self.data)



    def do_logout(self):
        from .login import LoginScreen
        for element in self.home_screen_elements:
            try:
                element.destroy()
            except:
                print(f'[DEBUG] Element `{element}` could not be destroyed.')

        print('[DEBUG] User logged out.')
        LoginScreen().load(root=self.root, x=self.x, y=self.y)



