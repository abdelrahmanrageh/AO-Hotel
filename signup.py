import tkinter as tk
from tkinter import messagebox as m
from tkinter.ttk import *
from ttkthemes import *
import db
import re


class Sign_up:

    def __init__(self):

        # ------------------Header------------------

        root = tk.Tk()
        root.title("AO Sign Up")
        root.iconbitmap("ao.ico")
        root.minsize(1000, 600)
        root.rowconfigure(0, weight=2)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(4, weight=1)
        root.rowconfigure(7, weight=2)
        root.columnconfigure(0, weight=5)
        root.columnconfigure(4, weight=1)
        root.columnconfigure(7, weight=5)

        # styling

        style = {"fg": "#ef7150", "bg": "#efefef", "font": "Cairo 10 bold"}

        # Button styling

        btn_style = {"font": "Cairo  10 bold",
                     "fg": "#b4403d", "width": 10, "height": 1}

        # Background image

        bg = tk.PhotoImage(file="bg.png")

        bg_label = Label(root, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title

        title = tk.Label(root, text="AO Hotel Sign up",
      font="cairo 30 bold", bg="#efefef", fg="#b4403d")
        title.grid(row=0, column=1, columnspan=6, pady=10)

        # ------------------Body------------------

        # Back button function   [ ↓ ]

        def back_home():
            from home import Home

            # Close the login page and go back to home page

            root.destroy()
            Home()

        # Show password fuction   [ ↓↓ ]

        def show_pass():
            eye_image.configure(file="view.png")
            password_entry.config(show="")
            self.eye_btn = tk.Button(root, image=eye_image ,bd=0, bg="white", command=hide_pass , activebackground="white")
            self.eye_btn.grid(row = 3 , column =2 , padx=5 , sticky="e")

        # Hide password fuction   [ ↓↓ ]

        def hide_pass():
            eye_image.configure(file="hide.png")
            password_entry.config(show="*")
            self.eye_btn = tk.Button(root, image=eye_image ,bd=0, bg="white", command=show_pass , activebackground="white")
            self.eye_btn.grid(row = 3 , column =2 , padx=5 , sticky="e")

        # Clear fuction   [ ↓↓ ]

        def clear():

            uname_entry.delete(0, "end")
            email_entry.delete(0, "end")
            Gender.set("none")
            phone_entry.delete(0, "end")
            password_entry.delete(0, "end")
            confirmation_entry.delete(0, "end")
            uname_entry.focus()

        # Save fuction   [ ↓↓↓ ]

        def save():
            from login import Log_in

            # Collecting data from the entries

            self.username = uname_entry.get().strip()
            self.email = email_entry.get().strip()
            self.gender = Gender.get()
            self.phone = phone_entry.get().strip()
            self.password = password_entry.get()
            self.pass_conf = confirmation_entry.get()

            # Select query returns the phone number from users table

            validate_phone = "SELECT phone FROM users WHERE phone = %s;"
            db.curs.execute(validate_phone, (self.phone,))
            phone_result = db.curs.fetchone()

            # Select query returns the email from users table

            validate_email = "SELECT email FROM users WHERE email = %s;"
            db.curs.execute(validate_email, (self.email,))
            email_result = db.curs.fetchone()

            # Select query returns the username from users table

            validate_uname = "SELECT username FROM users WHERE username = %s;"
            db.curs.execute(validate_uname, (self.username,))
            uname_result = db.curs.fetchone()

            # Checking that the username isn't empty

            if self.username == "":
                m.showerror("Incomplete data", "Please Enter your username")

            # Checking that the username doesn't contain any special characters, digits or spaces

            elif re.search(r'[\d!"#$%&\'()*+,\-./:;<=>?@\[\\\]^`{|}~\s]', self.username):
                m.showerror("Error!",
                            "Username cannot contain special characters, digits or spaces")

            # Checking that the username is less than 30 characters

            elif len(self.username) > 30:
                m.showerror("Error!", "Username should be less than 30 characters")

            # Checking that the username doesn't exists

            elif uname_result is not None:
                m.showerror("Error!", "Username already exists, Please Enter another username")

            # Checking that the email isn't empty

            elif self.email == "":
                m.showerror("Incomplete data", "Please Enter your email")

            # Checking that the username is less than 30 characters

            elif len(self.email) > 50:
                m.showerror("Error!", "Email should be less than 50 characters")

            # Checking that the email contains "@" sign and a "."

            elif '@' not in self.email or self.email.index('@') + 1 == '.' or '.' not in self.email or ' ' in self.email:
                m.showerror("Error!", "Please Enter a valid email")

            # Checking that the email doesn't exists

            elif email_result is not None:
                m.showerror("Error!", "Email already exists, Please Enter another email")

            # Checking that the gender isn't empty

            elif self.gender == "none":
                m.showerror("Incomplete data", "Please Choose gender type")

            # Checking that the phone number isn't empty

            elif self.phone == "":
                m.showerror("Incomplete data", "Please Enter your phone number")

            # Checking that the phone number is just 11 characters, and start with 010 or 011 or 012 or 015, and that is just a digits

            elif len(self.phone) != 11 or self.phone[0] != '0' or self.phone[1] != '1' or (self.phone[2] > '2' and self.phone[2] != '5') or not self.phone.isdigit():
                m.showerror("Error!", "Please Enter a valid phone number")

            # Checking that the phone number doesn't exists

            elif phone_result is not None:
                m.showerror("Error!", "Phone Number already exists, Please Enter another phone number")

            # Checking that the password isn't empty

            elif self.password == "":
                m.showerror("Incomplete data", "Please Enter your password")

            # Checking that the password is more than 8 characters

            elif len(self.password) < 8:
                m.showerror("Error!", "Password should be 8 or more characters")

            # Checking that the password is less than 25 characters

            elif len(self.password) > 25:
                m.showerror("Error!", "Password should be less than 25 characters")

            # Checking that the password and the password confirmation are equal

            elif self.password != self.pass_conf:
                m.showerror("Error!", "Your passwords should match each other, Please recheck")

            else:
                # Saving user information   [ ↓ ]

                m.showinfo("Success", "Registeration successful, Please login")

                # Inserting user data into the database

                inserting_query = "INSERT INTO users(username, email, phone, gender, password) VALUES(%s, %s, %s, %s, %s);"
                values = [self.username, self.email, self.phone, self.gender, self.password]

                db.curs.execute(inserting_query, values)

                # Saving the changes to users table

                db.conn.commit()

                # Close the signup page and redirect to login page

                root.destroy()
                Log_in()


        # Entries   [ ↓↓↓ ]


        # Username

        uname_label = tk.Label(root, text="Username", **style)
        uname_label.grid(row=1, column=1)

        uname_entry = tk.Entry(root, font="Cairo 10",  bd=0)
        uname_entry.grid(row=1, column=2, pady=7)

        uname_entry.focus()

        # Email

        email_label = tk.Label(root, text="Email Address", **style)
        email_label.grid(row=1, column=5)

        email_entry = tk.Entry(root, font="Cairo 10",  bd=0)
        email_entry.grid(row=1, column=6)

        # Phone

        phone_label = tk.Label(root, text="Phone Number", **style)
        phone_label.grid(row=2, column=5)

        phone_entry = tk.Entry(root, font="Cairo 10",  bd=0)
        phone_entry.grid(row=2, column=6, pady=7)

        # Gender

        gender_label = tk.Label(root, text="Gender", **style)
        gender_label.grid(row=2, column=1)

        Gender = tk.StringVar(root)
        gender_choices = ['Male', 'Female']
        Gender.set("none")

        gender_dropdown = Combobox(
            root, textvariable=Gender, values=gender_choices, state="readonly", font="cairo 8 bold")
        gender_dropdown.grid(row=2, column=2, pady=7)

        # Password

        password_label = tk.Label(root, text="Password", **style)
        password_label.grid(row=3, column=1)

        password_entry = tk.Entry(root, font="Cairo 10", show="*",  bd=0)
        password_entry.grid(row=3, column=2, pady=7)

        # Confirm Password

        confirmation_label = tk.Label(root, text="Confirm Password", **style)
        confirmation_label.grid(row=3, column=5)

        confirmation_entry = tk.Entry(root, font="Cairo 10", show="*",  bd=0)
        confirmation_entry.grid(row=3, column=6, pady=7)

        self.username = ""
        self.email = ""
        self.gender = ""
        self.phone = ""
        self.password = ""
        self.pass_conf = ""


        # Buttons   [ ↓↓ ]


        # Show password button

        eye_image = tk.PhotoImage(file = "hide.png")
        self.eye_btn = tk.Button(root, image=eye_image ,bd=0, bg="white", command=show_pass , activebackground="white")
        self.eye_btn.grid(row = 3 , column =2 , padx=5 , sticky="e")

        # Save button

        save_button = tk.Button(root, text="Save",  **btn_style, command=save, cursor="hand2")
        save_button.grid(row=6, column=2, pady=10)

        # Clear button

        clear_button = tk.Button(root, text="Clear", **btn_style, command=clear, cursor="hand2")
        clear_button.grid(row=6, column=5, pady=10)

        # Back button

        back = tk.PhotoImage(file="back.png")
        back_button = tk.Button(root, image=back , bd=0 , cursor="hand2" , command=back_home)
        back_button.place(x=20, y=20)

        root.mainloop()


if __name__ == "__main__":

    app = Sign_up()
