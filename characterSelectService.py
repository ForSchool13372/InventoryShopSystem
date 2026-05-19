from sqlalchemy import text
from database import engine

def selectCharacter():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, gold, level, hp
            FROM player
            ORDER BY id
        """)).fetchall()

    print("\n=== CHARACTER SELECT ===")

    for r in rows:
        print(f"Slot {r[0]} | Gold: {r[1]} | Level: {r[2]} | HP: {r[3]}")

    while True:
        try:
            choice = int(input("\nSelect Slot (1-3): "))

            if choice in [1, 2, 3]:
                return choice
            else:
                print("Choose 1, 2, or 3 only.")

        except ValueError:
            print("Enter a number.")