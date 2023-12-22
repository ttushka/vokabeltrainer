import json
import random
import datetime
import tkinter as tk
from tkinter import filedialog

# Function to load Italian words data from the JSON file
def load_words(file_path):
    try:
        with open(file_path, "r") as file:
            words = json.load(file)
            #print("Loaded data:")
            #print(json.dumps(words, indent=4))  # Print loaded data
        return words
    except FileNotFoundError:
        print(f"File not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON file.")
        return {}
    
def save_words(words, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(words, file, indent=4)
    except Exception as e:
        print(f"Error saving to file: {e}")


# Function to show the next word for review
def show_next_word(words):
    word = random.choice(words)
    details = word["details"]
    details["next_review_time"] = details["next_review_time"].strip()
    if datetime.datetime.strptime(details["next_review_time"], "%Y-%m-%d %H:%M:%S") <= datetime.datetime.now():
        # Show Italian word
        print(f"Italian Word: {details['Italian']}")
        input("Press Enter to reveal English translation...")

        # Show English translation
        print(f"English Translation: {details['English']}")
            
        # Ask for correctness input
        response = input("Was your translation correct? (Type 'c' or 'w'): ").lower()

        # Update review intervals based on correctness
        if response == "c":
            details["Phase"]+= 1
            if details["Phase"] > 6:
                details["Phase"] = 6
            details["next_review_time"] = (datetime.datetime.now() + datetime.timedelta(days=next_review(details["Phase"]))).strftime("%Y-%m-%d %H:%M:%S")
                    
        else:
            # If the response is incorrect, reset the phase to 1
            phase = 1
            details["next_review_time"] = (datetime.datetime.now() + datetime.timedelta(days=next_review(phase))).strftime("%Y-%m-%d %H:%M:%S")
            details["Phase"] = phase

    return words

# Function to calculate the next review time based on the phase
def next_review(phase):
    phase_durations = {
        1: 0,
        2: 1,
        3: 2,
        4: 4,
        5: 7,
        6: 12,
    }
    
    return phase_durations.get(phase, 0)

# Main function to run the memorization app
def memorize_words():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select JSON File", filetypes=[("JSON files", "*.json")])

    italian_words = load_words(file_path)
    while True:
        save_words(show_next_word(italian_words), file_path)

if __name__ == "__main__":
    memorize_words()