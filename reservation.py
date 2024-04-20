import tkinter as tk
from tkinter import messagebox as mb
from tkinter.ttk import *
import tkcalendar as tkc
from tkinter import PhotoImage
from datetime import *
import db


class Reservation:

    def __init__(self):

        # ------------------Header------------------

        root = tk.Tk()
        root.title("AO Reservation")
        root.iconbitmap("ao.ico")
        root.minsize(1000, 600)
        root.rowconfigure(0, weight=2)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)
        root.rowconfigure(6, weight=4)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(5, weight=1)

        # Styling

        label_style = {"fg": "#ef7150",
                       "bg": "#efefef", "font": "Cairo 11 bold"}
        padding = {"padx": 7, "pady": 7}

        # Button styling

        btn_style = {"font": "Cairo  10 bold",
                     "fg": "#b4403d", "width": 10, "height": 1}

        # Background image

        bg = PhotoImage(file="bg.png")
        bg_label = Label(root, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title

        title = tk.Label(root, text="AO Hotel Reservation",
                      font="cairo 30 bold", bg="#efefef", fg="#b4403d")
        title.grid(row=0, column=1, columnspan=4, sticky='we', **padding)

        # ------------------Body------------------

        # Clear fuction   [ ↓↓ ]

        def clear():

            room_type.set("Select Room")
            number_of_rooms_entry.delete(0, "end")
            checkin_date_entry.set_date(date.today())
            checkout_date_entry.set_date(date.today())
            phone_entry.delete(0, "end")
            total_price_label["text"] = "0 EGP"

        # Validate entries function   [ ↓↓↓ ]

        def validate_entries():

            # Collecting data from the entries

            checkin_date_str = checkin_date_entry.get()
            checkout_date_str = checkout_date_entry.get()
            num_rooms = number_of_rooms.get().strip()
            selected_room_type = room_type.get()
            phone_number = phone_entry.get()

            # Check-in and check-out dates in [ date format ]

            checkin_date = datetime.strptime(checkin_date_str, "%m/%d/%y")
            checkout_date = datetime.strptime(checkout_date_str, "%m/%d/%y")

            # Check-in and today's dates in [ string format ]

            date_check_in = datetime.strftime(checkin_date, "%Y-%m-%d")
            today_date = datetime.strftime(date.today(), "%Y-%m-%d")

            # Select query returns the phone number from database

            validate_phone = "SELECT phone FROM users WHERE phone = %s;"
            db.curs.execute(validate_phone, (phone_number,))
            phone_result = db.curs.fetchone()

            # Checking that the user select a room type

            if selected_room_type == "Select Room":
                mb.showerror("Error!", "Please Choose a room type")

            # Checking that the number of rooms is not empty

            elif num_rooms == "":
                mb.showerror("Error!", "Please Enter number of rooms")

            # Checking that the number of rooms is just digits

            elif not num_rooms.isdigit():
                mb.showerror("Error!", "Number of rooms should be an integer")

            # Checking that the number of rooms is not 0

            elif num_rooms == '0':
                mb.showerror("Error!", "Number of rooms can't be 0")

            # Checking if the user enters more than 20 rooms of each type

            elif (selected_room_type == "Single" and int(num_rooms) >= 20) or (selected_room_type == "Double" and int(num_rooms) >= 20):
                mb.showerror("Error!", "We don't have this number of rooms from this type, Please Choose fewer number of rooms")

            # Checking if the user enters more than 4 suites

            elif selected_room_type == "Suite" and int(num_rooms) >= 4:
                mb.showerror("Error!", "We don't have this number of suites, Please Choose fewer number of suites")

            # Checking that the checkin date is not earlier than todays's date [string format]

            elif date_check_in < today_date:
                mb.showerror("Error!", "Check-in date can not be earlier than today's date")

            # Checking that the checkout date is not earlier than the checkin date [date format]

            elif checkin_date > checkout_date:
                mb.showerror("Error!", "Check-out date can not be earlier than check-in date")

            # Checking that the checkout date is not equal to the checkin date [date format]

            elif checkin_date == checkout_date:
                mb.showerror("Error!", "Check-out date can not be equal to check-in date")
            
            # Checking that the phone number isn't empty
            
            elif phone_number == "":
                mb.showerror("Error!", "Please Enter your phone number")

            # Checking that the phone number doesn't exists

            elif phone_result is None:
                mb.showerror("Error!", "Phone Number doesn't exist, Please recheck")
            
            else:
                return True
            
            return False
        
        # Validate room function   [ ↓↓↓ ]
        
        def validate_rooms(how_many_rooms, type):

            # Collecting data from the entries

            checkin_date_str = checkin_date_entry.get()
            checkout_date_str = checkout_date_entry.get()
            num_rooms = number_of_rooms.get().strip()

            # Check-in and check-out dates in [ date format ]

            checkin_date = datetime.strptime(checkin_date_str, "%m/%d/%y")
            checkout_date = datetime.strptime(checkout_date_str, "%m/%d/%y")

            # Check-in and check-out dates in [ string format ]

            date_check_in = datetime.strftime(checkin_date, "%Y-%m-%d")
            date_check_out = datetime.strftime(checkout_date, "%Y-%m-%d")

            check_num_rooms = 0
            num_of_rows = 0

            # Select query returns room type, check-in and check-out dates from reservation table

            is_empty = "SELECT num_of_rooms, checkin_date, checkout_date FROM reservation WHERE room_type = %s;"

            db.curs.execute(is_empty, (type,))
            roomID_result = db.curs.fetchall()

            # Checking if the room type was saved in the database before

            if roomID_result is not None:

                for roomid in roomID_result:
                    
                    for i in range(0, roomid[0]):
                        num_of_rows += 1

                        # Checking if the check-out date of this room is after the check-in date of that the user has selected 
                        # or check-out date that the user selected is after the check-in date of this room

                        if date_check_in < str(roomid[2]) and date_check_out > str(roomid[1]):
                            continue

                        # The room is empty and can be reserved

                        else:
                            check_num_rooms += 1

                            # Checking if the number of rooms the user wants equals the actual empty rooms

                            if check_num_rooms == int(num_rooms) or (how_many_rooms - int(num_rooms)) > num_of_rows:
                                return True
                        
            # Just the first time to this room type to be reserved [ single, double, suite ]        

            else:
                return True
                    
            check_num_rooms = check_num_rooms + (how_many_rooms - num_of_rows)

            # Checking if all rooms were full

            if check_num_rooms == 0:
                mb.showerror("Error!", "Sorry, All rooms are full, Please try again later")

            # Checking if the number of rooms the user wants is fewer than the actual number of empty rooms

            elif check_num_rooms < int(num_rooms):
                mb.showerror("Error!", "Sorry, This number of rooms isn't available at the moment, Please choose fewer number of rooms")

            else:
                return True

            return False
        
        # Total price function   [ ↓↓ ]

        def total_price():

            # Entries validation

            check_entries = validate_entries()

            if check_entries == False:
                return
            
            # Setting each room type price
            
            if room_type.get() == "Single" :
                room_price.set(500)

            elif room_type.get() == "Double":
                room_price.set(1000)

            else: 
                room_price.set(3000)
            
            # Calculate reservation period in days

            checkin_date_str = checkin_date_entry.get()
            checkout_date_str = checkout_date_entry.get()

            checkin_date = datetime.strptime(checkin_date_str, "%m/%d/%y")
            checkout_date = datetime.strptime(checkout_date_str, "%m/%d/%y")
            duration = (checkout_date - checkin_date).days

            # Printing total price

            total_price_label["text"] = f"{room_price.get() * int(number_of_rooms.get()) * duration} EGP"

        # Sumbit function   [ ↓↓↓ ]

        def submit():

            # Entries validation

            check_entries = validate_entries()

            if check_entries == False:
                return

            # Collecting data from the entries

            checkin_date_str = checkin_date_entry.get()
            checkout_date_str = checkout_date_entry.get()
            num_rooms = number_of_rooms.get().strip()
            selected_room_price = room_price.get()
            selected_room_type = room_type.get()
            phone_number = phone_entry.get()
            
            # Check-in and check-out dates in [ date format ]

            checkin_date = datetime.strptime(checkin_date_str, "%m/%d/%y")
            checkout_date = datetime.strptime(checkout_date_str, "%m/%d/%y")

            # Check-in and check-out dates in [ string format ]

            date_check_in = datetime.strftime(checkin_date, "%Y-%m-%d")
            date_check_out = datetime.strftime(checkout_date, "%Y-%m-%d")

            # Reservation duration in days

            duration = (checkout_date - checkin_date).days

            # Calculating total price

            price = selected_room_price * int(num_rooms) * duration

            # Getting user id from users table
            
            userID = "SELECT user_id FROM users WHERE phone = %s ;"

            db.curs.execute(userID, (phone_number,))
            userID_result = db.curs.fetchone()

            # Getting maximum reservation id from reservation table

            reservationID = "SELECT MAX(reservation_key) FROM reservation;"

            db.curs.execute(reservationID)
            reservationID_result = db.curs.fetchone()

            # Calling the validate rooms function according to each room type

            if selected_room_type == "Single":

               validation = validate_rooms(20, "single")

            elif selected_room_type == "Double":

                validation = validate_rooms(20, "double")

            else:
                validation = validate_rooms(4, "suite")

            if validation:

                # Saving user information   [ ↓ ]

                mb.showinfo("Success", f"Reservation successful, Your reservation number is: {reservationID_result[0] + 1}")

                # Inserting reservation data into the raservation table

                inserting_query = """ INSERT INTO reservation(user_id, room_type, num_of_rooms, checkin_date, checkout_date, price)
                                                     VALUES(%s, %s, %s, %s, %s, %s); """
                values = [userID_result[0], selected_room_type, num_rooms, date_check_in, date_check_out, price]

                db.curs.execute(inserting_query, values)

                # Saving the changes to the database

                db.conn.commit()

                # Calling clear function to clear all the entries after reservation

                clear()


        # Entries and Labels  [ ↓↓↓ ]


        # Room Type
        
        room_type_label = tk.Label(root, text = "Room Type", **label_style)
        room_type_label.grid(row = 1, column = 1, **padding)

        # Combo box

        room_type = tk.StringVar()
        room_price = tk.IntVar()
        room_type.set("Select Room")
        
        room_choices = ["Single", "Double", "Suite"]
   
        room_type_dropdown = Combobox(root, textvariable=room_type, values=room_choices, state= "readonly", font="cairo 8 bold" )
        room_type_dropdown.grid(row=1, column=2,**padding)

        # Number of rooms

        number_of_rooms = tk.StringVar()

        number_of_rooms_label = tk.Label(root, text="Number of Rooms", **label_style)
        number_of_rooms_label.grid(row=1, column=3, **padding)

        number_of_rooms_entry = tk.Entry(root, textvariable=number_of_rooms, bd=0)
        number_of_rooms_entry.grid(row=1, column=4, ipady = 2, **padding)

        # Check-in date

        checkin_date_label = tk.Label(root, text="Check in date", **label_style)
        checkin_date_label.grid(row=2, column=1, sticky="e", **padding)

        checkin_date_entry = tkc.DateEntry(root)
        checkin_date_entry.grid(row=2, column=2, sticky = "we", **padding)

        # Check-out date

        checkout_date_label = tk.Label(root, text="Check out date", **label_style)
        checkout_date_label.grid(row=2, column=3, sticky="e", **padding)

        checkout_date_entry = tkc.DateEntry(root)
        checkout_date_entry.grid(row=2, column=4, sticky="we", **padding)

        # Phone number

        phone = tk.StringVar()

        phone_label = tk.Label(root, text="Phone Number", **label_style)
        phone_label.grid(row=3, column=2, sticky="e")

        phone_entry = tk.Entry(root,  bd=0)
        phone_entry.grid(row=3, column=3, ipady = 2, **padding)

        # Total price

        total_price_label = tk.Label(root, text="0 EGP", **btn_style)
        total_price_label.grid(row=4, column=4, **padding)


        # Buttons   [ ↓↓ ]


        # Total price button

        total_price_button = tk.Button(root, text="Total Price", **btn_style, command=total_price, cursor="hand2")
        total_price_button.grid(row=4, column=3, **padding)

        # Submit button

        submit_button = tk.Button(root, text="Submit", **btn_style, command=submit, cursor="hand2")
        submit_button.grid(row=5, column=2, **padding, ipadx=5)

        root.mainloop()


if __name__ == "__main__":
    app = Reservation()
