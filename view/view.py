class Menu:


    def __init__(self):
        self.list_error = []
        self.present()

    def present(self):
        print("--------------------------------------------------------------\n"
              "---------------------- CHESS TOURNAMENT ----------------------\n"
              "______________________________________________________________\n")

    def main_menu(self):
        menu_options = {
            1: 'Créer un tournoi',
            2: 'Quitter',
        }
        for key in menu_options.keys():
            print(key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    def set_name_tournament(self):
        name = input("Entrer le nom du tournoi : ")
        return name

    def set_place_tournament(self):
        return input("Entrer la localisation du tournoi : ")

    def set_date_start(self):
        return input("Entrer la date de démarrage du tournoi : ")

    def set_date_end(self):
        return input("Entrer la date de fin du tournoi : ")

    def set_game_mode(self, mods):
        return input(f"Entrer le mode de jeu : \n"
                     f"{mods} : ")

    def set_description(self):
        return input("Entrer un description du tournoi : ")

    def set_id_player(self):
        return input("Entrer l'identifiant du Joueur : ")

    def set_family_name(self):
        return input("Nom : ")

    def set_birthday(self):
        return input("Date de naissance  : ")

    def set_name_player(self):
        return input("Prénom : ")

    def set_sex(self):
        return input("Genre (M/F) : ")

    def set_rank(self):
        return input("Classement actuel : ")
