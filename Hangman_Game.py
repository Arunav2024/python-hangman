import tkinter as tk
from tkinter import messagebox
import random

# --- Game Data with Clues ---
word_lists = {
    "Easy": [
        ("apple", "A red or green fruit that keeps the doctor away."),
        ("banana", "A long yellow fruit loved by monkeys."),
        ("grape", "A small, round, purple or green fruit used to make wine."),
        ("orange", "A citrus fruit that shares its name with a color.")
    ],
    "Medium": [
        ("python", "A large snake, or a popular programming language."),
        ("puzzle", "A game or problem designed to test your ingenuity."),
        ("guitar", "A string instrument typically played with a pick."),
        ("castle", "A large fortified building from the medieval period.")
    ],
    "Hard": [
        ("symphony", "An elaborate musical composition for a full orchestra."),
        ("labyrinth", "A complicated irregular network of passages or paths."),
        ("astronomy", "The branch of science that deals with celestial objects."),
        ("paradox", "A seemingly absurd or self-contradictory statement.")
    ]
}

# --- Theme Colors ---
BG_COLOR = "#F0F4F8"       # Soft light blue-grey
TEXT_COLOR = "#2D3748"     # Dark slate for readable text
ACCENT_BLUE = "#4299E1"
ACCENT_GREEN = "#48BB78"
ACCENT_RED = "#F56565"
ACCENT_YELLOW = "#ECC94B"

# --- ASCII Art ---
def display_hangman(attempts):
    stages = [
"""
  -------
  |/    |
 |     
 |     
   |       
 |     
       ---
""",
"""
  -------
  |/    |
  |     O
  |     
  |     
  |     
       ---
""",
"""
  -------
  |/    |
  |     O
  |     |
  |     
  |     
       ---
""",
"""
  -------
  |/    |
  |     O
  |    /|
  |     
  |     
      ---
""",
"""
  -------
  |/    |
  |     O
  |    /|\\
  |     
  |     
       ---
""",
"""
  -------
  |/    |
  |     O
  |    /|\\
  |    /
  |     
      ---
""",
"""
  -------
  |/    |
  |     O
  |    /|\\
  |    / \\
  |     
       ---
"""
    ]
    return stages[attempts]

def display_person_free():
    return """
  -------
  |/    |
  |     |
  |    \\O/
 |     |
  |    / \\
       ---
"""
# --- Game Logic Helpers ---
def display_word(word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

def check_win(word, guessed_letters):
    return all(letter in guessed_letters for letter in word)

# --- UI Helper to keep everything in 1 window ---
def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.unbind('<Return>') # Remove enter key binding between screens
    root.config(bg=BG_COLOR)

# --- Screens ---
def rules_screen(root):
    clear_window(root)
    root.title("Hangman Game - How to Play")

    title = tk.Label(root, text="How to Play", font=("Helvetica", 24, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
    title.pack(pady=(40, 20))

    rules_text = (
        "1. Select a difficulty on the main menu and click Start.\n\n"
        "2. You will be given a clue/question to guess the hidden word.\n\n"
        "3. Type a single letter and click 'Guess' (or press Enter).\n\n"
        "4. If you guess wrong, a part of the hangman is drawn.\n\n"
        "5. You have 6 attempts to guess the word before he hangs!\n\n"
        "6. Need help? Use the 'Hint' button to reveal a correct letter,\n"
        "   but be careful—it costs you 1 attempt!"
    )
    
    rules_label = tk.Label(root, text=rules_text, font=("Helvetica", 14), bg=BG_COLOR, fg=TEXT_COLOR, justify="left")
    rules_label.pack(pady=10, padx=40)

    back_btn = tk.Button(root, text="Back to Menu", command=lambda: main_menu(root), font=("Helvetica", 14, "bold"), bg=ACCENT_BLUE, fg="white", padx=20, pady=5, relief="flat")
    back_btn.pack(pady=40)


def main_menu(root):
    clear_window(root)
    root.title("Hangman Game - Main Menu")

    title_label = tk.Label(root, text="HANGMAN", font=("Helvetica", 36, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
    title_label.pack(pady=(50, 10))

    subtitle_label = tk.Label(root, text="Save him before it's too late!", font=("Helvetica", 14, "italic"), bg=BG_COLOR, fg="#718096")
    subtitle_label.pack(pady=(0, 30))

    difficulty_frame = tk.Frame(root, bg=BG_COLOR)
    difficulty_frame.pack(pady=10)

    diff_label = tk.Label(difficulty_frame, text="Select Difficulty:", font=("Helvetica", 14, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
    diff_label.pack(side="top", pady=10)

    difficulty_var = tk.StringVar(value="Medium") # Default value
    
    # Pack radio buttons horizontally
    radio_frame = tk.Frame(difficulty_frame, bg=BG_COLOR)
    radio_frame.pack()
    for level in word_lists.keys():
        tk.Radiobutton(radio_frame, text=level, variable=difficulty_var, value=level, font=("Helvetica", 12), bg=BG_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR, cursor="hand2").pack(side="left", padx=15)

    # Buttons Frame
    btn_frame = tk.Frame(root, bg=BG_COLOR)
    btn_frame.pack(pady=40)

    start_btn = tk.Button(btn_frame, text="Start Game", command=lambda: hangman_game(root, difficulty_var.get()), font=("Helvetica", 14, "bold"), bg=ACCENT_GREEN, fg="white", width=15, pady=8, relief="flat", cursor="hand2")
    start_btn.pack(pady=10)

    rules_btn = tk.Button(btn_frame, text="How to Play", command=lambda: rules_screen(root), font=("Helvetica", 14, "bold"), bg=ACCENT_BLUE, fg="white", width=15, pady=8, relief="flat", cursor="hand2")
    rules_btn.pack(pady=10)

    quit_btn = tk.Button(btn_frame, text="Quit", command=root.destroy, font=("Helvetica", 14, "bold"), bg=ACCENT_RED, fg="white", width=15, pady=8, relief="flat", cursor="hand2")
    quit_btn.pack(pady=10)


def hangman_game(root, difficulty_level):
    clear_window(root)
    root.title(f"Hangman Game - {difficulty_level} Mode")

    # Game Variables (word and clue from tuple)
    word, clue = random.choice(word_lists[difficulty_level])
    guessed_letters = []
    attempts = 6

    # Clue Label
    clue_label = tk.Label(root, text=f"Clue: {clue}", font=("Helvetica", 14, "italic"), bg=BG_COLOR, fg=TEXT_COLOR, wraplength=450, justify="center")
    clue_label.pack(pady=(30, 10))

    # UI Elements
    guessed_word_label = tk.Label(root, text=display_word(word, guessed_letters), font=("Courier", 28, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
    guessed_word_label.pack(pady=20)

    hangman_image = tk.Label(root, text=display_hangman(0), font=("Courier", 16), bg=BG_COLOR, fg=TEXT_COLOR)
    hangman_image.pack()

    attempts_label = tk.Label(root, text=f"Attempts left: {attempts}", font=("Helvetica", 14, "bold"), bg=BG_COLOR, fg=ACCENT_RED)
    attempts_label.pack(pady=10)

    input_frame = tk.Frame(root, bg=BG_COLOR)
    input_frame.pack(pady=20)

    guess_entry = tk.Entry(input_frame, font=("Helvetica", 16), width=5, justify="center", relief="solid", bd=1)
    guess_entry.pack(side="left", padx=10, ipady=5)
    guess_entry.focus()

    def guess_letter(event=None):
        nonlocal attempts
        guess = guess_entry.get().lower()
        guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a single letter.")
            return

        if guess in guessed_letters:
            messagebox.showinfo("Already Guessed", f"You already guessed '{guess.upper()}'. Try another letter.")
            return

        guessed_letters.append(guess)

        if guess not in word:
            attempts -= 1
            hangman_image.config(text=display_hangman(6 - attempts))
            if attempts == 0:
                lose_display(root, word)
                return
        else:
            if check_win(word, guessed_letters):
                win_display(root, word)
                return

        guessed_word_label.config(text=display_word(word, guessed_letters))
        attempts_label.config(text=f"Attempts left: {attempts}")

    def use_hint():
        nonlocal attempts
        if attempts <= 1:
            messagebox.showwarning("Warning", "Not enough attempts left to use a hint!")
            return
            
        unguessed_letters = [char for char in word if char not in guessed_letters]
        if unguessed_letters:
            hint_letter = random.choice(unguessed_letters)
            guessed_letters.append(hint_letter)
            attempts -= 1
            
            hangman_image.config(text=display_hangman(6 - attempts))
            guessed_word_label.config(text=display_word(word, guessed_letters))
            attempts_label.config(text=f"Attempts left: {attempts}")
            
            if check_win(word, guessed_letters):
                win_display(root, word)
                return

    guess_button = tk.Button(input_frame, text="Guess", command=guess_letter, font=("Helvetica", 12, "bold"), bg=ACCENT_BLUE, fg="white", width=8, relief="flat", cursor="hand2")
    guess_button.pack(side="left", padx=5, ipady=3)

    hint_button = tk.Button(input_frame, text="Hint (-1)", command=use_hint, font=("Helvetica", 12, "bold"), bg=ACCENT_YELLOW, fg=TEXT_COLOR, width=8, relief="flat", cursor="hand2")
    hint_button.pack(side="left", padx=5, ipady=3)

    root.bind('<Return>', guess_letter)


def win_display(root, word):
    clear_window(root)
    root.title("You Won!")
    
    congrats_label = tk.Label(root, text="Congratulations!\nYou freed Hangman!", font=("Helvetica", 24, "bold"), bg=BG_COLOR, fg=ACCENT_GREEN, justify="center")
    congrats_label.pack(pady=(50, 10))

    word_label = tk.Label(root, text=f"The word was: {word.upper()}", font=("Helvetica", 16), bg=BG_COLOR, fg=TEXT_COLOR)
    word_label.pack(pady=10)

    free_hangman_label = tk.Label(root, text=display_person_free(), font=("Courier", 16), bg=BG_COLOR, fg=TEXT_COLOR)
    free_hangman_label.pack(pady=20)

    btn_frame = tk.Frame(root, bg=BG_COLOR)
    btn_frame.pack(pady=30)

    retry_btn = tk.Button(btn_frame, text="Play Again", command=lambda: main_menu(root), font=("Helvetica", 14, "bold"), bg=ACCENT_BLUE, fg="white", width=12, pady=8, relief="flat", cursor="hand2")
    retry_btn.pack(side="left", padx=10)

    quit_btn = tk.Button(btn_frame, text="Quit", command=root.destroy, font=("Helvetica", 14, "bold"), bg=ACCENT_RED, fg="white", width=12, pady=8, relief="flat", cursor="hand2")
    quit_btn.pack(side="left", padx=10)


def lose_display(root, word):
    clear_window(root)
    root.title("Game Over!")

    lose_label = tk.Label(root, text="Game Over!\nHangman got hanged.", font=("Helvetica", 24, "bold"), bg=BG_COLOR, fg=ACCENT_RED, justify="center")
    lose_label.pack(pady=(40, 10))

    word_label = tk.Label(root, text=f"The word was: {word.upper()}", font=("Helvetica", 16), bg=BG_COLOR, fg=TEXT_COLOR)
    word_label.pack(pady=10)

    hangman_label = tk.Label(root, text=display_hangman(6), font=("Courier", 16), bg=BG_COLOR, fg=TEXT_COLOR)
    hangman_label.pack(pady=10)

    btn_frame = tk.Frame(root, bg=BG_COLOR)
    btn_frame.pack(pady=30)

    retry_btn = tk.Button(btn_frame, text="Play Again", command=lambda: main_menu(root), font=("Helvetica", 14, "bold"), bg=ACCENT_BLUE, fg="white", width=12, pady=8, relief="flat", cursor="hand2")
    retry_btn.pack(side="left", padx=10)

    quit_btn = tk.Button(btn_frame, text="Quit", command=root.destroy, font=("Helvetica", 14, "bold"), bg=ACCENT_RED, fg="white", width=12, pady=8, relief="flat", cursor="hand2")
    quit_btn.pack(side="left", padx=10)

# --- Main App Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x750") # Set a slightly wider and taller fixed window size
    root.resizable(False, False) # Prevent resizing to keep layout perfect
    main_menu(root)
    root.mainloop()