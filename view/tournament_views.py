class SetTournament:

    def __init__(self):
        self.dict_tournament = {"Name" : "Entrer le nom du tournoi (3 caracteres minimum) : ",
                                "Place" : "Entrer la localisation du tournoi (3 caracteres minimum) : ",
                                "Date_start" : "Entrer la date de démarrage du tournoi (YYYY/MM/DD): ",
                                "Date_end" : "Entrer la date de fin du tournoi (YYYY/MM/DD): ",
                                "Game_mod" : f"Entrer le mode de jeu \n"
                                             f" bullet / blitz / fast : ",
                                "Number_player" : "Entrer le nombre de participants : ",
                                "Number_rounds": "Entrer le nombre de rounds : ",
                                "Description" : "Entrer un description du tournoi : ",}

    def write(self, attr):
        return input(self.dict_tournament[attr])

    def show_list_tournament(self, list):
        i = 1
        if len(list) == 0:
            print("Aucun Tournoi créé actuellement")
            return -1
        for tournament in list:
            print(f"[{i}] : {tournament.name} / {len(tournament.id_players)} Joueurs \n"
                  f"- {tournament.description}")
            i += 1
        return input("Quel tournoi voulez vous selectionner ? : ")