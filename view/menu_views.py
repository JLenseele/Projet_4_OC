class Menu:

    def __init__(self):
        self.present()

    @staticmethod
    def present():
        print("========================================\n"
              "||||||||||| CHESS TOURNAMENT |||||||||||\n"
              "========================================\n")

    @staticmethod
    def main_menu(tournament):
        menu_options = {
            1: 'Créer un nouveau tournoi',
            2: 'Sélectionner un tournoi',
            3: 'Générer les rapports',
            4: 'Créer des joueurs',
            5: 'Modification des classements (ligue)',
            6: 'Enregistrer le programme',
            7: 'Importer données',
            8: 'Quitter'
        }

        if tournament:
            print(f"\n[== Tournoi actuellement selectionné : {tournament.name} ==]")
        print("---------------\n Menu Principal \n")
        for key in menu_options.keys():
            print(' ', key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    @staticmethod
    def second_menu():
        menu_options = {
            1: 'Démarrer le tournoi',
            2: 'Inscription nouveau joueur au tournoi',
            3: 'Inscription joueur existant au tournoi',
            4: 'Retour Menu Principal',
            5: 'Quitter'
        }
        for key in menu_options.keys():
            print(' ', key, '--', menu_options[key])
        choice = int(input())
        return choice

    @staticmethod
    def second_menu_option():
        return int(input("Combien de joueurs voulez vous inscrire ? "))

    @staticmethod
    def resolution():
        menu_options = {
            1: 'Cloturer le round',
            2: 'Afficher le classement provisoire',
            3: 'Retour - Menu Principal'
        }
        print("Une fois les matchs terminés, cloturez le round pour saisir les résultats")
        for key in menu_options.keys():
            print(key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    @staticmethod
    def menu_report():
        menu_options = {
            1: 'Rapport de tous les joueurs (Ordre alphabetique)',
            2: 'Rapport de tous les joueurs (Classement)',
            3: 'Liste de tous les tournois',
            4: "Rapport complet d'un tournoi"
        }
        for key in menu_options.keys():
            print(' ', key, '--', menu_options[key])
        choice = int(input(""))
        return choice
