class GameContext:
    def __init__(
        self,
        player,
        playerId,
        services,
        repos,
        world,
        questManager,
        gameEventService,
        auth=None
    ):
        # =========================================================
        # CORE STATE
        # =========================================================
        self.player = player
        self.playerId = playerId
        self.world = world

        # =========================================================
        # DEPENDENCIES
        # =========================================================
        self.services = services
        self.repos = repos
        self.questManager = questManager
        self.gameEventService = gameEventService

        # =========================================================
        # OPTIONAL (CLEAN EXTENSION POINT)
        # =========================================================
        self.auth = auth

    # =========================================================
    # SHORTCUT ACCESSORS (OPTIONAL BUT CLEANER LONG TERM)
    # =========================================================

    @property
    def combat(self):
        return self.services.combat

    @property
    def shop(self):
        return self.services.shop

    @property
    def items(self):
        return self.services.item

    @property
    def player_repo(self):
        return self.repos.player

    @property
    def inventory_repo(self):
        return self.repos.inventory

    @property
    def shop_repo(self):
        return self.repos.shop