# 📦 Gilded Rose 

This project is a refactored solution for the classic Gilded Rose Kata, demonstrating clean code, design patterns, and robust item quality management.

# 📋 Problem Statement
In the Gilded Rose store, items have a sell_in (days remaining to sell) and quality value.
Every day:

sell_in decreases by 1.

quality generally degrades, except for special items like "Aged Brie" and "Backstage Passes".

"Sulfuras" is a legendary item that never changes.

"Conjured" items degrade twice as fast.

The business rules require:

Quality is always between 0 and 50 (except Sulfuras, which has fixed 80).

Quality never becomes negative.

# 🛠️ Technologies Used

Python 3

OOP Design (classes, abstraction)

Design Patterns:

Strategy Pattern (different item behaviors)

Factory Pattern (item updater selection)

Wrapper Pattern (input validation)

# 🧩 Project Structure

File	Purpose
gilded_rose_refactored.py	Main code handling item updates, rules enforcement, and validation
tests/	(Optional) Unit tests to validate functionality

# 🧠 Key Design Concepts
Strategy Pattern: Each item type (Normal, Aged Brie, Backstage Passes, Sulfuras, Conjured) has its own updater class.

Factory Pattern: ItemUpdaterFactory selects the right updater dynamically.

Wrapper Class: AddItem ensures quality and constraints are validated when items are created.

# 🧠 Design Explanation
In this implementation, I designed a modular, extendable system to manage item behaviors for the Gilded Rose Inventory Management problem.
The goal was to separate concerns, apply design patterns, and enforce data integrity while keeping the system flexible for future changes.

Main Orchestration:
The GildedRose class drives the update process without hardcoding item logic.

Strategy Pattern:
Each item type has its own updater class — like NormalItemUpdater, AgedBrieUpdater, and BackstagePassUpdater — encapsulating its unique business rules.

Factory Pattern:
ItemUpdaterFactory selects the correct updater dynamically based on item name, keeping update_quality clean and open for extension.

Global Quality Rules:
ItemQualityRules ensures that item quality stays within allowed limits globally (e.g., [0–50] for most items, exactly 80 for Sulfuras).

Input Validation:
AddItem wrapper ensures no invalid items are added. It enforces:

No negative quality

Sulfuras must have a quality of exactly 80

No item quality exceeds 50 unless it's Sulfuras

SOLID Principles:
The design particularly follows the Open/Closed Principle —
To add a new item type, simply create a new updater class without modifying existing code.

# ✨ Summary:
This design makes the system scalable, testable, and easy to maintain as business rules evolve.


# ▶️ How to Run
bash
Copy
Edit
# Clone the repo
git clone https://github.com/nitinpapadkar/GildedRose.git
cd GildedRose

# Run the Python script
python3 gilded_rose.py

# ✅ Future Improvements
Add automated unit tests using unittest or pytest.

Extend support for more special items.

Improve simulation menu for more flexible testing.

# 🙏 Credits
Original problem: Gilded Rose Kata by Emily Bache

Refactoring & enhancement: Nitin Papadkar