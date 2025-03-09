"""
leaderboard.py
----------------------
This module defines the LeaderboardScreen class for displaying
the top players ranked by points in a Quiz Game.

"""

import customtkinter as ctk
import json


class LeaderboardScreen(ctk.CTk):
    """
    LeaderboardScreen class displays a ranked list of users based on their points.

    Attributes:
        current_user (dict): The currently logged-in user (optional).
    """

    def __init__(self, current_user=None):
        """
        Initializes the leaderboard window and loads user rankings.

        Args:
            current_user (dict, optional): The current user's details. Defaults to None.
        """

        super().__init__()

        self.current_user = current_user

        # Configure window
        self.title("Leaderboard")
        self.geometry("400x500")
        self.resizable(False, False)

        self.init_GUI()
        self.load_leaderboard_data()

    def init_GUI(self):
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Add back button
        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="←",
            width=30,
            height=30,
            corner_radius=15,
            command=self.go_back
        )
        self.back_button.place(x=0, y=0)

        # Create title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Leaderboard",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Create subtitle
        self.subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Top players by points",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle.pack(pady=(0, 20))

        # Create headers frame
        self.headers_frame = ctk.CTkFrame(self.main_frame)
        self.headers_frame.pack(fill="x", padx=10, pady=(0, 5))

        # Create headers
        self.rank_header = ctk.CTkLabel(
            self.headers_frame,
            text="Rank",
            font=ctk.CTkFont(weight="bold"),
            width=50
        )
        self.rank_header.pack(side="left", padx=(10, 0))

        self.name_header = ctk.CTkLabel(
            self.headers_frame,
            text="Username",
            font=ctk.CTkFont(weight="bold")
        )
        self.name_header.pack(side="left", padx=(20, 0), expand=True, anchor="w")

        self.points_header = ctk.CTkLabel(
            self.headers_frame,
            text="Points",
            font=ctk.CTkFont(weight="bold"),
            width=80
        )
        self.points_header.pack(side="right", padx=(0, 10))

        # Create a container frame for the scrollable frame
        self.container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.container,
            width=340,
            height=300,
            fg_color="transparent"
        )
        self.scrollable_frame.pack(fill="both", expand=True)

        # Create refresh button at the bottom
        self.refresh_button = ctk.CTkButton(
            self.main_frame,
            text="Refresh",
            width=150,
            command=self.load_leaderboard_data
        )
        self.refresh_button.pack(pady=(5, 10))

    def load_leaderboard_data(self):
        """Loads and displays the leaderboard rankings from a JSON file."""

        # Clear existing items in the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            with open("users.json", "r") as file:
                json_data = json.load(file)

            # Sort users by points (highest first)
            sorted_users = sorted(json_data["data"], key=lambda x: x["points"], reverse=True)

            # Add each user to the leaderboard
            for i, user in enumerate(sorted_users):
                # Create a frame for each row
                row_frame = ctk.CTkFrame(self.scrollable_frame)
                row_frame.pack(fill="x", pady=2)

                # Highlight current user's row
                if self.current_user and user["username"] == self.current_user["username"]:
                    row_frame.configure(fg_color=("lightblue", "#2a5278"))

                # Rank
                rank_label = ctk.CTkLabel(
                    row_frame,
                    text=f"#{i + 1}",
                    width=50
                )
                rank_label.pack(side="left", padx=(10, 0))

                # Username
                username_label = ctk.CTkLabel(
                    row_frame,
                    text=user["username"],
                    anchor="w"
                )
                username_label.pack(side="left", padx=(20, 0), expand=True, fill="x")

                # Points
                points_label = ctk.CTkLabel(
                    row_frame,
                    text=str(user["points"]),
                    width=80
                )
                points_label.pack(side="right", padx=(0, 10))

        except FileNotFoundError:
            error_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Error: Users database not found!",
                text_color="red"
            )
            error_label.pack(pady=20)

        except Exception as e:
            error_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Error loading leaderboard: {str(e)}",
                text_color="red"
            )
            error_label.pack(pady=20)

    def go_back(self):
        """Returns to the home screen."""

        from homeScreen import HomeScreen
        self.destroy()
        app = HomeScreen(self.current_user)
        app.mainloop()


if __name__ == "__main__":
    # For testing purposes
    app = LeaderboardScreen()
    app.mainloop()
