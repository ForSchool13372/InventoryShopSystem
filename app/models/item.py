class Item:
    def __init__(
        self,
        name,
        price,
        itemType="misc",
        description="",
        rarity="common"
    ):
        self.name = name.lower()
        self.price = price

        self.itemType = itemType
        self.description = description
        self.rarity = rarity