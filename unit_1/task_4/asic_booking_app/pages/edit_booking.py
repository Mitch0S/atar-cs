import textwrap
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
from .sql import SQL
import datetime

class EditBookingScreen:
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

        self.membership_number = kwargs['data']['membership_number']
        self.edit_booking_screen_elements = []

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
        self.edit_booking_screen_elements.append(element_box_label)
        element_box_label.place(x=x / 2, y=y / 2, anchor='center')

        # Place ASIC Logo on the top left of the screen
        asic_logo = Image.open("./resources/images/asic_logo.png")
        asic_logo = asic_logo.resize((100, 100))
        asic_logo = ImageTk.PhotoImage(asic_logo)
        asic_logo_label = tkinter.ttk.Label(root, image=asic_logo)
        self.edit_booking_screen_elements.append(asic_logo_label)
        asic_logo_label.place(x=x / 2 - 175, y=y / 2 - 275, anchor='center')

        # Places "ASIC Booking App" Text below Logo
        asic_login_text = tkinter.ttk.Label(root, text='ASIC Booking App', font=('catamaran', 40, 'italic'), )
        self.edit_booking_screen_elements.append(asic_login_text)
        asic_login_text.place(x=x / 2 + 55, y=y / 2 - 275, anchor='center')

        # Places "Home" Text below Logo
        asic_login_text = tkinter.ttk.Label(root, text='Edit Booking', font=('catamaran', 20, 'italic'), )
        self.edit_booking_screen_elements.append(asic_login_text)
        asic_login_text.place(x=x / 2, y=y / 2 - 200, anchor='center')

        query = SQL().get_workshops()
        if query['status'] == 'ok':
            self.workshop_dict = query['data']['workshops']
            workshop_list = []
            for workshop in self.workshop_dict:
                workshop_list.append(workshop)
        else:
            print('[DEBUG] Unable to connect to database')
            exit()

        self.default_workshop_booking = tkinter.StringVar()
        self.default_workshop_booking.set("Workshop")
        self.workshop_booking = tkinter.ttk.OptionMenu(root, self.default_workshop_booking, "Workshop", *workshop_list, command=self.update_workshop_details)
        self.workshop_booking.place(x=x / 2, y=y / 2 - 150, anchor="center")

        self.back_to_home_button = customtkinter.CTkButton(root, text="Cancel", text_color='dark grey', hover=False, fg_color=None, hover_color=None, command=self.back_to_home)
        self.edit_booking_screen_elements.append(self.back_to_home_button)
        self.back_to_home_button.place(x=x / 2, y=y / 2 + 320, anchor='center')

        newline = '\n'

        self.workshop_info = customtkinter.CTkLabel(self.root, text=f"""
                   Workshop Details
               -----------------------{4*newline}Select a workshop above to display details {8*newline}""", height=325, width=225, fg_color=("white", "gray38"), justify=tkinter.LEFT)
        self.workshop_info.place(x=self.x / 2, y=self.y / 2 + 35, anchor='center')

        self.confirm_booking_button = customtkinter.CTkButton(root, text="Confirm", fg_color='gray', hover_color='dark gray', command=self.confirm_booking)
        self.edit_booking_screen_elements.append(self.confirm_booking_button)
        self.confirm_booking_button.place(x=x / 2, y=y / 2 + 270, anchor='center')

        root.mainloop()

    def back_to_home(self, **kwargs):
        print('Back to home')
        from .home import HomeScreen
        for element in self.edit_booking_screen_elements:
            try:
                element.destroy()
            except:
                print(f'[DEBUG] Element `{element}` could not be destroyed.')

        HomeScreen().load(root=self.root, x=self.x, y=self.y, data=self.data)



    def confirm_booking(self):
        query = SQL().check_membership_number(membership_number=self.membership_number)
        if query['status'] == 'ok':
            attendee_id = query['data']['user'][0]


        query = SQL().get_booking_availability(workshop_id=self.workshop_dict[self.default_workshop_booking.get()])
        if query['status'] == 'ok':
            if query['data']['available'] == True:
                SQL().edit_booking(attendee_id=attendee_id, workshop_id=self.workshop_dict[self.default_workshop_booking.get()])

                self.confirm_booking_button.destroy()
                self.back_to_home_button.destroy()

                self.home_button = customtkinter.CTkButton(self.root, text="Home", fg_color='gray', hover_color='dark gray', command=self.back_to_home)
                self.edit_booking_screen_elements.append(self.home_button)
                self.home_button.place(x=self.x / 2, y=self.y / 2 + 290, anchor='center')

                self.success_text = tkinter.ttk.Label(text=f'Successfully updated your booking. You may return to home.', foreground='light green')
                self.edit_booking_screen_elements.append(self.success_text)
                self.success_text.place(x=self.x / 2, y=self.y / 2 + 230, anchor='center')


        else:
            self.error_text = tkinter.ttk.Label(text=f'Error, {query["reason"]}', foreground='red')
            self.edit_booking_screen_elements.append(self.error_text)
            self.error_text.place(x=self.x / 2, y=self.y / 2 + 230, anchor='center')



    def update_workshop_details(self, *args, **kwargs):
        workshop_value = self.default_workshop_booking.get()
        workshop_id = self.workshop_dict[workshop_value]
        query = SQL().get_workshop_details(workshop_id=workshop_id)
        if query['status'] == 'ok':
            workshop_details = query['data']['workshop_details']


        newline = '\n                              '
        newline.join(textwrap.wrap(workshop_details[3], 45))

        try:
            self.workshop_info.destroy()
        except:
            pass

        self.workshop_info = customtkinter.CTkLabel(self.root, text=f"""
                               Workshop Details
                           -----------------------

        Title: {workshop_details[2]}

        Description: {newline.join(textwrap.wrap(workshop_details[3], 45))}

        Presenter: {workshop_details[0]} {workshop_details[1]}

        Start Time: {datetime.datetime.fromtimestamp(workshop_details[4]).strftime("%d/%m/%Y, %H:%M")}

        End Time: {datetime.datetime.fromtimestamp(workshop_details[5]).strftime("%d/%m/%Y, %H:%M")}

        Room Number: {workshop_details[6]}
        
        """,
                                                   height=325,
                                                   width=225,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.workshop_info.place(x=self.x / 2, y=self.y / 2 + 35, anchor='center')



