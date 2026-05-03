import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_settings():
    default = {"sound": True, "car_color": "red", "difficulty": "Medium"}
    if not os.path.exists(SETTINGS_FILE):
        save_settings(default)
        return default
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return default

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_score(name, score, distance):
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": int(distance)})
    board = sorted(board, key=lambda x: x['score'], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(board, f, indent=4)