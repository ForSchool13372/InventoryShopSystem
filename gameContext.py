class GameContext:
    def __init__(self, player, playerId, services, repos, world, questManager, gameEventService):
        self.player = player
        self.playerId = playerId
        self.services = services
        self.repos = repos
        self.world = world
        self.questManager = questManager
        self.gameEventService = gameEventService