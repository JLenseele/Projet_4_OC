class SetTournament:

    def __init__(self):
        self.dict_tournament = {"Name": "Entrer le nom du tournoi (3 caracteres minimum) : ",
                                "Place": "Entrer la localisation du tournoi (3 caracteres minimum) : ",
                                "Date_start": "Entrer la date de démarrage du tournoi (DD/MM/YYYY): ",
                                "Date_end": "Entrer la date de fin du tournoi (DD/MM/YYYY): ",
                                "Game_mod": "Entrer le mode de jeu \n"
                                            " bullet / blitz / fast : ",
                                "Nb_player": "Entrer le nombre de participants : ",
                                "Nb_rounds": "Entrer le nombre de rounds : ",
                                "Description": "Entrer une description du tournoi : ",
                                "AddOk": "=== Inscription au tournoi OK",
                                "Tournament_end": "Ce tournoi est terminé.",
                                "Open": "Un autre tournoi est déja en cour. Terminez ce tournoi "
                                        "avant d'en démarrer un nouveau."}

    def write(self, attr):
        return input(self.dict_tournament[attr])

    def show(self, attr):
        return print(self.dict_tournament[attr])

    @staticmethod
    def show_list_tournament(list_tournament):
        i = 1
        if len(list_tournament) == 0:
            print("Aucun Tournoi créé actuellement")
            return -1
        for tournament in list_tournament:
            print(f"[{i}] : {tournament.name} / {len(tournament.id_players)} Joueurs \n"
                  f"- {tournament.description}")
            i += 1
        return input("Quel tournoi voulez vous selectionner ? : ")
