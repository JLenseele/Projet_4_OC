class SetPlayer:

    def __init__(self):
        self.dict_player = {"Family_name" : "Nom : ",
                            "Birthday" : "Date de naissance DD/MM/YYYY : ",
                            "Name" : "Prénom : ",
                            "Sex" : "Genre (M/F) : ",
                            "Rank" : "Classement actuel : "}

    def write(self, attr):
        return input(self.dict_player[attr])

    def menu_list_player(self, attr):
        if attr == "id":
            return print("Saisissez les ID Joueurs un par un pour les ajouter au tournoi (Q pour quitter) :")
        elif attr == "rank":
            return input("Saisissez l'ID d'un joueurs pour modifier son classement (Q pour quitter)")
        elif attr == "new_rank":
            return input("Nouveaux classement (ligue) : ")
        else:
            return input()
