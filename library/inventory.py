class Inventory:
    def __init__(self):
        self.fishes = []  # list of fish caught
        self.rods = ["Basic Rod"]  # player starts with 1 rod
        self.money = 0  # start with $0

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

    def add_money(self):
        self.money += 1000
    