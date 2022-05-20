import sqlite3


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

        #if len(kwargs['membership_number']) > 10 or len(kwargs['membership_number']) < 10:
        #    return {'status': 'error', 'reason': 'Membership Number must be 10 digits'}

        connection = sqlite3.connect('./pages/sql/online_booking_system.db')
        cursor = connection.cursor()
        sql = f'SELECT * FROM attendees WHERE membership_number = "{kwargs["membership_number"]}"'
        query = cursor.execute(sql)
        query_response = query.fetchone()
        if query_response != None:
            return {'status': 'ok', 'reason': 'successfully logged in', 'data': {'user': query_response}}
        else:
            return {'status': 'error', 'reason': 'incorrect membership number', 'data': {}}

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
        connection = sqlite3.connect('online_booking_system.db')
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
                'current_bookings': current_booking_amount
            }}

        else:
            return {'status': 'error', 'reason': 'workshop has reached the maximum booking capacity', 'data': {
                'max_capacity': workshop_capacity,
                'current_bookings': current_booking_amount
            }}





# print(SQL().check_membership_number(membership_number=1234567890))
# print(SQL().get_attendee_booking(membership_number="1234567890"))
# print(SQL().get_booking_availability(workshop_id=1))
