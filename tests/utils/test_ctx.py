class ShopTestContext:
    def __init__(self, player, item, quantity, playerId, shopRepo):
        self.player = player
        self.item = item
        self.quantity = quantity
        self.playerId = playerId
        self.shopRepo = shopRepo