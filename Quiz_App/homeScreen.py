"""
homeScreen.py
----------------------
This module defines the HomeScreen class for a Quiz Game.
It allows users to select a quiz category and difficulty, then fetches
questions from the Open Trivia Database API.

"""

import requests
from gameScreen import *
from leaderboard import LeaderboardScreen


categories = [
    "General Knowledge", "Entertainment: Books", "Entertainment: Film",
    "Entertainment: Music", "Entertainment: Musicals & Theatres", "Entertainment: Television",
    "Entertainment: Video Games", "Entertainment: Board Games", "Science & Nature",
    "Science: Computers", "Science: Mathematics", "Mythology", "Sports", "Geography",
    "History", "Politics", "Art", "Celebrities", "Animals", "Vehicles",
    "Entertainment: Comics", "Science: Gadgets", "Entertainment: Japanese Anime & Manga",
    "Entertainment: Cartoon & Animations"
]

class HomeScreen(ctk.CTk):
    def __init__(self, connected_user):
        super().__init__()

        self.title("Quiz Game")
        self.geometry("400x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.resizable(False, False)

        self.init_gui()

        self.curUser = connected_user


    def init_gui(self):
        # Logo Frame
        self.logo_frame = ctk.CTkFrame(self)
        self.logo_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.logo_frame.grid_columnconfigure(0, weight=1)
        self.logo_frame.grid_rowconfigure((0,1,2), weight=1)

        self.leaderBoardBt = ctk.CTkButton(self.logo_frame, text="LeaderBoard", font=("Arial", 15, "bold"), command=self.open_leaderboard)
        self.leaderBoardBt.grid(row=0, column=0, sticky="w")

        self.logo_label = ctk.CTkLabel(self.logo_frame, text="Quiz Game", font=("Arial", 40, "bold"))
        self.logo_label.grid(row=1, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

        # Bottom Frame
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=2, column=0, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Category Dropdown
        self.category_option = ctk.CTkComboBox(
            self.bottom_frame, values=categories, font=("Arial", 16), state="readonly"
        )
        self.category_option.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.category_option.set("Pick a category:")

        # Difficulty Dropdown
        self.difficulty_option = ctk.CTkComboBox(
            self.bottom_frame, values=["Easy", "Medium", "Hard"], font=("Arial", 16), state="readonly"
        )
        self.difficulty_option.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.difficulty_option.set("Pick a difficulty:")

        # Start Button
        self.start_button = ctk.CTkButton(
            self.bottom_frame, text="Start Quiz", font=("Arial", 20), height=50, command=self.start_game
        )
        self.start_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Status Label
        self.status_label = ctk.CTkLabel(self.bottom_frame, text="", font=("Arial", 20), text_color="red")
        self.status_label.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def open_leaderboard(self):
        self.destroy()
        leaderboard = LeaderboardScreen(self.curUser)
        leaderboard.mainloop()

    def start_game(self):
        difficulty = self.difficulty_option.get().lower()
        category = self.category_option.get()

        if difficulty == "Pick a difficulty:" or category == "Pick a category:":
            self.status_label.configure(text="please pick a category and difficulty !")
        else:
            print("making api request...")
            questions_lst = self.load_questions(category, difficulty)

            if len(questions_lst) < 1:
                self.status_label.configure(text="Error in the process of making the request!\n please try again later...")
            else:
                self.quit()
                self.destroy()
                game = GameScreen(questions_lst, self.curUser)
                game.mainloop()

    def load_questions(self, category, difficulty) -> list:
        category_id = self.convert_category(category)
        amount = 10
        q_type = "multiple"
        base_url = f"https://opentdb.com/api.php?amount={amount}&category={category_id}&difficulty={difficulty}&type={q_type}"

        try:
            response = requests.get(base_url, timeout=5)
            data = response.json()

            if "response_code" in data:
                code = data["response_code"]
                if code == 1:
                    raise ValueError("No Results: No questions found for the given parameters.")
                elif code == 2:
                    raise ValueError("Invalid Parameter: Check your query parameters.")
                elif code == 3:
                    raise ValueError("Token Not Found: Your session token is invalid.")
                elif code == 4:
                    raise ValueError("Token Empty: Your session token has expired, reset it.")

            return data["results"]  # Return questions if everything is fine

        except requests.exceptions.ConnectionError:
            print("Error: Unable to connect to the API. Check your internet connection.")
        except requests.exceptions.Timeout:
            print("Error: The request timed out. Try again later.")
        except requests.exceptions.RequestException as e:
            print(f"HTTP Error: {e}")
        except ValueError as e:
            print(f"API Error: {e}")
        except KeyError:
            print("Error: Unexpected response format from the API.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def convert_category(self, category):
        return categories.index(category) + 9


if __name__ == "__main__":
    app = HomeScreen(None)
    app.mainloop()