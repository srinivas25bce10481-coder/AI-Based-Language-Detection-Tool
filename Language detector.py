import argparse
import json
import os
import time
from datetime import datetime
from langdetect import detect, detect_langs, DetectorFactory

# Set seed so results don't change every time I run it
DetectorFactory.seed = 0

# I mapped the most common language codes to their full names here.
# (Added the ones I tested most often)
LANG_NAMES = {
    'EN': 'English', 
    'ES': 'Spanish', 
    'FR': 'French', 
    'DE': 'German', 
    'IT': 'Italian', 
    'JA': 'Japanese',
    'KO': 'Korean', 
    'ZH-CN': 'Chinese', 
    'PT': 'Portuguese', 
    'RU': 'Russian',
    'HI': 'Hindi',
    'AR': 'Arabic'
}

class LanguageDetectorApp:
    def __init__(self, filename="history.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        # Create the history file if it's missing so the program doesn't crash
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def save_to_history(self, user_text, result_lang, conf_score):
        # This saves my previous searches so I can view them in the menu
        try:
            with open(self.filename, 'r+') as file:
                try:
                    logs = json.load(file)
                except:
                    logs = []
                
                # Truncate long text so the JSON file doesn't get huge
                preview = user_text[:35] + "..." if len(user_text) > 35 else user_text
                
                new_data = {
                    "date": datetime.now().strftime("%H:%M:%S"),
                    "text": preview,
                    "lang": result_lang,
                    "confidence": f"{conf_score:.1%}"
                }
                
                logs.append(new_data)
                file.seek(0)
                file.truncate()
                # Keep only the last 10 entries for simplicity
                json.dump(logs[-10:], file, indent=2)
        except Exception as err:
            print(f"Note: Could not save to history. ({err})")

    def run_detection(self, text):
        input_data = text.strip()
        
        # Check if the text is long enough to actually analyze
        if len(input_data) < 3:
            return {"status": "short", "message": "Input is too short! Please provide a longer string of text."}

        # Adding a small delay to make the UI feel better
        print("Analyzing linguistic patterns", end="", flush=True)
        for i in range(3):
            time.sleep(0.2)
            print(".", end="", flush=True)
        print("\n")

        try:
            # Get probabilities for different languages
            predictions = detect_langs(input_data)
            top_pick = predictions[0]
            
            lang_code = top_pick.lang.upper()
            full_name = LANG_NAMES.get(lang_code, f"Other ({lang_code})")
            score = top_pick.prob

            # Prepare the list of alternative predictions
            alternatives = []
            if len(predictions) > 1:
                for p in predictions[1:4]: # Show up to 3 alternatives
                    alt_name = LANG_NAMES.get(p.lang.upper(), p.lang.upper())
                    alternatives.append(f"{alt_name}: {p.prob:.1%}")

            # If the score is low, I should probably warn the user
            if score < 0.75:
                print("-- Notice: The analysis returned low confidence for the primary result. --")

            self.save_to_history(input_data, full_name, score)

            return {
                "status": "ok",
                "name": full_name,
                "score": f"{score:.1%}",
                "alternatives": alternatives
            }
        except:
            return {"status": "error", "message": "Could not detect any language."}

def main():
    app = LanguageDetectorApp()
    
    print("\n" + "*" * 40)
    print("      BYOP: MY LANGUAGE DETECTOR")
    print("*" * 40)

    while True:
        print("\nMain Menu:")
        print("1. Analyze text input")
        print("2. Analyze a .txt file")
        print("3. View analysis history")
        print("4. Exit")
        
        user_choice = input("\nPlease select an option: ").strip()

        if user_choice == '1':
            phrase = input("Please enter the text for analysis: ")
            res = app.run_detection(phrase)
            
            if res['status'] == 'ok':
                print("-" * 30)
                print(f"Primary Language: {res['name']}")
                print(f"Confidence Level: {res['score']}")
                
                if res['alternatives']:
                    print("\nOther possibilities:")
                    for alt in res['alternatives']:
                        print(f" - {alt}")
                print("-" * 30)
            else:
                print(f"Result: {res['message']}")

        elif user_choice == '2':
            file_path = input("Please enter the full filename: ")
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        res = app.run_detection(content)
                        if res['status'] == 'ok':
                            print("-" * 30)
                            print(f"File Detection: {res['name']}")
                            print(f"Confidence: {res['score']}")
                            if res['alternatives']:
                                print("\nOther possibilities:")
                                for alt in res['alternatives']:
                                    print(f" - {alt}")
                            print("-" * 30)
                except Exception as e:
                    print(f"Error reading file: {e}")
            else:
                print("Error: The specified file could not be found.")

        elif user_choice == '3':
            if os.path.exists("history.json"):
                with open("history.json", "r") as f:
                    try:
                        data = json.load(f)
                        if not data:
                            print("History is currently empty.")
                        else:
                            print(f"\n{'TIME':<10} | {'LANG':<12} | {'TEXT'}")
                            print("-" * 45)
                            for item in data:
                                print(f"{item['date']:<10} | {item['lang']:<12} | {item['text']}")
                    except:
                        print("Error reading history file.")
            else:
                print("No history file found.")

        elif user_choice == '4':
            print("Terminating program. Farewell.")
            break
        else:
            print("Invalid selection. Please enter a valid menu option (1-4).")

if __name__ == "__main__":
    main()