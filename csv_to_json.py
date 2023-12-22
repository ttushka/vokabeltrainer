import tkinter as tk
from tkinter import filedialog
import csv
import json

def convert_to_json(csv_filename):
    result = []

    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            index = int(row['index'])
            italian = row['Italian']
            english = row['English']
            next_review_time = row['next_review_time']
            phase = int(row['Phase'])

            entry = {
                "index": index,
                "details": {
                    "Italian": italian,
                    "English": english,
                    "next_review_time": next_review_time,
                    "Phase": phase
                }
            }
            result.append(entry)

    # Choose a file to save the JSON data
    save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if save_path:
        with open(save_path, 'w') as jsonfile:
            json.dump(result, jsonfile, indent=4)
            print(f"JSON data saved to {save_path}")    
            
    return result

def choose_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        json_data = convert_to_json(file_path)
        print(json_data)
        

if __name__ == "__main__":
    choose_file()
