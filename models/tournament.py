class Tournament:
    """
    Class Tournament
    """
    def __init__(self, name, place, date_start, date_end,
                 id_players, game_mode, description, nb_tours,
                 nb_player, list_player, list_tour, result=None, open=True):

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
        self.open = open

    def __str__(self):
        frm = "%d %b %Y"
        print(f"----------------------------------------------------------------------------------\n"
              f" Tournoi : {self.name} à {self.place},"
              f"du {self.date_start.strftime(frm)} au {self.date_end.strftime(frm)} \n"
              f" {self.nb_tours} Rounds / Mode de jeu : {self.game_mode}\n"
              f" Joueurs actuel : {len(self.id_players)} / {self.nb_player} \n"
              f"----------------------------------------------------------------------------------\n")
        if not self.open:
            print("Tournoi terminé : \n"
                  "Résultat final : \n"
                  "[R][S][  ID  ][      Prénom/Nom     ]")
            for line in self.result:
                print(line)

    def add_list_player(self, list_player):
        self.player = list_player
