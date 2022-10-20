class SetTournament:

    def __init__(self):
        self.dict_tournament = {"Name" : "Entrer le nom du tournoi (3 caracteres minimum) : ",
                                "Place" : "Entrer la localisation du tournoi (3 caracteres minimum) : ",
                                "Date_start" : "Entrer la date de démarrage du tournoi (DD/MM/YYYY): ",
                                "Date_end" : "Entrer la date de fin du tournoi (DD/MM/YYYY): ",
                                "Game_mod" : f"Entrer le mode de jeu \n"
                                             f" bullet / blitz / fast : ",
                                "Number_player" : "Entrer le nombre de participants : ",
                                "Number_rounds": "Entrer le nombre de rounds : ",
                                "Description" : "Entrer un description du tournoi : ",
                                "AddOk" : "=== Inscription au tournoi OK",
                                "AddNok" : "=== Le tournoi en cour est plein. "
                                           "(Joueur enregistré dans la base de données global)",
                                "AddNok": "=== Pas de tournoi en cour. "
                                          "(Joueur enregistré dans la base de données global)"
                                }

    def write(self, attr):
        return input(self.dict_tournament[attr])

    def show(self, attr):
        return print(self.dict_tournament[attr])

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