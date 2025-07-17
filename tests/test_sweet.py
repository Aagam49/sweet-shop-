from sweets.sweet import Sweet
from sweets.inventory import InventoryManager

def test_add_sweet():
    inventory = InventoryManager()
    sweet = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 10)
    inventory.add_sweet(sweet)
    assert len(inventory.get_all_sweets()) == 1
    assert inventory.get_all_sweets()[0].name == "Kaju Katli"

def test_delete_sweet():
    inventory = InventoryManager()
    sweet = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 10)
    inventory.add_sweet(sweet)
    inventory.delete_sweet(1001)
    assert len(inventory.get_all_sweets()) == 0

def test_restock_sweet():
    inventory = InventoryManager()
    sweet = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 5)
    inventory.add_sweet(sweet)
    inventory.restock_sweet(1001, 10)
    assert sweet.quantity == 15
