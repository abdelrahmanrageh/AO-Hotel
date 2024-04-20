from tkinter import *
import tkinter as tk
from tkinter import messagebox as m
import tkinter.ttk as ttk
import db


class New_password:
    def __init__(self):

        # ------------------Header------------------

        root = Toplevel()
        root.title("Reset Password")
        root.iconbitmap("ao.ico")
        root.minsize(700, 450)
        root.maxsize(700, 450)
        root.resizable(0, 0)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(3, weight=1)
        root.rowconfigure(8, weight=1)

        # Styling

        label_style = {"font": 'Cairo, 10  bold', "bg": "#efefef", "fg": "#ef7150"}
        padding = {"padx": -0, "pady": 7}

        # Button styling

        btn_style = {"font": "Cairo  10 bold", "fg": "#b4403d", "width": 10, "height": 1}

        # Title

        title = tk.Label(root, text="Reset Password", font="cairo 20 bold", bg="#efefef", fg="#b4403d")
        title.grid(row=0, column=1, columnspan=2, pady=10)

        text = tk.Label(root, text="Your Password will not be updated if Username, Email and Phone Number are not entered correctly.",
                        font="Cairo  9 ", bg="#efefef", fg="red")
        text.grid(row=1, column=0, columnspan=4, **padding)

        # ------------------Body------------------

        # Show password fuction   [ ↓↓ ]

        def show_pass():
            eye_image.configure(file="view.png")
            new_password_entry.config(show="")
            self.eye_btn = Button(root, image=eye_image, bd=0, bg="white", command=hide_pass,
                                  activebackground="white").grid(row=5, column=2, padx=5, sticky="e")

        # Hide password fuction   [ ↓↓ ]

        def hide_pass():
            eye_image.configure(file="hide.png")
            new_password_entry.config(show="*")
            self.eye_btn = Button(root, image=eye_image, bd=0, bg="white", command=show_pass,
                                  activebackground="white").grid(row=5, column=2, padx=5, sticky="e")

        # Submit function   [ ↓↓↓ ]

        def submit():

            # Collecting data from the entries

            username = username_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            new_pass = new_password_entry.get()
            pass_conf = confirmation_entry.get()

            # Select query returns the username from database

            validate_username = "SELECT username FROM users WHERE username = %s;"
            db.curs.execute(validate_username, (username,))
            username_result = db.curs.fetchone()

            # Select query returns the email from database

            validate_email = "SELECT username FROM users WHERE email = %s;"
            db.curs.execute(validate_email, (email,))
            email_result = db.curs.fetchone()

            # Select query returns the phone number from database

            validate_phone = "SELECT username FROM users WHERE phone = %s;"
            db.curs.execute(validate_phone, (phone,))
            phone_result = db.curs.fetchone()

            # Checking that the username isn't empty

            if username == "":
                m.showerror("Error!", "Please Enter your username")

            # Checking that the email isn't empty

            elif email == "":
                m.showerror("Error!", "Please Enter your email")

            # Checking that the phone number isn't empty

            elif phone == "":
                m.showerror("Error!", "Please Enter your phone number")

            elif username_result == email_result == phone_result != None:

                # Checking that the password isn't empty

                if new_pass == "":
                    m.showerror("Error!", "Please Enter a password")

                # Checking that the password is more than 8 characters

                elif len(new_pass) < 8:
                    m.showerror("Error!", "Password should be 8 or more characters")

                # Checking that the password is less than 25 characters

                elif len(new_pass) > 25:
                    m.showerror("Error!", "Password should be less than 25 characters")

                # Checking that the password and the password confirmation are equal

                elif new_pass == pass_conf:

                    # Update query that changes the password

                    update_pass = "UPDATE users SET password = %s WHERE username = %s;"
                    values = (new_pass, username_result[0])

                    db.curs.execute(update_pass, values)

                    # Saving the changes to users table

                    db.conn.commit()

                    m.showinfo("Success", "Your password changed successfully")

                else:
                    m.showerror("Error!", "Your passwords should match each other, Please recheck")

            else:
                m.showerror("Error!", "Your credentials are not correct, Please recheck")


        # Entries   [ ↓↓↓ ]


        # Username

        username = StringVar()

        username_label = tk.Label(root, text="Username", **label_style)
        username_label.grid(row=2, column=1, sticky="w")

        username_entry = Entry(root, font="Cairo 10", bd=0)
        username_entry.grid(row=2, column=2, **padding)
        username_entry.focus()

        # Email

        email = StringVar()

        email_label = tk.Label(root, text="Email Address", **label_style)
        email_label.grid(row=3, column=1, sticky="w")

        email_entry = Entry(root, font="Cairo 10", bd=0)
        email_entry.grid(row=3, column=2, pady=7)

        # Phone

        phone = StringVar()

        phone_label = tk.Label(root, text="Phone Number", **label_style)
        phone_label.grid(row=4, column=1, sticky="w")

        phone_entry = Entry(root, font="Cairo 10", bd=0)
        phone_entry.grid(row=4, column=2, **padding)

        # New password

        new_password = StringVar()

        new_password_label = tk.Label(root, text="New Password", **label_style)
        new_password_label.grid(row=5, column=1, sticky="w")

        new_password_entry = Entry(root, font="Cairo 10", show="*", bd=0)
        new_password_entry.grid(row=5, column=2, **padding, sticky="e")

        # Confirmation

        confirmation = StringVar()

        confirmation_label = tk.Label(root, text="Confirm Password", **label_style)
        confirmation_label.grid(row=6, column=1, sticky="w")

        confirmation_entry = Entry(root, font="Cairo 10", show="*", bd=0)
        confirmation_entry.grid(row=6, column=2, **padding)


        # Buttons   [ ↓↓ ]


        # Show password button

        eye_image = PhotoImage(file="hide.png")
        self.eye_btn = Button(root, image=eye_image, bd=0, bg="white", command=show_pass,
                              activebackground="white").grid(row=5, column=2, padx=5, sticky="e")

        # Submit button

        submit_button = Button(root, text="Submit", **btn_style, cursor="hand2", command=submit)
        submit_button.grid(row=7, column=1, columnspan=2, **padding, ipadx=5)

        root.mainloop()


if __name__ == "__main__":
    login_window = New_password()
