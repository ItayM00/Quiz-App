"""
gameScreen.py
----------------------
This module defines the GameScreen class for a Flashcard App using the CustomTkinter library.
It manages the quiz interface, handles question selection, user interaction, and scoring.

"""

import customtkinter as ctk
import html
import random
from tkinter import messagebox
import json


class GameScreen(ctk.CTk):
    """
    GameScreen class represents the flashcard quiz interface.

    Attributes:
        question_lst (list): A list of quiz questions.
        curUser (dict): The current user details.
    """

    def __init__(self, question_lst, curUser):
        """
        Initializes the game screen with questions and user data.

        Args:
            question_lst (list): List of questions from the database.
            curUser (dict): Dictionary containing user details.
        """
        super().__init__()

        self.title("Flashcard App")
        self.geometry("700x500")

        self.question_lst = question_lst
        self.cur_question = ""
        self.correct_answer = ""
        self.wrong_answers = []
        self.q_index = 0
        self.curUser = curUser

        self.init_GUI()
        self.correct_index = self.update_GUI()

    def init_GUI(self):
        """Initializes the graphical user interface components."""
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Menu bar
        self.menu_bar = ctk.CTkFrame(self.main_frame)
        self.menu_bar.pack(fill="x", padx=10, pady=10)

        # Navigation buttons
        self.back_button = ctk.CTkButton(self.menu_bar, text="Back", command=self.go_back)
        self.back_button.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(self.menu_bar, text="Next Question", command=self.update_GUI)
        self.next_button.pack(side="right", padx=10)

        # Flashcard display
        self.card_frame = ctk.CTkFrame(self.main_frame)
        self.card_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.qa_label = ctk.CTkLabel(self.card_frame, text="", wraplength=500, font=("Arial", 25, "bold"))
        self.qa_label.pack(pady=50, padx=20)

        # Answer buttons
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)
        self.buttons_frame.grid_rowconfigure(1, weight=1)

        self.ans1_button = ctk.CTkButton(self.buttons_frame, text="Answer 1", font=("Arial", 16),
                                         command=lambda: self.check_answer(1))
        self.ans1_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.ans2_button = ctk.CTkButton(self.buttons_frame, text="Answer 2", font=("Arial", 16),
                                         command=lambda: self.check_answer(2))
        self.ans2_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.ans3_button = ctk.CTkButton(self.buttons_frame, text="Answer 3", font=("Arial", 16),
                                         command=lambda: self.check_answer(3))
        self.ans3_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.ans4_button = ctk.CTkButton(self.buttons_frame, text="Answer 4", font=("Arial", 16),
                                         command=lambda: self.check_answer(4))
        self.ans4_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.default_color = self.ans1_button._fg_color

    def update_GUI(self) -> int:
        """
        Updates the UI with the next question and answer choices.

        Returns:
            int: The index of the correct answer button.
        """
        if self.q_index > 9:
            self.qa_label.configure(text="Out of Questions! Please press Back to return to the home screen.")
            self.next_button.configure(state="disabled")
            return -1

        self.cur_question = html.unescape(self.question_lst[self.q_index]['question'])
        self.correct_answer = html.unescape(self.question_lst[self.q_index]['correct_answer'])
        self.wrong_answers = [html.unescape(ans) for ans in self.question_lst[self.q_index]['incorrect_answers']]

        self.qa_label.configure(text=self.cur_question)

        btns = [self.ans1_button, self.ans2_button, self.ans3_button, self.ans4_button]
        anss = self.wrong_answers + [self.correct_answer]
        random.shuffle(anss)
        random.shuffle(btns)

        correct_bt_index = anss.index(self.correct_answer)

        for i, btn in enumerate(btns):
            btn.configure(text=anss[i])

        self.q_index += 1
        self.reset_buttons()
        return correct_bt_index

    def go_back(self):
        """Handles returning to the home screen."""
        from homeScreen import HomeScreen
        if messagebox.askquestion("Quit", "Do you want to quit?") == "yes":
            print("Going back to previous screen")
            self.quit()
            self.destroy()
            home_screen = HomeScreen(self.curUser)
            home_screen.mainloop()

    def check_answer(self, btn_id):
        """
        Checks if the selected answer is correct.

        Args:
            btn_id (int): The button ID of the selected answer.
        """
        btn_map = {1: self.ans1_button, 2: self.ans2_button, 3: self.ans3_button, 4: self.ans4_button}
        ans = btn_map[btn_id].cget("text")

        if ans == self.correct_answer:
            self.paint_Button("green", btn_id)
            self.update_user_score()
        else:
            self.paint_Button("red", btn_id)

    def update_user_score(self):
        """Updates the user's score in the JSON file."""
        try:
            with open("users.json", "r") as file:
                json_data = json.load(file)

            for user in json_data["data"]:
                if user["username"] == self.curUser["username"]:
                    user["points"] += 10
                    break

            with open("users.json", "w") as file:
                json.dump(json_data, file, indent=4)

        except FileNotFoundError:
            print("File Not Found...")

    def paint_Button(self, color, bt_id):
        """Changes the button color after selection."""
        btn_map = {1: self.ans1_button, 2: self.ans2_button, 3: self.ans3_button, 4: self.ans4_button}
        btn_map[bt_id].configure(fg_color=color, state="disabled")

    def reset_buttons(self):
        """Resets the buttons for the next question."""
        for btn in [self.ans1_button, self.ans2_button, self.ans3_button, self.ans4_button]:
            btn.configure(fg_color=self.default_color, state="normal")


if __name__ == "__main__":
    app = GameScreen()
    app.mainloop()
