"""
1.  CREATE API KEY AT: https://opentdb.com/
2.  UNDERSTAND THE JSON FILE AND IT'S CONTENT
3.  UNDERSTAND THE BACKEND AND TEST ON CONSOLE
4.  START MAKING THE GUI

JSON FILE CONTENT
{
    'response_code': 0,
    'results':
            [
                {
                'type': 'multiple',
                'difficulty': 'easy',
                'category': 'General Knowledge',
                'question': 'Who is the author of Jurassic Park?',
                'correct_answer': 'Michael Crichton',
                'incorrect_answers': ['Peter Benchley', 'Chuck Paluhniuk', 'Irvine Welsh']
                }
            ]
}

"""

from loginScreen import LoginApp

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
