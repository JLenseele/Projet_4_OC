class Tour:


    def __init__(self, name, list_matchs, date_start, date_end):
        self.name = name
        self.list_matchs = list_matchs
        self.date_start = date_start
        self.date_end = date_end

    def __str__(self):
        show_match = ""
        frm = "%d/%m/%Y %H:%M:%S"
        for match in self.list_matchs:
            player1 = match.player_1
            player2 = match.player_2
            name1 = player1.name
            name2 = player2.name
            rank1 = player1.rank
            rank2 = player2.rank
            score1 = player1.score
            score2 = player2.score

            show_match = f"{show_match} [{name1}:(R:{rank1}/S:{score1}) VS {name2}:(R:{rank2}/S:{score2})] \n"

        print(f"--- {self.name} ------------------------------------------\n"
              f"** Liste des matchs à jouer **\n"
              f"{show_match}\n"
              f"-- Démarrage : {self.date_start.strftime(frm)} -----")

