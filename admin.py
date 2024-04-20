
import tkinter as tk
from tkinter import messagebox as m
from tkinter import ttk
from datetime import *
import db


class Admin:

    def __init__(self):

        # ------------------Header------------------

        root = tk.Tk()
        root.title("Admin Panel")
        root.iconbitmap("ao.ico")
        root.minsize(1000 , 600)
        root.rowconfigure(1, weight = 1)
        root.rowconfigure(2, weight = 1)
        root.rowconfigure(3, weight = 1)
        root.rowconfigure(4, weight = 1)
        root.rowconfigure(5, weight = 1)
        root.rowconfigure(6, weight = 1)
        root.rowconfigure(7, weight = 1)
        root.rowconfigure(8, weight = 1)
        root.columnconfigure(0, weight = 2)
        root.columnconfigure(2, weight = 1)
        root.columnconfigure(3, weight = 1)
        root.columnconfigure(4, weight = 1)
        root.columnconfigure(5, weight = 3)

        # Styling

        style = {"fg": "#ef7150", "bg": "#efefef", "font": "Cairo 14 bold"}
        padding = {"padx": 7, "pady": 7}

        # Button styling

        btn_style= {"font": "Cairo  10 bold", "fg" : "#b4403d" , "width" : 17}

        # Title

        title = tk.Label(root, text="Admin Panel",
                      font="cairo 30 bold", bg="#efefef", fg="#b4403d")
        title.grid(row=0, column=1, columnspan=4, sticky='we', **padding)

        # ------------------Body------------------

        # Add user fuction   [ ↓ ]

        def add_user():
            from signup import Sign_up

            # Close the admin panel and redirect to the sign up page

            root.destroy()
            Sign_up()

        # Add reservation fuction   [ ↓ ]

        def add_res():
            from reservation import Reservation

            # Close the admin panel and redirect to the reservation page

            root.destroy()
            Reservation()


        # Search fuction   [ ↓↓↓ ]

        def search():

            # Collecting data from the entries

            self.username = name_search_entry.get().strip()
            self.email = email_search_entry.get().strip()
            self.phone = phone_search_entry.get().strip()

            # Counting how many entries are written in them

            count_entries = 0
            search_entries = [self.username, self.email, self.phone]

            for entry in search_entries:
                if entry != "":
                    count_entries += 1

            # Checking if all fields are empty

            if self.username == "" and self.email == "" and self.phone == "":
                m.showerror("Error!", "All fields are empty")

            # Checking if more than one entry has been written in it

            elif count_entries > 1:
                m.showerror("Error!", "Can not search with more than one entry")

            # Searching by username   [ ↓↓ ]

            elif self.username != "":

                username_query = "SELECT username, email, phone, gender, user_id FROM users WHERE username = %s;"
                db.curs.execute(username_query, (self.username,))
                username_result = db.curs.fetchone()

                # Checking if the username searched by exists

                if username_result is None:
                    m.showerror("Error!", "Username doesn't exist")
                    return

                # printing the values returned from the users table to the screen

                else:
                    self.username_label["text"] = f"Username : {username_result[0]}"
                    self.email_label["text"] = f"Email : {username_result[1]}"
                    self.phone_label["text"] = f"Phone : {username_result[2]}"
                    self.gender_label["text"] = f"Gender : {username_result[3]}"

                # Selecting max reservation id from reservation table

                max_res_key = "SELECT MAX(reservation_key) FROM reservation WHERE user_id = %s;"
                db.curs.execute(max_res_key, (username_result[4],))
                max_key_result = db.curs.fetchone()

                # Selecting reservation details from reservation table

                reservation_details = "SELECT room_type, num_of_rooms, checkin_date , checkout_date, price FROM reservation WHERE reservation_key = %s;"
                db.curs.execute(reservation_details, (max_key_result[0],))
                details_result = db.curs.fetchone()

                # Checking if the user exists
                
                if details_result is None:

                    m.showinfo("Note.", "There is no reservation done by this user")
                    self.reservationlabel["text"] = f"Reservation Key : None"
                    self.room_type_label["text"] = f"Room Type : None"
                    self.room_num_label["text"] = f"Number of Rooms : None"
                    self.checkin_label["text"] = f"Check-in Date : None"
                    self.checkout_label["text"] = f"Check-out Date : None"
                    self.price_label["text"] = f"Price : None"

                else:

                    # Checking if this user has never reserved before

                    if date.today() > details_result[3]:

                        m.showinfo("Note.", "There is no current reservation by this user")
                        self.reservationlabel["text"] = f"Reservation Key : None"
                        self.room_type_label["text"] = f"Room Type : None"
                        self.room_num_label["text"] = f"Number of Rooms : None"
                        self.checkin_label["text"] = f"Check-in Date : None"
                        self.checkout_label["text"] = f"Check-out Date : None"
                        self.price_label["text"] = f"Price : None"

                    # Printing the current reservation details

                    else:
                        self.reservationlabel["text"] = f"Reservation Key : {max_key_result[0]}"
                        self.room_type_label["text"] = f"Room Type : {details_result[0]}"
                        self.room_num_label["text"] = f"Number of Rooms : {details_result[1]}"
                        self.checkin_label["text"] = f"Check-in Date : {details_result[2]}"
                        self.checkout_label["text"] = f"Check-out Date : {details_result[3]}"
                        self.price_label["text"] = f"Price : {details_result[4]}"

            # Searching by email   [ ↓↓ ]

            elif self.email != "":

                email_query = "SELECT username, email, phone, gender, user_id FROM users WHERE email = %s;"
                db.curs.execute(email_query, (self.email,))
                email_result = db.curs.fetchone()

                # Checking if the email searched by exists

                if email_result is None:
                    m.showerror("Error!", "Email doesn't exist")
                    return

                # printing the values returned from the users table to the screen

                else:
                    self.username_label["text"] = f"Username : {email_result[0]}"
                    self.email_label["text"] = f"Email : {email_result[1]}"
                    self.phone_label["text"] = f"Phone : {email_result[2]}"
                    self.gender_label["text"] = f"Gender : {email_result[3]}"

                # Selecting max reservation id from reservation table

                max_res_key = "SELECT MAX(reservation_key) FROM reservation WHERE user_id = %s;"
                db.curs.execute(max_res_key, (email_result[4],))
                max_key_result = db.curs.fetchone()

                # Selecting reservation details from reservation table

                reservation_details = "SELECT room_type, num_of_rooms, checkin_date , checkout_date, price FROM reservation WHERE reservation_key = %s;"
                db.curs.execute(reservation_details, (max_key_result[0],))
                details_result = db.curs.fetchone()

                # Checking if the user exists
                
                if details_result is None:

                    m.showinfo("Note.", "There is no reservation done by this user")
                    self.reservationlabel["text"] = f"Reservation Key : None"
                    self.room_type_label["text"] = f"Room Type : None"
                    self.room_num_label["text"] = f"Number of Rooms : None"
                    self.checkin_label["text"] = f"Check-in Date : None"
                    self.checkout_label["text"] = f"Check-out Date : None"
                    self.price_label["text"] = f"Price : None"

                else:

                    # Checking if this user has never reserved before
                   
                    if date.today() > details_result[3]:

                        m.showinfo("Note.", "There is no current reservation by this user")
                        self.reservationlabel["text"] = f"Reservation Key : None"
                        self.room_type_label["text"] = f"Room Type : None"
                        self.room_num_label["text"] = f"Number of Rooms : None"
                        self.checkin_label["text"] = f"Check-in Date : None"
                        self.checkout_label["text"] = f"Check-out Date : None"
                        self.price_label["text"] = f"Price : None"

                     # Printing the current reservation details

                    else:
                        self.reservationlabel["text"] = f"Reservation Key : {max_key_result[0]}"
                        self.room_type_label["text"] = f"Room Type : {details_result[0]}"
                        self.room_num_label["text"] = f"Number of Rooms : {details_result[1]}"
                        self.checkin_label["text"] = f"Check-in Date : {details_result[2]}"
                        self.checkout_label["text"] = f"Check-out Date : {details_result[3]}"
                        self.price_label["text"] = f"Price : {details_result[4]}"

            # Searching by phone number   [ ↓↓ ]

            else:

                phone_query = "SELECT username, email, phone, gender, user_id FROM users WHERE phone = %s;"
                db.curs.execute(phone_query, (self.phone,))
                phone_result = db.curs.fetchone()

                # Checking if the phone number searched by exists

                if phone_result is None:
                    m.showerror("Error!", "Phone number doesn't exist")
                    return

                # printing the values returned from the database to the screen

                else:
                    self.username_label["text"] = f"Username : {phone_result[0]}"
                    self.email_label["text"] = f"Email : {phone_result[1]}"
                    self.phone_label["text"] = f"Phone : {phone_result[2]}"
                    self.gender_label["text"] = f"Gender : {phone_result[3]}"

                # Selecting max reservation id from reservation table

                max_res_key = "SELECT MAX(reservation_key) FROM reservation WHERE user_id = %s;"
                db.curs.execute(max_res_key, (phone_result[4],))
                max_key_result = db.curs.fetchone()

                # Selecting reservation details from reservation table

                reservation_details = "SELECT room_type, num_of_rooms, checkin_date , checkout_date, price FROM reservation WHERE reservation_key = %s;"
                db.curs.execute(reservation_details, (max_key_result[0],))
                details_result = db.curs.fetchone()

                # Checking if the user exists

                if details_result is None:

                    m.showinfo("Note.", "There is no reservation done by this user")
                    self.reservationlabel["text"] = f"Reservation Key : None"
                    self.room_type_label["text"] = f"Room Type : None"
                    self.room_num_label["text"] = f"Number of Rooms : None"
                    self.checkin_label["text"] = f"Check-in Date : None"
                    self.checkout_label["text"] = f"Check-out Date : None"
                    self.price_label["text"] = f"Price : None"

                else:

                    # Checking if this user has never reserved before
                   
                    if date.today() > details_result[3]:

                        m.showinfo("Note.", "There is no current reservation by this user")
                        self.reservationlabel["text"] = f"Reservation Key : None"
                        self.room_type_label["text"] = f"Room Type : None"
                        self.room_num_label["text"] = f"Number of Rooms : None"
                        self.checkin_label["text"] = f"Check-in Date : None"
                        self.checkout_label["text"] = f"Check-out Date : None"
                        self.price_label["text"] = f"Price : None"

                     # Printing the current reservation details

                    else:
                        self.reservationlabel["text"] = f"Reservation Key : {max_key_result[0]}"
                        self.room_type_label["text"] = f"Room Type : {details_result[0]}"
                        self.room_num_label["text"] = f"Number of Rooms : {details_result[1]}"
                        self.checkin_label["text"] = f"Check-in Date : {details_result[2]}"
                        self.checkout_label["text"] = f"Check-out Date : {details_result[3]}"
                        self.price_label["text"] = f"Price : {details_result[4]}"

        # Delete fuction   [ ↓↓↓ ]

        def delete_user():

           # Collecting data from the entries

            self.username = name_search_entry.get().strip()
            self.email = email_search_entry.get().strip()
            self.phone = phone_search_entry.get().strip()

            # Counting how many entries are written in them

            count_entries = 0
            search_entries = [self.username, self.email, self.phone]

            for entry in search_entries:
                if entry != "":
                    count_entries += 1

            # Checking if all fields are empty

            if self.username == "" and self.email == "" and self.phone == "":
                m.showerror("Error!", "All fields are empty")

            # Checking if more than one entry has been written in it

            elif count_entries > 1:
                m.showerror("Error!", "Can not delete with more than one entry")

            # Deleting user by username   [ ↓↓ ]

            elif self.username != "":

                # Select the user id from users table

                select_userID_name = "SELECT user_id FROM users WHERE username = %s;"
                db.curs.execute(select_userID_name, (self.username,))
                select_result_name = db.curs.fetchone()

                # Checking if the username deleted by exists

                if select_result_name is None:
                    m.showerror("Error!", "Username doesn't exist")
                    return

            # Checking if the admin wants to delete this user

                delete_user1 = m.askokcancel(
                            "Delete confirmation", "Are you sure you want to delete this user ?", icon="warning")

                if delete_user1:

                    # Delete query to delete the user from reservation table and delete all his reservations

                    delete_res_name = "DELETE FROM reservation WHERE user_id = %s;"
                    db.curs.execute(delete_res_name, (select_result_name[0],))

                    # Delete query to delete the user from users table

                    delete_user_name = "DELETE FROM users WHERE username = %s;"
                    db.curs.execute(delete_user_name, (self.username,))

                    # Saving the changes to users and reservation tables

                    db.conn.commit()
                    m.showinfo("Success", "User deleted successfully")

            # Deleting user by email   [ ↓↓ ]

            elif self.email != "":

                # Select the user id from users table

                select_userID_email = "SELECT user_id FROM users WHERE email = %s;"
                db.curs.execute(select_userID_email, (self.email,))
                select_result_email = db.curs.fetchone()

                # Checking if the email deleted by exists

                if select_result_email is None:
                    m.showerror("Error!", "Email doesn't exist")
                    return

                # Checking if the admin wants to delete this user

                delete_user2 = m.askokcancel(
                            "Delete confirmation", "Are you sure you want to delete this user ?", icon="warning")

                if delete_user2:

                    # Delete query to delete the user from reservation table and delete all his reservations

                    delete_res_email = "DELETE FROM reservation WHERE user_id = %s;"
                    db.curs.execute(delete_res_email, (select_result_email[0],))

                    # Delete query that deletes the selected user

                    delete_user_email = "DELETE FROM users WHERE email = %s;"
                    db.curs.execute(delete_user_email, (self.email,))

                    # Saving the changes to users and reservation tables

                    db.conn.commit()
                    m.showinfo("Success", "User deleted successfully")

            # Deleting user by phone number   [ ↓↓ ]

            elif self.phone != "":

                # Select the user id from users table

                select_userID_phone = "SELECT user_id FROM users WHERE phone = %s;"
                db.curs.execute(select_userID_phone, (self.phone,))
                select_result_phone = db.curs.fetchone()

                # Checking if the phone number deleted by exists

                if select_result_phone is None:
                    m.showerror("Error!", "Phone number doesn't exist")
                    return

                # Checking if the admin wants to delete this user

                delete_user3 = m.askokcancel(
                            "Delete confirmation", "Are you sure you want to delete this user ?", icon="warning")

                if delete_user3:

                    # Delete query to delete the user from reservation table and delete all his reservations

                    delete_res_phone = "DELETE FROM reservation WHERE user_id = %s;"
                    db.curs.execute(delete_res_phone, (select_result_phone[0],))

                    # Delete query that deletes the selected user

                    delete_user_phone = "DELETE FROM users WHERE phone = %s;"
                    db.curs.execute(delete_user_phone, (self.phone,))

                    # Saving the changes to users and reservation tables

                    db.conn.commit()
                    m.showinfo("Success", "User deleted successfully")
                

        # Cancel reservation fuction   [ ↓↓↓ ]

        def cancel_res():

            if self.reservationlabel["text"][18:] == "None" or self.reservationlabel["text"][18:] == "":
                m.showerror("Error!", "There is no reservation selected to be canceled")
            
            else:

                cancel_res = m.askokcancel(
                            "Cancel confirmation", "Are you sure you want to cancel this reservation ?", icon="warning")

                if cancel_res:

                    # Delete query to delete the reservation from reservation table

                    cancel_query = "DELETE FROM reservation WHERE reservation_key = %s;"
                    db.curs.execute(cancel_query, (self.reservationlabel["text"][18:],))

                    # Saving the changes to users and reservation tables

                    db.conn.commit()
                    m.showinfo("Success", "Reservation canceled successfully")


        # Entries and Labels  [ ↓↓↓ ]


        # Search by Username

        name_search = tk.StringVar()

        name_search_label = tk.Label(root, text="Search by Name" , **style)
        name_search_label.grid(row = 1 , column= 2)

        name_search_entry = tk.Entry(root, textvariable=name_search, **style)
        name_search_entry.grid(row = 2 , column= 2 , padx= 15, sticky="we")

        # Search by Email

        email_search = tk.StringVar()
        
        email_search_label = tk.Label(root, text="Search by Email" , **style)
        email_search_label.grid(row =  1, column= 3)

        email_search_entry = tk.Entry(root, textvariable=email_search, **style)
        email_search_entry.grid(row = 2 , column= 3, sticky="we")

        # Search by Phone number

        phone_search = tk.StringVar()

        phone_search_label = tk.Label(root, text="Search by Phone" , **style)
        phone_search_label.grid(row =  1, column= 4)

        phone_search_entry = tk.Entry(root, textvariable=phone_search, **style)
        phone_search_entry.grid(row = 2 , column= 4 , padx=15, sticky="we")

        # Username label

        self.username_label = tk.Label(root , text="Username :" , anchor="w", font="Cairo 14")
        self.username_label.grid(row=4 , column=2 ,sticky="w", padx=15)

        # Email label

        self.email_label = tk.Label(root , text="Email :" , anchor="w", font="Cairo 14")
        self.email_label.grid(row=5 , column=2 ,sticky="w", padx=15)

        # Phone number label

        self.phone_label = tk.Label(root , text="Phone :", font="Cairo 14")
        self.phone_label.grid(row=6 , column=2,sticky="w", padx=15)

        # Gender label

        self.gender_label = tk.Label(root , text="Gender :", font="Cairo 14")
        self.gender_label.grid(row=7 , column=2,sticky="w", padx=15)

        # Reservation label

        self.reservationlabel = tk.Label(root, text="Reservation Key :", font="Cairo 14")
        self.reservationlabel.grid(row=4, column=3, sticky="w", padx=15)

        # Room type label

        self.room_type_label = tk.Label(root, text="Room Type :", font="Cairo 14")
        self.room_type_label.grid(row=5, column=3, sticky="w", padx=15)

        # Number of rooms label

        self.room_num_label = tk.Label(root, text="Number of Rooms :", font="Cairo 14")
        self.room_num_label.grid(row=5, column=4, sticky="w", padx=15)

        # Check-in date label

        self.checkin_label = tk.Label(root, text="Check-in Date :", font="Cairo 14")
        self.checkin_label.grid(row=6, column=3, sticky="w", padx=15)

        # Check-out date label

        self.checkout_label = tk.Label(root, text="Check-out Date :", font="Cairo 14")
        self.checkout_label.grid(row=6, column=4, sticky="w", padx=15)

        # Price label

        self.price_label =tk.Label(root, text="Price :", font="Cairo 14")
        self.price_label.grid(row=7, column=3, sticky="w", padx=15)


        # Buttons  [ ↓↓↓ ]


        # Search button

        search_btn = tk.Button(root, text="Search", **btn_style, command=search, cursor="hand2")
        search_btn.grid(row = 2, column= 0)

        # Add user button

        add_user_btn = tk.Button(root, text="Add User", **btn_style, command=add_user, cursor="hand2")
        add_user_btn.grid(row = 4, column= 0)

        # Delete user button

        del_user_btn = tk.Button(root, text="Delete User", **btn_style, command=delete_user, cursor="hand2")
        del_user_btn.grid(row = 5, column= 0)

        # Add reservation button

        add_res_btn = tk.Button(root, text="Add Reservation", **btn_style, command=add_res, cursor="hand2")
        add_res_btn.grid(row = 6, column= 0)

        # Cancel reservation button

        del_res_btn = tk.Button(root, text="Cancel Reservation" , **btn_style, command=cancel_res, cursor="hand2")
        del_res_btn.grid(row = 7 , column= 0 )

        root.mainloop()


if __name__ == "__main__":

    app = Admin()
