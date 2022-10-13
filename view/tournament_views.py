class SetTournament:

    def __init__(self):
        self.dict_tournament = {"Name" : "Entrer le nom du tournoi (3 caracteres minimum) : ",
                                "Place" : "Entrer la localisation du tournoi (3 caracteres minimum) : ",
                                "Date_start" : "Entrer la date de démarrage du tournoi (YYYY/MM/DD): ",
                                "Date_end" : "Entrer la date de fin du tournoi (YYYY/MM/DD): ",
                                "Game_mod" : f"Entrer le mode de jeu \n"
                                             f" bullet / blitz / fast : ",
                                "Description" : "Entrer un description du tournoi : ",}

    def write(self, attr):
        return input(self.dict_tournament[attr])