from operator import attrgetter

class Report:


    def prompt_report(self, tournaments, players, rapport):

        if tournaments == [] or players == []:
            print("Creez des tournois et des joueurs avant de pouvoir afficher des rapports")
            return

        if rapport == 1:
            players.sort(key=attrgetter('name'))
            print(f"   ID  /    NOM    /    PRENOM    / DATE NAISSANCE / G /Classement(ligue)")
            for player in players:
                player.__str__()
        elif rapport == 2:
            players.sort(key=attrgetter('rank'))
            print(f"   ID  /    NOM    /    PRENOM    / DATE NAISSANCE / G /Classement(ligue)")
            for player in players:
                player.__str__()
        elif rapport == 3:
            tournaments.sort(key=attrgetter('name'))
            i = 1
            for tournament in tournaments:
                print(f"[{i}]")
                tournament.__str__()
                i += 1

            choice = input("Vous pouvez choisir le numéro d'un tournoi pour voir les détails")
            tournament = tournaments[int(choice) - 1]
            print(f"====================================================\n"
                  f"- Détail du tournoi {tournament.name} :\n"
                  f"\n"
                  f"Liste des participants (ordre alphabétique) :")
            print(f"   ID  /    NOM    /    PRENOM    / DATE NAISSANCE / G /Classement(ligue)")

            tournament.player.sort(key=attrgetter('name'))
            for player in tournament.player:
                print(f"{player.__str__()}")

            print(f"\nListe des participants (par classement) :"
                  f"   ID  /    NOM    /    PRENOM    / DATE NAISSANCE / G /Classement(ligue)")

            tournament.player.sort(key=attrgetter('rank'))
            for player in tournament.player:
                print(f"{player.__str__()}")

            print(f"Liste Rounds et Matchs du tournoi :")
            for tour in tournament.list_tour:
                print("#", tour.name)
                for match in tour.list_matchs:
                    print("  -", match.__str__())

