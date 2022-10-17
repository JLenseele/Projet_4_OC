class Error:

    def __init__(self):
        self.dict_error = {"ValueError": "/!\ Vous devez saisir un nombre\n",
                           "IndexError": "/!\ Cet élément n'existe pas\n",
                           "TypeError": "/!\ Vous devez saisir un nombre\n",
                           "MenuError" : "/!\ Ce choix n'est pas disponible\n",
                           "NameTournament" : "/!\ Le nom du tournoi est trop court\n",
                           "PlaceTournament" : "/!\ La localisation saisie est trop courte\n",
                           "DateTournament" : "/!\ format incorect \n "
                                              "Le format doit etre de type : YYYY/MM/DD",
                           "ModTournament" : "Ce mod de jeu n'existe pas",
                           "DescTournament" : "La description est trop courte",
                           "TooLong" : "Ce parametre est trop long",
                           "NoNb" : "Ce parametre ne doit pas contenir de nombre",
                           "MoreRoundThanPlayer" : "Il ne peut y avoir plus de tours que de joueurs"
                                                   "(Max rounds = Nombre de joueurs - 1)",
                           "PlayerMissing" : "Il manque des joueurs pour démarrer le tournoi",
                           "NoPlayer" : "Aucun joueur créé"}

    def show_error(self, error):
        return print(self.dict_error[error])

