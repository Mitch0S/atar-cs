import sqlite3
import time
import traceback

class SQL:
    def __init__(self):
        pass

    def check_membership_number(self, **kwargs):
        allowed_values = '1234567890'

        if kwargs['membership_number'] == '':
            return {'status': 'error', 'reason': 'Membership number is empty.'}

        for number in kwargs['membership_number']:
            if str(number) not in allowed_values:
                return {'status': 'error', 'reason': 'Membership number must \n     only contain numbers'}

        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f'SELECT * FROM attendees WHERE membership_number = "{kwargs["membership_number"]}"'
        query = cursor.execute(sql)
        query_response = query.fetchone()
        if query_response != None:
            return {'status': 'ok', 'reason': 'successfully logged in', 'data': {'user': query_response}}
        else:
            return {'status': 'error', 'reason': 'incorrect membership number', 'data': {}}



    def registration(self, **kwargs):
        try:
            required_kwargs = ['first_name', 'last_name', 'email', 'mobile_number', 'membership_number', 'company_id', 'shirt_size']
            missing_required_kwargs = []
            for required_kwarg in required_kwargs:
                if required_kwarg not in kwargs:
                    missing_required_kwargs.append(required_kwarg)

            if len(missing_required_kwargs) > 0:
                return {'status': 'error', 'reason': 'missing required information', 'data': {'kwargs': {'missing': missing_required_kwargs, 'required': required_kwargs}}}

            for kwarg in kwargs:
                print(f"[DEBUG] {kwarg} = '{kwargs[kwarg]}'")
                if kwarg == None:
                    return {'status': 'error', 'reason': f"{kwarg.replace('_', ' ')} has in invalid value"}

                if kwargs[kwarg] == "":
                    return {'status': 'error', 'reason': f"{kwarg.replace('_', ' ')} is empty"}

            if len(kwargs['mobile_number']) < 12:
                return {'status': 'error', 'reason': 'invalid mobile number'}

            try:
                connection = sqlite3.connect('./pages/sql/online_booking_system.db')
                cursor = connection.cursor()
                sql = f"""INSERT INTO attendees (first_name, last_name, email, mobile_number, membership_number, company_id, shirt_size)
                               VALUES ("{kwargs['first_name']}", "{kwargs['last_name']}", "{kwargs['email']}", "{kwargs['mobile_number']}", "{kwargs['membership_number']}", "{kwargs['company_id']}", "{kwargs['shirt_size']}")
                       """
                cursor.execute(sql)
                connection.commit()
                return {'status': 'ok', 'reason': 'successfully signed up', 'data': {
                    'user_object': {
                        'first_name': kwargs['first_name'],
                        'last_name': kwargs['last_name'],
                        'membership_number': kwargs['membership_number'],
                        'email': kwargs['email'],
                        'mobile_number': kwargs['mobile_number']
                    }
                }}
            except sqlite3.IntegrityError as error:
                print(error)
                error = str(error)
                if "UNIQUE" in error:
                    return {'status': 'error', 'reason': f'an account with the same {error.split(".")[1].replace("_", " ")} already exists'}

        except Exception as error:
            traceback.print_exc()

    def get_attendee_booking(self, **kwargs):
        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f"""SELECT presenters.first_name,
                         presenters.last_name,
                         workshop_details.title,
                         workshop_details.description,
                         workshop_details.start_time,
                         workshop_details.end_time,
                         workshop_details.room_number
                
                  FROM presenters, workshop_details, workshop_bookings, attendees
                
                  WHERE attendees.membership_number = "{kwargs["membership_number"]}"
                  AND attendees.attendee_id = workshop_bookings.attendee_id
                  AND presenters.presenter_id = workshop_details.presenter_id
                  AND workshop_details.workshop_id = workshop_bookings.workshop_id"""
        query = cursor.execute(sql)
        query_response = query.fetchone()
        if query_response != None:
            return {'status': 'ok', 'reason': 'user has booking', 'data': {'booking_data': query_response}}
        else:
            return {'status': 'ok', 'reason': 'user has no booking', 'data': {'booking_data': None}}


    def get_booking_availability(self, **kwargs):
        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f'SELECT COUNT(workshop_id) FROM workshop_bookings WHERE workshop_id = {kwargs["workshop_id"]}'
        query = cursor.execute(sql)
        current_booking_amount = query.fetchone()[0]

        sql = f'SELECT capacity_max FROM workshop_details WHERE workshop_id = {kwargs["workshop_id"]}'
        query = cursor.execute(sql)
        workshop_capacity = query.fetchone()[0]

        if not current_booking_amount >= workshop_capacity:
            return {'status': 'ok', 'reason': 'workshop has available capacity', 'data': {
                'max_capacity': workshop_capacity,
                'current_bookings': current_booking_amount,
                'available': True
            }}

        else:
            return {'status': 'error', 'reason': 'workshop has reached the maximum booking capacity', 'data': {
                'max_capacity': workshop_capacity,
                'current_bookings': current_booking_amount,
                'available': False
            }}

    def get_companies(self):
        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f'SELECT * FROM companies'
        query = cursor.execute(sql)
        companies = query.fetchall()
        company_dict = {}
        for company in companies:
            company_dict[company[1]] = company[0]

        return {'status': 'ok', 'reason': 'successfully got companies', 'data': {'companies': company_dict}}

    def get_workshops(self):
        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f'SELECT title, workshop_id FROM workshop_details'
        query = cursor.execute(sql)
        companies = query.fetchall()
        company_dict = {}
        for company in companies:
            company_dict[company[0]] = company[1]

        return {'status': 'ok', 'reason': 'successfully got workshops', 'data': {'workshops': company_dict}}

    def get_workshop_details(self, **kwargs):
        if 'workshop_id' not in kwargs:
            return {'status': 'error', 'reason': 'no workshop_id was passed in kwargs'}

        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f"""
            SELECT first_name, last_name, title, description, start_time, end_time, room_number
            FROM presenters, workshop_details
            WHERE presenters.presenter_id = workshop_details.presenter_id
              AND workshop_details.workshop_id = {kwargs['workshop_id']}
               """
        query = cursor.execute(sql)
        workshop_details = query.fetchone()
        return {'status': 'ok', 'reason': 'retrieved workshop details', 'data': {'workshop_details': workshop_details}}

    def create_booking(self, **kwargs):
        if 'workshop_id' not in kwargs:
            return {'status': 'error', 'reason': 'no workshop_id was passed in kwargs'}

        if 'attendee_id' not in kwargs:
            return {'status': 'error', 'reason': 'no workshop_id was passed in kwargs'}

        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f"""
            INSERT INTO workshop_bookings (attendee_id, workshop_id, date_booked)
            VALUES ({kwargs['attendee_id']}, {kwargs['workshop_id']}, {time.time()})
               """
        query = cursor.execute(sql)
        connection.commit()
        workshop_details = query.fetchone()
        return {'status': 'ok', 'reason': 'created new booking'}

    def delete_booking(self, **kwargs):
        """
        DELETE FROM workshop_bookings
        WHERE attendee_id = 1
        """
        if 'attendee_id' not in kwargs:
            return {'status': 'error', 'reason': 'no workshop_id was passed in kwargs'}

        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f"""
            DELETE FROM workshop_bookings
            WHERE attendee_id = {kwargs['attendee_id']}
               """
        query = cursor.execute(sql)
        connection.commit()
        return {'status': 'ok', 'reason': 'successfully deleted booking'}

    def edit_booking(self, **kwargs):
        if 'attendee_id' not in kwargs:
            return {'status': 'error', 'reason': 'no workshop_id was passed in kwargs'}

        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f"""
            UPDATE workshop_bookings
               SET workshop_id = {kwargs['workshop_id']}
               AND attendee_id = {kwargs['attendee_id']}
               """

        query = cursor.execute(sql)
        connection.commit()
        return {'status': 'ok', 'reason': 'successfully deleted booking'}


# SQL().get_workshop_details(workshop_id=2)
# SQL().get_workshops()
# print(SQL().check_membership_number(membership_number=1234567890))
# print(SQL().get_attendee_booking(membership_number="1234567890"))
# print(SQL().get_booking_availability(workshop_id=1))
