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

    def start_round(self):
        menu_options = {
            1: 'Démarrer',
            2: 'Quitter',
        }
        for key in menu_options.keys():
            print(key, '--', menu_options[key])
        choice = int(input(""))