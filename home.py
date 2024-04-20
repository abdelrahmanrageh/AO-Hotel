import tkinter as tk
from tkinter import ttk


class Home:

    def __init__(self):

        # ------------------Header------------------

        root = tk.Tk()
        root.title("AO Hotel")
        root.iconbitmap("ao.ico")
        root.minsize(1000, 600)
        root.rowconfigure(0, weight=2)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)
        root.rowconfigure(5, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(5, weight=1)

        # Styling

        style = {"fg": "#ef7150", "bg": "#efefef"}

        # Button styling

        btn_style = {"font": "Cairo  10 bold", "fg": "#b4403d", "width": 10, "height": 1}

        # Background image

        bg = tk.PhotoImage(file="bg.png")
        bg_label = tk.Label(root, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Logo image

        logo = tk.PhotoImage(file="ao.png")
        logo_label = tk.Label(root, image=logo)
        logo_label.grid(row=0, column=1, columnspan=4, pady=20)

        # ------------------Body------------------

        # Login function   [ ↓ ]

        def login():
            from login import Log_in

            # Close the home page and redirect to login page

            root.destroy()
            Log_in()

        # Sign up function   [ ↓ ]

        def signup():
            from signup import Sign_up                  

            # Close the home page and redirect to signup page

            root.destroy()
            Sign_up()

        # Welcome label

        tk.Label(root, text="Welcom to AO hotel", **style, font=("Cairo", 25)).grid(row=1, column=1, columnspan=3, pady=5)

        # Signup label

        tk.Label(root, text="Or", **style, font=("Cairo", 12)).grid(row=3, column=2)


        # Buttons   [ ↓ ]


        # Login button

        login_btn = tk.Button(root, text="Login", **btn_style, command=login, cursor="hand2")
        login_btn.grid(row=3, column=1, padx=7)

        # Signup button

        signup_btn = tk.Button(root, text="Sign up", **btn_style, command=signup, cursor="hand2")
        signup_btn.grid(row=3, column=3, padx=7)

        root.mainloop()


if __name__ == "__main__":
    app = Home()
