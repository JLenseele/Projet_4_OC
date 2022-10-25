from datetime import date


class Tournament:
    """
    Class Tournament
    """
    def __init__(self, name, place, date_start, date_end, id_players, game_mode, description, nb_tours, nb_player, list_player, list_tour, result=None):
        self.name = name
        self.place = place
        self.date_start = date_start
        self.date_end = date_end
        self.id_players = id_players
        self.game_mode = game_mode
        self.description = description
        self.nb_tours = nb_tours
        self.nb_player = nb_player
        self.player = list_player
        self.list_tour = list_tour
        self.result = result

    def __str__(self):
        frm = "%d %b %Y"
        return print(f"----------------------------------------------------------------------------------\n"
                     f" Tournoi : {self.name} à {self.place}, du {self.date_start.strftime(frm)} au {self.date_end.strftime(frm)} \n"
                     f" En {self.nb_tours} Rounds \n"
                     f" Joueurs actuel : {len(self.id_players)} / {self.nb_player} \n"
                     f"----------------------------------------------------------------------------------\n")

    def add_list_player(self, list):
        self.list_player = list

