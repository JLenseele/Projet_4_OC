from operator import attrgetter


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
            2: 'Sélectionner un autre tournoi',
            3: 'Générer les rapports',
            4: 'Créer des joueurs',
            5: 'Modification des classements (ligue)',
            6: 'Enregistrer le programme',
            7: 'Importer données',
            8: 'Quitter'
        }
        print("\n Menu Principal")
        for key in menu_options.keys():
            print(' ', key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    def second_menu(self):
        menu_options = {
            1: 'Démarrer le tournoi',
            2: 'Inscription nouveau joueur au tournoi',
            3: 'Inscription joueur existant au tournoi',
            4: 'Retour Menu Principal',
            5: 'Quitter'
        }
        for key in menu_options.keys():
            print(' ', key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    def second_menu_option(self):
        return int(input("Combien de joueurs voulez vous inscrire ? "))

    def resolution(self):
        menu_options = {
            1: 'Cloturer le round',
            2: 'Quitter'
        }
        print("Une fois les matchs terminés, cloturez le round pour saisir les résultats")
        for key in menu_options.keys():
            print(key, '--', menu_options[key])
        choice = int(input(""))
        return choice

    def show_result(self, list_players):

        form = "{0:^10}{1:^10}{2:^15}{3:^15}{4:^5}"
        results = []

        print(f"=============================\n"
              f"Tournoi terminé\n"
              f"Classement final :\n")
        print(f"Classement / Score /       Nom      /      Prénom     /  Classement(ligue)")

        list_players.sort(key=attrgetter('score'), reverse=True)
        i = 1

        for player in list_players:
            print(form.format(i,
                              player.score,
                              player.name,
                              player.family_name,
                              player.rank,))
            line = [i, player.score, player.id_player, player.name, player.family_name]
            results.append(line)
            i += 1
        return results

    def menu_report(self):
        menu_options = {
            1: 'Rapport de tous les joueurs (Ordre alphabetique)',
            2: 'Rapport de tous les joueurs (Classement)',
            3: 'Liste de tous les tournois'
        }
        for key in menu_options.keys():
            print(' ', key, '--', menu_options[key])
        choice = int(input(""))
        return choice