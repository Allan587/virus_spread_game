import os
import pickle

SAVE_DIR = "saved_games"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_user_save_path(username):
    """Gets the user's saved game.

    Args:
        username (str): get user's name to search for the path 

    Returns:
        path: returns the path where the user's games was saved
    """
    return os.path.join(SAVE_DIR, f"{username}_saves.pkl")

def load_user_saves(username):
    """Gets into the path indexed to the user's name

    Args:
        username (str): use it to checks if the user path exist, then returns the path

    Returns:
        file: returns saved games indexed with the user's name
    """
    path = get_user_save_path(username)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return {}

def save_game(username, slot_name, data):
    """This function saves games using the user's name as an index

    Args:
        username (str): used as an index
        slot_name (str):  file that contains the game

    Returns:
        bool: returns "True" if the game was saved efectly and "False" otherwise
    """
    saves = load_user_saves(username)
    if len(saves) >= 5 and slot_name not in saves:
        return False, "Máximo de 5 partidas alcanzado."
    saves[slot_name] = data
    with open(get_user_save_path(username), "wb") as f:
        pickle.dump(saves, f)
    return True, "Partida guardada correctamente."

def delete_game(username, slot_name):
    """This function delete saves game

    Args:
        username (str): Takes the username to search for saved games indexed to the user
        slot_name (str): the file with the saved game

    Returns:
        _type_: _description_
    """
    saves = load_user_saves(username)
    if slot_name in saves:
        del saves[slot_name]
        with open(get_user_save_path(username), "wb") as f:
            pickle.dump(saves, f)
        return True
    return False