class InventoryManager:
    def __init__(self):
        self.sweets = []

    def add_sweet(self, sweet):
        for s in self.sweets:
            if s.id == sweet.id:
                raise ValueError("Sweet with this ID already exists.")
        self.sweets.append(sweet)

    def delete_sweet(self, sweet_id):
        self.sweets = [s for s in self.sweets if s.id != sweet_id]

    def restock_sweet(self, sweet_id, quantity):
        for s in self.sweets:
            if s.id == sweet_id:
                s.quantity += quantity
                return
        raise ValueError("Sweet not found to restock.")

    def get_all_sweets(self):
        return self.sweets
    

    def search_by_name(self, name):
        return [s for s in self.sweets if name.lower() in s.name.lower()]

    def search_by_category(self, category):
        return [s for s in self.sweets if category.lower() == s.category.lower()]

    def search_by_price_range(self, min_price, max_price):
        return [s for s in self.sweets if min_price <= s.price <= max_price]
    
    def purchase_sweet(self, sweet_id, quantity):
        for sweet in self.sweets:
            if sweet.id == sweet_id:
                if sweet.quantity >= quantity:
                    sweet.quantity -= quantity
                    return
                else:
                    raise ValueError("Not enough stock to complete the purchase.")
        raise ValueError("Sweet not found.")

