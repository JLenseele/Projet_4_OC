class Menu:


    def __init__(self):
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

    def second_menu(self):
        menu_options = {
            1: 'Ajouter des joueurs',
            2: 'Quitter',
        }
        for key in menu_options.keys():
            print(key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    def start_round(self):
        menu_options = {
            1: 'Démarrer le tournoi',
            2: 'Quitter',
        }
        for key in menu_options.keys():
            print(key, '--', menu_options[key])
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