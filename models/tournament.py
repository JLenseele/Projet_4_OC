GAME_MODE = ("bullet", "blitz", "fast")
NB_TOURS = 4
NB_PLAYER = 8


class Tournament:
    """
    Class Tournament
    """
    def __init__(self, name, place, date_start, date_end, list_player, game_mode, description, list_tour):
        self.name = name
        self.place = place
        self.date_start = date_start
        self.date_end = date_end
        self.list_player = list_player
        self.game_mode = game_mode
        self.description = description
        self.list_tour = list_tour

