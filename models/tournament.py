from datetime import date


class Tournament:
    """
    Class Tournament
    """
    def __init__(self, name, place, date_start, date_end, id_players, game_mode, description, list_tour):
        self.name = name
        self.place = place
        self.date_start = date_start
        self.date_end = date_end
        self.id_players = id_players
        self.game_mode = game_mode
        self.description = description
        self.list_tour = list_tour

    def __str__(self):
        return print(f"----------------------------------------------------------------------------------\n"
                     f"Tournoi créé : {self.name} à {self.place}, du {self.date_start} au {self.date_end} \n"
                     f"----------------------------------------------------------------------------------\n"
                     f"Joueurs actuel : {len(self.id_players)} \n")

    def add_list_player(self, list):
        self.list_player = list
