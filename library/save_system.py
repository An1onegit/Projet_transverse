import json
import os

SAVE_FILE_PATH = "save_data.json"

def save_game(player_data, inventory_data):
    data_to_save = {
        "player": {
            "pos_x": player_data["position"].x,
            "pos_y": player_data["position"].y,
        },
        "inventory": {
            "money": inventory_data["money"],
            "fishes": inventory_data["fishes"],
            "rods": inventory_data["rods"],
            "equipped_rod": inventory_data["equipped_rod"],
        }
    }
    with open(SAVE_FILE_PATH, 'w') as f:
        json.dump(data_to_save, f, indent=4)
    print("Game saved successfully.")

def load_game():
    if not os.path.exists(SAVE_FILE_PATH):
        print("No save file found. Starting a new game.")
        return None

    with open(SAVE_FILE_PATH, 'r') as f:
        data = json.load(f)
    print("Game loaded successfully.")
    return data

def get_default_player_data(initial_pos_x, initial_pos_y):
    return {
        "pos_x": initial_pos_x,
        "pos_y": initial_pos_y
    }

def get_default_inventory_data():
    return {
        "money": 0,
        "fishes": [],
        "rods": ["Basic Rod"],
        "equipped_rod": "Basic Rod"
    }