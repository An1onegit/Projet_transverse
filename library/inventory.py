ROD_STATS = {
        "Basic Rod": 600,
        "Advanced Rod": 900,
        "Super Rod": 1200,
        "Legendary Rod": 1500
    }

class Inventory:
    def __init__(self):
        self.fishes = []
        self.rods = ["Basic Rod"]
        self.money = 0
        self.equipped_rod = "Basic Rod"

    def add_fish(self, fish):
        self.fishes.append(fish)

    def sell_fish(self, fish_name, price_per_fish):
        if fish_name in self.fishes:
            self.fishes.remove(fish_name)
            self.money += price_per_fish
            return True
        return False

    def buy_rod(self, rod_name, cost):
        if self.money >= cost:
            self.money -= cost
            self.rods.append(rod_name)
            return True
        return False

    def equip_rod(self, rod_name):
        if rod_name in self.rods:
            self.equipped_rod = rod_name

    def get_rod_power(self):
        return ROD_STATS.get(self.equipped_rod, 500)
    
    def get_save_data(self):
        """Return the data we want to save, in a serializable form."""
        return {
            "items": self.items,
            "level": self.level,
        }

    def load_from_data(self, data):
        """Load game data (like inventory items) from saved data."""
        self.items = data.get("items", [])
        self.level = data.get("level", 1)
