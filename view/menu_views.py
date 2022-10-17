class Menu:


    def __init__(self):
        self.present()

    def present(self):
        print("========================================\n"
              "||||||||||| CHESS TOURNAMENT |||||||||||\n"
              "========================================\n")

    def main_menu(self):
        menu_options = {
            1: 'Créer un nouveau tournoi',
            2: 'Sélectionner un tournoi en cour',
            3: 'Générer les rapports',
            4: 'Quitter',
        }
        print("\n Menu Principal")
        for key in menu_options.keys():
            print(' ', key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    def second_menu(self):
        menu_options = {
            1: 'Démarrer le tournoi',
            2: 'Saisir un nouveau joueur au tournoi',
            3: 'Ajouter un joueur existant au tournoi',
            4: 'Retour Menu Principal',
            5: 'Quitter',
        }
        for key in menu_options.keys():
            print(' ', key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    def start_round(self):
        menu_options = {
            1: 'Démarrer le tournoi',
            2: 'Quitter',
        }
        for key in menu_options.keys():
            print(' ', key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    def resolution(self):
        menu_options = {
            1: 'Cloturer le round',
            2: 'Quitter',
        }

        print("Une fois les matchs terminés, cloturez le round pour saisir les résultats")
        for key in menu_options.keys():
            print(key, '--', menu_options[key])
        choice = int(input(""))
        return choice