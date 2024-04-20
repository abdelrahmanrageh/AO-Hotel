import tkinter as tk
from tkinter import messagebox as m
from tkinter.ttk import *
import db


class Log_in:

    def __init__(self):

        # ------------------Header------------------

        root = tk.Tk()
        root.title("Ao Login")
        root.iconbitmap("ao.ico")
        root.minsize(1000, 600)
        root.rowconfigure(0, weight=2)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(6, weight=8)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(3, weight=1)

        # Styling

        style = {"fg": "#ef7150", "bg": "#efefef", "font": "Cairo 11 bold"}

        # Background image

        bg = tk.PhotoImage(file="bg.png")
        bg_label = tk.Label(root, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title

        title = tk.Label(root, font="cairo 30 bold", bg="#efefef",
                         fg="#b4403d", text="AO Hotel Login")
        title.grid(row=0, column=1, columnspan=2, pady=50)

        # ------------------Body------------------

        # Reservation fuction   [ ↓ ]

        def reservation():
            from reservation import Reservation

            # Close the login page and redirect to reservation page

            root.destroy()
            Reservation()

        # Admin panel fuction   [ ↓ ]

        def admin():
            from admin import Admin

            # Close the login page and redirect to admin panel

            root.destroy()
            Admin()

        # New password fuction   [ ↓ ]

        def new_pass():
            from new_password import New_password

            # Opens the reset password window

            New_password()

        # Show password fuction   [ ↓↓ ]

        def show_pass():
            eye_image.configure(file="view.png")
            password_entry.config(show="")
            self.eye_btn = tk.Button(root, image=eye_image, bd=0, bg="white", command=hide_pass,
                                  activebackground="white").grid(row=3, column=2, padx=5, sticky="e")

        # Hide password fuction   [ ↓↓ ]

        def hide_pass():
            eye_image.configure(file="hide.png")
            password_entry.config(show="*")
            self.eye_btn = tk.Button(root, image=eye_image, bd=0, bg="white", command=show_pass,
                                  activebackground="white").grid(row=3, column=2, padx=5, sticky="e")
            
        # Back button function   [ ↓ ]

        def back_home():
            from home import Home
            # Close the login page and go back to home page

            root.destroy()
            Home()

        # Login fuction   [ ↓↓↓ ]

        def Login():

            # Collecting data from the entries

            uname = username_entry.get().strip()
            password = password_entry.get()

            # Select query returns the username & passaword from database

            login_query = "SELECT username, password FROM users WHERE username = %s and password = %s;"
            values = (uname, password)

            db.curs.execute(login_query, values)
            login_result = db.curs.fetchone()

            # Checking if the username or password are empty

            if uname == "" or password == "":
                m.showerror("Error!", "All fields are required")

            # Checking if the username & password are admin, then redirect to admin panel

            elif uname.lower() == "admin" and password.lower() == "admin":
                admin()

            # Checking if the query result is not None then the user exists, then redirect to reservation

            elif login_result is not None:
                m.showinfo("Success", "Login Successful!")
                reservation()

            # Checking if the username or password aren't correct

            else:
                m.showerror("Error!", "Invalid username or password")
                username_entry.delete(0, "end")
                password_entry.delete(0, "end")
                username_entry.focus()


        # Entries   [ ↓↓ ]


        # Username

        username_label = tk.Label(root, **style, text="Username")
        username_label.grid(row=2, column=1, ipadx=2)

        username_entry = tk.Entry(root, font="Cairo 10", bd=0)
        username_entry.grid(row=2, column=2, sticky="we")
        username_entry.focus()

        # Password

        password_label = tk.Label(root, text="Password", **style)
        password_label.grid(row=3, column=1, ipadx=2)

        password_entry = tk.Entry(root, show='*', font="Cairo 10", bd=0)
        password_entry.grid(row=3, column=2, pady=10, sticky="we")


        # Buttons   [ ↓↓↓ ]


        # Show password button

        eye_image = tk.PhotoImage(file="hide.png")
        self.eye_btn = tk.Button(root, image=eye_image, bd=0, bg="white", command=show_pass,
                              activebackground="white").grid(row=3, column=2, padx=5, sticky="e")

        # Forget password button

        forget_btn = tk.Button(root, bd=0, text="forget password?",
                            fg="#b4403d", cursor="hand2", command=new_pass)
        forget_btn.grid(row=4, column=2, sticky="e")

        # Login button

        login = tk.Button(root, text="Log In", fg="#b4403d",
                          font="Cairo 11 bold", height=1, command=Login, cursor="hand2")
        login.grid(row=5, column=1, columnspan=2, pady=20, sticky="we")

        # Back button

        back = tk.PhotoImage(file="back.png")
        back_button = tk.Button(root, image=back , bd=0 , cursor="hand2" , command=back_home)
        back_button.place(x=20, y=20)

        root.mainloop()


if __name__ == "__main__":
    login_window = Log_in()
