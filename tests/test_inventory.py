import pytest
from sweets.sweet import Sweet
from sweets.inventory import InventoryManager

def test_search_by_name():
    inventory = InventoryManager()
    inventory.add_sweet(Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20))
    inventory.add_sweet(Sweet(1002, "Gulab Jamun", "Milk-Based", 30, 10))
    
    results = inventory.search_by_name("Gulab")
    assert len(results) == 1
    assert results[0].name == "Gulab Jamun"

def test_search_by_category():
    inventory = InventoryManager()
    inventory.add_sweet(Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20))
    inventory.add_sweet(Sweet(1002, "Rasgulla", "Milk-Based", 30, 15))
    
    results = inventory.search_by_category("Milk-Based")
    assert len(results) == 1
    assert results[0].name == "Rasgulla"

def test_search_by_price_range():
    inventory = InventoryManager()
    inventory.add_sweet(Sweet(1001, "Kaju Katli", "Nut-Based", 50, 20))
    inventory.add_sweet(Sweet(1002, "Gulab Jamun", "Milk-Based", 30, 10))
    inventory.add_sweet(Sweet(1003, "Rasgulla", "Milk-Based", 70, 15))

    results = inventory.search_by_price_range(30, 60)
    names = [s.name for s in results]
    assert "Kaju Katli" in names
    assert "Gulab Jamun" in names
    assert "Rasgulla" not in names

def test_purchase_sweet_success():
    inventory = InventoryManager()
    sweet = Sweet(1001, "Kaju Katli", "Nut-Based", 50, 10)
    inventory.add_sweet(sweet)
        
    inventory.purchase_sweet(1001, 3)
        
    assert sweet.quantity == 7  # 10 - 3

def test_purchase_sweet_insufficient_stock():
    inventory = InventoryManager()
    sweet = Sweet(1002, "Gulab Jamun", "Milk-Based", 30, 5)
    inventory.add_sweet(sweet)

    with pytest.raises(ValueError) as exc:
        inventory.purchase_sweet(1002, 10)

    assert "Not enough stock" in str(exc.value)

def test_purchase_sweet_not_found():
    inventory = InventoryManager()
        
    with pytest.raises(ValueError) as exc:
        inventory.purchase_sweet(9999, 2)

    assert "Sweet not found" in str(exc.value)