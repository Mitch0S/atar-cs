import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
from .sql import SQL
from .home import HomeScreen

class RegisterScreen:
    def __init__(self, **kwargs):
        pass

    def load(self, **kwargs):
        print('[DEBUG] Register page loaded')


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
        element_box = element_box.resize((500, 700))
        element_box = ImageTk.PhotoImage(element_box)
        element_box_label = tkinter.ttk.Label(root, image=element_box)
        self.login_screen_elements.append(element_box_label)
        element_box_label.place(x=x / 2, y=y / 2 , anchor='center')

        # Places ASIC Logo on login screen
        asic_logo = Image.open("./resources/images/asic_logo.png")
        asic_logo = asic_logo.resize((150, 150))
        asic_logo = ImageTk.PhotoImage(asic_logo)
        asic_logo_label = tkinter.ttk.Label(root, image=asic_logo)
        self.login_screen_elements.append(asic_logo_label)
        asic_logo_label.place(x=x/2, y=y/2-225, anchor='center')

        # Places Login Text below Logo
        asic_register_text = tkinter.ttk.Label(root, text='ASIC Booking App - Registration', font='catamaran')
        self.login_screen_elements.append(asic_register_text)
        asic_register_text.place(x=x / 2, y=y / 2 - 120, anchor='center')

        # Places Membership Number Entry box on login screen
        self.first_name_entry = customtkinter.CTkEntry(root, width=120, placeholder_text="First Name", fg_color='white', text_color='black', placeholder_text_color='gray')
        self.login_screen_elements.append(self.first_name_entry)
        self.first_name_entry.place(x=x / 2 - 62, y=y / 2 - 50, anchor='center')

        self.last_name_entry = customtkinter.CTkEntry(root, width=120, placeholder_text="Last Name", fg_color='white', text_color='black', placeholder_text_color='gray')
        self.login_screen_elements.append(self.last_name_entry)
        self.last_name_entry.place(x=x / 2 + 62, y=y / 2 - 50, anchor='center')

        self.email_entry = customtkinter.CTkEntry(root, width=245, placeholder_text="Email", fg_color='white', text_color='black', placeholder_text_color='gray')
        self.login_screen_elements.append(self.email_entry)
        self.email_entry.place(x=x / 2, y=y / 2, anchor='center')

        self.default_country_code = tkinter.StringVar()
        self.default_country_code.set("+61")
        self.country_code = tkinter.ttk.OptionMenu(root, self.default_country_code, "+61", "+61", "+38", "+39", "+28", "+35", "+93")
        self.country_code.place(x=x/2 - 85, y=y/2 + 50, anchor="center")


        self.phone_entry = customtkinter.CTkEntry(root, width=160, placeholder_text="Phone Number", fg_color='white', text_color='black', placeholder_text_color='gray')
        self.login_screen_elements.append(self.phone_entry)
        self.phone_entry.place(x=x / 2 + 42.5, y=y / 2 + 50, anchor='center')


        # Places Membership Number Entry box on login screen
        self.membership_number_entry = customtkinter.CTkEntry(root, width=245, placeholder_text="Membership Number", fg_color='white', text_color='black', placeholder_text_color='gray')
        self.login_screen_elements.append(self.membership_number_entry)
        self.membership_number_entry.place(x=x / 2, y=y / 2 + 100, anchor='center')



        company_list = ['Company']
        company_data = SQL().get_companies()
        if company_data['status'] == 'ok':
            self.company_dict = company_data['data']['companies']
            for company in self.company_dict:
                company_list.append(company)

        self.default_company_value = tkinter.StringVar()
        self.default_company_value.set("Company")
        self.company_value = tkinter.ttk.OptionMenu(root, self.default_company_value, *company_list)
        self.company_value.place(x=x / 2, y=y / 2 + 142.5, anchor="center")

        self.default_shirt_size_value = tkinter.StringVar()
        self.default_shirt_size_value.set("Shirt Size")
        self.shirt_size_value = tkinter.ttk.OptionMenu(root, self.default_shirt_size_value, "Shirt Size", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL")
        self.shirt_size_value.place(x=x / 2, y=y / 2 + 180, anchor="center")



        # Places Membership Number Submit button on login screen
        register_submit_button = customtkinter.CTkButton(root, text="Register", fg_color='gray', hover_color='dark gray', command=self.do_registration)
        self.login_screen_elements.append(register_submit_button)
        register_submit_button.place(x=x / 2, y=y / 2 + 275, anchor='center')

        # Places Membership Number Submit button on login screen
        load_register_page = customtkinter.CTkButton(root, text='Login?', text_color='dark grey', fg_color=None, hover_color=None, command=self.load_registration_page)
        self.login_screen_elements.append(load_register_page)
        load_register_page.configure()
        load_register_page.place(x=x / 2, y=y / 2 + 325, anchor='center')

        self.root.mainloop()

    def do_registration(self):
        try:
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            email = self.email_entry.get()
            mobile_number = self.default_country_code.get() + self.phone_entry.get()
            membership_number = self.membership_number_entry.get()
            company_id = self.company_dict[self.default_company_value.get()]
            shirt_size = self.default_shirt_size_value.get()


            query = SQL().registration(first_name=first_name,
                                       last_name=last_name,
                                       email=email,
                                       mobile_number=mobile_number,
                                       membership_number=membership_number,
                                       company_id=company_id,
                                       shirt_size=shirt_size)

            try:
                self.error_text.destroy()
            except:
                pass

            if query['status'] == 'ok':
                for element in self.login_screen_elements:
                    try:
                        element.destroy()
                    except:
                        print(f'[DEBUG] Element `{element}` could not be destroyed.')

                HomeScreen().load(root=self.root, x=self.x, y=self.y, data={'membership_number': membership_number})
            else:
                print(f"[DEBUG] Error: {query['reason'].strip()}")
                self.error_text = tkinter.ttk.Label(text=f'Error, {query["reason"]}', foreground='red')
                self.login_screen_elements.append(self.error_text)
                self.error_text.place(x=self.x / 2, y=self.y / 2 + 225, anchor='center')

        except KeyError as error:
            print(f"[DEBUG] Error: {error}")
            self.error_text = tkinter.ttk.Label(text=f'Error, dropdown boxes can not be left as default', foreground='red')
            self.login_screen_elements.append(self.error_text)
            self.error_text.place(x=self.x / 2, y=self.y / 2 + 225, anchor='center')

    def load_registration_page(self):
        from .login import LoginScreen
        for element in self.login_screen_elements:
            try:
                element.destroy()
            except:
                print(f'[DEBUG] Element `{element}` could not be destroyed.')

        LoginScreen().load(root=self.root, x=self.x, y=self.y, data={})
