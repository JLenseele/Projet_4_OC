class Error:

    def __init__(self):
        self.dict_error = {"ValueError": "Vous devez saisir un nombre",
                           "IndexError": "Cet element n'existe pas",
                           "TypeError": "Vous devez saisir un nombre",
                           "MenuError": "Ce choix n'est pas disponible",
                           "NameTournament": "Le nom du tournoi est trop court",
                           "PlaceTournament": "La localisation saisie est trop courte",
                           "DateFormat": "/! format incorect"
                                         "Le format doit etre de type : DD/MM/YYYY",
                           "DateEnd": "La date de fin de tournoi ne peut etre antérieure"
                                      "à la date de démarrage du tournoi",
                           "TooMuchPlayer": "Il ne peut y avoir plus de 20 joueurs dans un tournoi",
                           "ModTournament": "Ce mod de jeu n'existe pas",
                           "DescTournament": "La description est trop courte",
                           "Gender": "Erreur de saisie -> M ou F ",
                           "NamePlayer": "Le nom du joueur est trop court",
                           "TooLong": "Ce parametre est trop long (+40 caract)",
                           "NoNb": "Ce parametre ne doit pas contenir de nombre",
                           "TooMuchRounds": "Il ne peut y avoir plus de tours que de joueurs"
                                            "(Max rounds = Nombre de joueurs - 1)",
                           "PlayerMissing": "Il manque des joueurs pour démarrer le tournoi",
                           "NoPlayer": "Aucun joueur créé",
                           "AddNok": "=== Le tournoi en cour est plein. "
                                     "(Joueur enregistré dans la base de données global)",
                           "AddNok2": "=== Pas de tournoi en cour."
                                      " (Joueur enregistré dans la base de données global)"}

    def show_error(self, error):
        return print(self.dict_error[error])
