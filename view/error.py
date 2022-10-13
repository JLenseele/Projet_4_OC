class Error:

    def __init__(self):
        self.dict_error = {"ValueError": "/!\ Vous devez saisir un nombre\n",
                           "MenuError" : "/!\ Ce choix n'est pas disponible\n",
                           "NameTournament" : "/!\ Le nom du tournoi est trop court\n",
                           "PlaceTournament" : "/!\ La localisation saisie est trop courte\n",
                           "DateTournament" : "/!\ format incorect \n "
                                              "Le format doit etre de type : YYYY/MM/DD",
                           "ModTournament" : "Ce mod de jeu n'existe pas",
                           "DescTournament" : "La description est trop courte",
                           "TooLong" : "Ce parametre est trop long",
                           "NoNb" : "Ce parametre ne doit pas contenir de nombre"}

    def show_error(self, error):
        return print(self.dict_error[error])

