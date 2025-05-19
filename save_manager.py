import os
import pickle

SAVE_DIR = "saved_games"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_user_save_path(username):
    return os.path.join(SAVE_DIR, f"{username}_saves.pkl")

def load_user_saves(username):
    path = get_user_save_path(username)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return {}

def save_game(username, slot_name, data):
    saves = load_user_saves(username)
    if len(saves) >= 5 and slot_name not in saves:
        return False, "Máximo de 5 partidas alcanzado."
    saves[slot_name] = data
    with open(get_user_save_path(username), "wb") as f:
        pickle.dump(saves, f)
    return True, "Partida guardada correctamente."

def delete_game(username, slot_name):
    saves = load_user_saves(username)
    if slot_name in saves:
        del saves[slot_name]
        with open(get_user_save_path(username), "wb") as f:
            pickle.dump(saves, f)
        return True
    return False