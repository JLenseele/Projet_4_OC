from operator import attrgetter


class Report:

    def __init__(self):
        self.report = None

    @staticmethod
    def prompt_report(tournaments, players, rapport):

        if tournaments == [] or players == []:
            print("Creez des tournois et des joueurs avant de pouvoir afficher des rapports")
            return

        if rapport == 1:
            Report.prompt_classement(players, 'name')
        elif rapport == 2:
            Report.prompt_classement(players, 'rank')
        elif rapport == 3:
            Report.prompt_tournament(tournaments, 'name')
        elif rapport == 4:

            tournaments.sort(key=attrgetter('name'))
            i = 1
            for tournament in tournaments:
                print(f"[{i}]")
                tournament.__str__()
                i += 1

            choice = input("Choisissez le numéro d'un tournoi pour afficher les détails")
            tournament = tournaments[int(choice) - 1]
            print(f"====================================================\n"
                  f"- Détail du tournoi {tournament.name} :\n")

            print("Liste des participants (ordre alphabétique) :")
            Report.prompt_classement(tournament.player, 'name')

            print("\nListe des participants (par classement) :")
            Report.prompt_classement(tournament.player, 'rank')

            print("\nListe Rounds et Matchs du tournoi :\n")
            for tour in tournament.list_tour:
                print("#", tour.name)
                for match in tour.list_matchs:
                    match.__str__()

    @staticmethod
    def prompt_classement(players, attr):

        players.sort(key=attrgetter(attr))
        print("   ID  /      NOM      /     PRENOM    / DATE NAISSANCE / G /Classement(ligue)")
        for player in players:
            player.__str__()

    @staticmethod
    def prompt_tournament(tournaments, attr):

        tournaments.sort(key=attrgetter(attr))
        for tournament in tournaments:
            tournament.__str__()

    @staticmethod
    def prompt_result(tournament):

        list_players = tournament.player
        form = "{0:^10}{1:^10}{2:^17}{3:^18}{4:^10}"
        results = []

        print("=============================\n")
        if not tournament.open:
            print("Tournoi terminé\n"
                  "Classement Final :\n")
        else:
            print("Classement provisoire :\n")

        print("Classement / Score /       Nom      /      Prénom     /  Classement(ligue)")

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
