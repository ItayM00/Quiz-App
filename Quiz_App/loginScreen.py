"""
loginScreen.py
----------------------
This module defines the LoginApp class, which provides
a login interface for the Quiz Game.

Users can enter their credentials to log in or navigate
to the signup screen.

"""

import customtkinter as ctk
import json
from homeScreen import HomeScreen


class LoginApp(ctk.CTk):
    """
        LoginApp class provides a GUI login screen.

        Users enter their credentials, which are validated against a JSON file.
        If successful, they are redirected to the home screen.
    """

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Login Screen")
        self.geometry("400x500")
        self.resizable(False, False)

        self.init_GUI()


    def init_GUI(self):
        """Initializes and arranges GUI components."""

        # Create main frame using pack
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create title label using pack
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Welcome Back",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(40, 20))

        # Create subtitle using pack
        self.subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Please enter your credentials to login",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle.pack(pady=(0, 30))

        # Create form frame using grid layout
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=30)

        # Username label and entry using grid
        self.username_label = ctk.CTkLabel(self.form_frame, text="Username:")
        self.username_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.username_entry = ctk.CTkEntry(self.form_frame, width=250, placeholder_text="Enter your username")
        self.username_entry.grid(row=1, column=0, sticky="we", pady=(0, 15))

        # Password label and entry using grid
        self.password_label = ctk.CTkLabel(self.form_frame, text="Password:")
        self.password_label.grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.password_entry = ctk.CTkEntry(self.form_frame, width=250, placeholder_text="Enter your password", show="•")
        self.password_entry.grid(row=3, column=0, sticky="we", pady=(0, 5))

        # Login button using pack
        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="Login",
            width=200,
            height=40,
            command=self.login
        )
        self.login_button.pack(pady=30)

        # Register link using pack
        self.register_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.register_frame.pack(pady=(5, 0))

        self.no_account_label = ctk.CTkLabel(
            self.register_frame,
            text="Don't have an account?",
            font=ctk.CTkFont(size=12)
        )
        self.no_account_label.pack(side="left", padx=(0, 5))

        self.register_link = ctk.CTkLabel(
            self.register_frame,
            text="Sign Up",
            font=ctk.CTkFont(size=12, underline=True),
            text_color="#0000EE"  # Blue colors for light/dark mode
        )
        self.register_link.pack(side="left")
        self.register_link.bind("<Button-1>", self.register_click)


    def login(self):
        """Validates user credentials and logs in the user."""

        username = self.username_entry.get()
        password = self.password_entry.get()

        users = self.read_json()

        if not username or not password:
            self.show_message("Please enter both username and password")
        else:
            user = self.search_by_username(users, username, password)
            if user == -1:
                print("error! user not found...")
            else:
                print(user)
                self.quit()
                self.destroy()
                home_screen = HomeScreen(user)
                home_screen.mainloop()

    def register_click(self, event):
        """Handles the transition to the registration screen."""

        from signUpScreen import SignupApp

        self.destroy()
        app = SignupApp()
        app.mainloop()
        self.show_message("Registration functionality")

    def show_message(self, message):
        # Display message (in a real app, you might use a proper message box)
        print(message)

    def read_json(self):
        """
        Reads the user database from a JSON file.

        Returns:
            list: List of user dictionaries or None if the file is not found.
        """

        try:
            with open("users.json", "r") as file:
                json_data = json.load(file)
            return json_data.get("data", [])
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            self.show_message("Error reading user data!")
            return None

    def search_by_username(self, usersList, username, password):
        for user in usersList:
            if user["username"] == username and user["password"] == password:
                return user

        return -1


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()

