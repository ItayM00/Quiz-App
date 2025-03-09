"""
signUpScreen.py
----------------------
This module defines the SignupApp class, which provides
a user registration interface for the Quiz Game.

Users can create an account, and their credentials
are stored in a JSON file.

"""

from tkinter import messagebox
import customtkinter as ctk
import json
from homeScreen import HomeScreen
from loginScreen import LoginApp


class SignupApp(ctk.CTk):
    """
    SignupApp class provides a GUI for user registration.

    Users can enter their details to create an account, which is stored in a JSON file.
    """

    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        # Configure window
        self.title("Sign Up")
        self.geometry("400x550")

        self.init_GUI()

    def init_GUI(self):
        """Initializes and arranges GUI components."""

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Create an Account",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(40, 20))

        # Create subtitle
        self.subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Please fill in your details below",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle.pack(pady=(0, 30))

        # Create form frame
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=30)

        # Username label and entry
        self.username_label = ctk.CTkLabel(self.form_frame, text="Username:")
        self.username_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.username_entry = ctk.CTkEntry(self.form_frame, width=250, placeholder_text="Choose a username")
        self.username_entry.grid(row=1, column=0, sticky="we", pady=(0, 15))

        # Password label and entry
        self.password_label = ctk.CTkLabel(self.form_frame, text="Password:")
        self.password_label.grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.password_entry = ctk.CTkEntry(self.form_frame, width=250, placeholder_text="Create a password", show="•")
        self.password_entry.grid(row=3, column=0, sticky="we", pady=(0, 15))

        # Confirm password label and entry
        self.confirm_label = ctk.CTkLabel(self.form_frame, text="Confirm Password:")
        self.confirm_label.grid(row=4, column=0, sticky="w", pady=(0, 5))

        self.confirm_entry = ctk.CTkEntry(self.form_frame, width=250, placeholder_text="Confirm your password",
                                          show="•")
        self.confirm_entry.grid(row=5, column=0, sticky="we", pady=(0, 15))

        # Sign up button
        self.signup_button = ctk.CTkButton(
            self.main_frame,
            text="Sign Up",
            width=200,
            height=40,
            command=self.signup
        )
        self.signup_button.pack(pady=20)

        # Login link
        self.login_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.login_frame.pack(pady=(5, 0))

        self.have_account_label = ctk.CTkLabel(
            self.login_frame,
            text="Already have an account?",
            font=ctk.CTkFont(size=12)
        )
        self.have_account_label.pack(side="left", padx=(0, 5))

        self.login_link = ctk.CTkLabel(
            self.login_frame,
            text="Login",
            font=ctk.CTkFont(size=12, underline=True),
            text_color="#0000EE"
        )
        self.login_link.pack(side="left")
        self.login_link.bind("<Button-1>", self.back_to_login)

    def signup(self):
        """Validates input fields and registers a new user."""

        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        # Validate inputs
        if not username or not password or not confirm:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            with open("users.json", "r") as file:
                json_data = json.load(file)

            for user in json_data["data"]:
                if user["username"] == username:
                    messagebox.showerror("Error", "Username already exists")
                    return

            new_user = {"username": username, "password": password, "points": 0}
            json_data["data"].append(new_user)

            with open("users.json", "w") as file:
                json.dump(json_data, file, indent=4)

            messagebox.showinfo("Success", f"Account created successfully for {username}!")
            self.destroy()
            home = HomeScreen(new_user)
            home.mainloop()

        except FileNotFoundError:
            print("FILE NOT FOUND!! CHECK DATABASE...")

    def back_to_login(self, event=None):
        """Handles transition back to the login screen."""

        self.destroy()
        app = LoginApp()
        app.mainloop()


if __name__ == "__main__":
    app = SignupApp()
    app.mainloop()