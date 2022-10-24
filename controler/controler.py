import itertools
import random

from models.tournament import Tournament
from models.player import Player
from models.tour import Tour
from models.match import Match
from view.menu_views import Menu
from view.tournament_views import SetTournament
from view.playerviews import SetPlayer
from view.error import Error
from view.report import Report

from operator import attrgetter
from datetime import datetime
from tinydb import TinyDB
from math import floor


GAME_MODE = ("bullet", "blitz", "fast")


class MainController:
    """Main controller."""
    def __init__(self):
        # models
        self.tournament = None

        # views
        self.menu = Menu()
        self.set_tournament = SetTournament()
        self.set_player = SetPlayer()
        self.error = Error()
        self.report = Report()

        # listes du controller
        self.list_id = []
        self.list_tour = []
        self.list_matchs = []
        self.list_tournament = []
        self.list_associate_player = []
        self.list_players = []

    def run(self):

        valid_choice = False
        while not valid_choice:
            try:
                main_menu = self.menu.main_menu()
            except ValueError:
                self.error.show_error("ValueError")
            else:
                if main_menu == 1:
                    self.create_tournament()
                    valid_choice = True
                elif main_menu == 2:
                    self.pick_tournament()
                    valid_choice = True
                elif main_menu == 3:
                    report = self.menu.menu_report()
                    self.report.prompt_report(self.list_tournament, self.list_players, report)
                elif main_menu == 4:
                    self.create_player()
                elif main_menu == 5:
                    self.edit_rank()
                elif main_menu == 6:
                    self.serialized()
                elif main_menu == 7:
                    self.deserialized()
                elif main_menu == 8:
                    valid_choice = True
                    quit()
                else:
                    self.error.show_error("MenuError")

    def check_second_menu(self):

        valid_choice = False
        while not valid_choice:
            try:
                second_menu = self.menu.second_menu()
            except ValueError:
                self.error.show_error("ValueError")
            else:
                if second_menu == 1:
                    if self.tournament.nb_player > len(self.tournament.id_players):
                        self.error.show_error("PlayerMissing")
                        print(f"({len(self.tournament.id_players)} / {self.tournament.nb_player})\n")
                    else:
                        valid_choice = True
                        self.start_tournament()
                elif second_menu == 2:
                    self.create_player()
                elif second_menu == 3:
                    self.add_player()
                elif second_menu == 4:
                    self.run()
                    valid_choice = True
                elif second_menu == 5:
                    valid_choice = True
                    quit()
                else:
                    self.error.show_error("MenuError")

    def start_tournament(self):

        self.create_tour()
        i = 0
        while i < self.tournament.nb_tours:

            if i == 0:
                method = 'split'
            else:
                method = 'swiss'

            self.create_match(method)
            matchs = self.list_matchs

            valid_choice = False
            while not valid_choice:
                try:
                    main_menu = self.menu.resolution()
                except ValueError:
                    self.error.show_error("ValueError")
                else:
                    if main_menu == 1:
                        self.solve_matchs(matchs)
                        self.close_round()
                        valid_choice = True
                    elif main_menu == 2:
                        valid_choice = True
                        quit()
                    else:
                        self.error.show_error("MenuError")
            i += 1
        self.tournament.result = (self.menu.show_result(self.tournament.player))
        self.tournament = None
        self.run()

    def create_tournament(self):

        valid_name = False
        while not valid_name:
            name = self.set_tournament.write("Name")
            if len(name) < 3:
                self.error.show_error("NameTournament")
            else:
                valid_name = True

        valid_place = False
        while not valid_place:
            place = self.set_tournament.write("Place")
            if len(place) < 3:
                self.error.show_error("PlaceTournament")
            else:
                valid_place = True

        valid_date = False
        date_format = "%d/%m/%Y"
        while not valid_date:
            try:
                date_start = self.set_tournament.write("Date_start")
                date_start = datetime.strptime(date_start, date_format)
            except ValueError:
                self.error.show_error("DateFormat")
            except TypeError:
                print("error TypeError")
            else:
                valid_date = True

        valid_date = False
        while not valid_date:
            try:
                date_end = self.set_tournament.write("Date_end")
                date_end = datetime.strptime(date_end, date_format)
            except ValueError:
                self.error.show_error("DateFormat")
            except TypeError:
                print("error TypeError")
            else:
                if date_end < date_start:
                    self.error.show_error("DateEnd")
                else:
                    valid_date = True

        mods = ""
        for mod in GAME_MODE:
            mods = f"{mods} / {mod}"

        valid_mod = False
        while not valid_mod:
            game_mod = self.set_tournament.write("Game_mod")
            if game_mod in GAME_MODE:
                valid_mod = True
            else:
                self.error.show_error("ModTournament")

        valid_nbplayer = False
        while not valid_nbplayer:
            try:
                nb_player = int(self.set_tournament.write("Number_player"))
            except ValueError:
                self.error.show_error("ValueError")
            except TypeError:
                print("error TypeError")
            else:
                valid_nbplayer = True

        valid_nbround = False
        while not valid_nbround:
            try:
                nb_rounds = int(self.set_tournament.write("Number_rounds"))
            except ValueError:
                self.error.show_error("ValueError")
            except TypeError:
                print("error TypeError")
            else:
                if nb_rounds >= nb_player:
                    self.error.show_error("MoreRoundThanPlayer")
                else:
                    valid_nbround = True

        valid_desc = False
        while not valid_desc:
            description = self.set_tournament.write("Description")
            if len(description) < 10:
                self.error.show_error("DescTournament")
            else:
                valid_desc = True

        list_tour = []
        id_players = []

        self.tournament = Tournament(name,
                                     place,
                                     date_start,
                                     date_end,
                                     id_players,
                                     game_mod,
                                     description,
                                     nb_rounds,
                                     nb_player)
        self.tournament.__str__()
        self.list_tournament.append(self.tournament)

        self.check_second_menu()

    def pick_tournament(self):

        pick = int(self.set_tournament.show_list_tournament(self.list_tournament)) - 1
        if pick > -1:
            try:
                self.tournament = self.list_tournament[pick]
                self.check_second_menu()
            except IndexError:
                self.error.show_error("IndexError")
                self.run()
            except ValueError:
                self.error.show_error("ValueError")
                self.run()
        else:
            self.run()

    def create_player(self):
        """
        Call Menu to add some player
        to the tournament
        """
        instances = self.menu.second_menu_option()
        for instance in range(instances):
            id_player = random.randint(10000, 99999)
            while id_player in self.list_id:
                id_player = random.randint(10000, 99999)

            valid_fname = False
            while not valid_fname:
                family_name = self.set_player.write("Family_name")
                if any(caract.isdigit() for caract in family_name):
                    self.error.show_error("NoNb")
                elif len(family_name) > 40:
                    self.error.show_error("TooLong")
                else:
                    valid_fname = True

            valid_name = False
            while not valid_name:
                name = self.set_player.write("Name")
                if any(caract.isdigit() for caract in name):
                    self.error.show_error("NoNb")
                elif len(family_name) > 40:
                    self.error.show_error("TooLong")
                else:
                    valid_name = True

            valid_birth = False
            date_format = "%d/%m/%Y"
            while not valid_birth:
                try:
                    date_birth = self.set_player.write("Birthday")
                    date_birth = datetime.strptime(date_birth, date_format)
                except ValueError:
                    self.error.show_error("DateFormat")
                except TypeError:
                    self.error.show_error("DateFormat")
                else:
                    valid_birth = True

            valid_sex = False
            gender = ['m', 'f']
            while not valid_sex:
                sex = self.set_player.write("Sex")
                if sex.lower() in gender:
                    valid_sex = True
                else:
                    self.error.show_error("Gender")

            valid_rank = False
            while not valid_rank:
                try:
                    rank = int(self.set_player.write("Rank"))
                except ValueError:
                    self.error.show_error("ValueError")
                except TypeError:
                    print("error TypeError")
                else:
                    valid_rank = True

            player = Player(id_player, family_name, name, date_birth, sex, rank)
            self.list_players.append(player)
            self.list_id.append(player.id_player)
            if self.tournament:
                if len(self.tournament.player) < self.tournament.nb_player:
                    self.tournament.player.append(player)
                    self.tournament.id_players.append(player.id_player)
                    self.set_tournament.show('AddOk')
                else:
                    self.set_tournament.show('AddNok')
            else:
                self.set_tournament.show('AddNok2')

    def add_player(self):
        if len(self.list_players) > len(self.tournament.id_players):
            for player in self.list_players:
                if player.id_player not in self.tournament.id_players:
                    Player.__str__(player)

            self.set_player.menu_list_player("id")
            choice = None
            while choice != "q":
                try:
                    choice = self.set_player.menu_list_player("list")
                    if choice == "q":
                        self.check_second_menu()
                    elif int(choice) in self.list_id:
                        for player in self.list_players:
                            if player.id_player == int(choice) and len(self.tournament.player) < self.tournament.nb_player:
                                self.tournament.id_players.append(int(choice))
                                self.tournament.player.append(player)
                                self.set_tournament.show('AddOk')
                            else:
                                self.set_tournament.show('AddNok')
                    else:
                        self.error.show_error("IndexError")
                except ValueError:
                    self.error.show_error("ValueError")
                except TypeError:
                    self.error.show_error("TypeError")
        else:
            self.error.show_error("NoPlayer")
            self.check_second_menu()

    def create_tour(self):

        i = 0
        while i < self.tournament.nb_tours:
            i += 1
            name = "Round" + str(i)
            list_matchs = []
            date_start = datetime.now()
            date_start = date_start.strftime("%d/%m/%Y %H:%M:%S")
            date_end = None
            current_round = Tour(name, list_matchs, date_start, date_end)
            self.list_tour.append(current_round)
            self.tournament.list_tour.append(current_round)

    def create_match(self, method):

        # reinitialise la liste des matchs pour en ajouter de nouveaux au round suivant
        self.list_matchs = []
        # reinitialise la liste des joueurs triés
        list_sort_players = []
        # determine le nombre de match a créer (1 round = 1 match par joueur)
        nb_match = floor(len(self.tournament.player) / 2)

        # Triage des joueurs par score
        self.tournament.player.sort(key=attrgetter('score'), reverse=True)

        # puis triage des joueurs par rank, pour les joueurs ayant le meme score
        low_list = [list(v) for k, v in itertools.groupby(self.tournament.player)]
        for player in low_list:
            player.sort(key=attrgetter('rank'))
            for u in player:
                # incremente une liste trié pour le round a venir
                list_sort_players.append(u)

        # method split utilisé pour le premier round
        if method == "split":
            upper_player, lower_player = self.split_player(list_sort_players)
            for i in range(int(nb_match)):
                j1 = upper_player[i]
                j2 = lower_player[i]
                pair = f"{j1.id_player}/{j2.id_player}"
                self.list_associate_player.append(pair)
                self.list_matchs.append(Match(upper_player[i], lower_player[i], 0, 0))

        # metode swiss pour les round suivant
        elif method == "swiss":
            long = int(len(list_sort_players))
            valid_match = False
            rematch = 0

            while not valid_match:
                # reinitialise la liste des joueurs utilisés pour le round suivant
                used_players = []
                for j in range(long - 1):
                    j1 = list_sort_players[j]
                    if j1 not in used_players:
                        for k in range(long):
                            if k > j:
                                if rematch > 0:
                                    j = j + rematch
                                j2 = list_sort_players[k]
                                if j2 not in used_players and j1 not in used_players and j1 != j2:
                                    pair = f"{j1.id_player}/{j2.id_player}"
                                    if pair not in self.list_associate_player:
                                        self.list_associate_player.append(pair)
                                        used_players.append(j1)
                                        used_players.append(j2)
                                        new_match = Match(j1, j2, 0, 0)
                                        self.list_matchs.append(new_match)

                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                    else:
                        pass
                if len(self.list_matchs) < nb_match:
                    for i in range(len(self.list_matchs)):
                        self.list_associate_player.pop()
                    self.list_matchs = []
                    if rematch == 0:
                        rematch = 1
                    else:
                        rematch += 1
                else:
                    # si un joueur n'est pas utilisé dans les matchs du round,
                    for player in list_sort_players:
                        if player not in used_players:
                            # alors il gagne un point
                            player.score += 1
                            used_players.append(player)
                    valid_match = True

        self.add_match_to_round()

    def add_match_to_round(self):

        set_dateend = False
        i = 0
        while not set_dateend:
            tour = self.list_tour[i]
            if not tour.date_end:
                tour.list_matchs = self.list_matchs
                tour.__str__()
                set_dateend = True
            else:
                i += 1

    def solve_matchs(self, matchs):
        print("Pour chaque match ci dessous, taper le numéro du vainqueur\n"
              "Taper 3 en cas d'égalité")
        for match in matchs:
            win = int(input(f"[1]-{match.player_1.name} VS [2]-{match.player_2.name} [3]-Egalite"))
            if win == 1:
                match.score_1 += 1
                match.player_1.score += 1
            elif win == 2:
                match.score_2 += 1
                match.player_2.score += 1
            elif win == 3:
                match.score_1 += 0.5
                match.player_1.score += 0.5
                match.score_2 += 0.5
                match.player_2.score += 0.5
            else:
                print("Erreur de saisie")

    def close_round(self):

        end_tour = False
        i = 0
        while not end_tour:
            if i < len(self.list_tour):
                tour = self.list_tour[i]
                if not tour.date_end:
                    tour.date_end = datetime.now()
                    tour.date_end = tour.date_end.strftime("%d/%m/%Y %H:%M:%S")
                    end_tour = True
                else:
                    i += 1
            else:
                end_tour = True

    def edit_rank(self):

        if len(self.list_players) > 0:
            for player in self.list_players:
                Player.__str__(player)

            choice = None
            while choice != "q":
                try:
                    choice = self.set_player.menu_list_player("rank")
                    if choice == "q":
                        self.run()
                    elif int(choice) in self.list_id:
                        new_rank = self.set_player.menu_list_player("new_rank")
                        for player in self.list_players:
                            if player.id_player == int(choice):
                                player.rank = new_rank
                    else:
                        self.error.show_error("IndexError")
                except ValueError:
                    self.error.show_error("ValueError")
                except TypeError:
                    self.error.show_error("TypeError")
        else:
            self.error.show_error("NoPlayer")
            self.run()

    @staticmethod
    def split_player(list):
        half = len(list)//2
        return list[:half], list[half:]

    def serialized(self):
        """
        Function de sauvegarde complete des tournois et joueurs
        dans un fichier db.json
        """

        db = TinyDB('db.json')
        # creation table players
        players_table = db.table('players')
        players_table.truncate()

        # création table tournament
        tournaments_table = db.table('tournaments')
        tournaments_table.truncate()

        serialized_players = []
        serialized_tournaments = []
        serialized_tours = []
        serialized_matchs = []

        # serialized de la liste complète des joueurs
        for player in self.list_players:
            serialized_player = {'id':player.id_player,
                                 'name': player.name,
                                 'family_name': player.family_name,
                                 'birthday': str(player.birthday),
                                 'sex': player.sex,
                                 'rank': player.rank}
            serialized_players.append(serialized_player)
        players_table.insert_multiple(serialized_players)

        # serialized de la liste des tournois
        for tournament in self.list_tournament:
            #serialized de la liste des tours d'un tournoi
            for tour in tournament.list_tour:
                #serialized de la liste des matchs d'un tour
                for match in tour.list_matchs:

                    serialized_match = {'p1' : match.player_1.id_player,
                                        'p2' : match.player_2.id_player,
                                        's1' : match.score_1,
                                        's2' : match.score_2}
                    serialized_matchs.append(serialized_match)

                serialized_tour = {'name' : tour.name,
                                   'list_m' : serialized_matchs,
                                   'date_s' : tour.date_start,
                                   'date_e' : tour.date_end}
                serialized_tours.append(serialized_tour)

            serialized_tournament = {'name': tournament.name,
                                     'place': tournament.place,
                                     'date_start': str(tournament.date_start),
                                     'date_end': str(tournament.date_end),
                                     'id_player': tournament.id_players,
                                     'game_mod': tournament.game_mode,
                                     'descr': tournament.description,
                                     'nb_tours' : tournament.nb_tours,
                                     'nb_player': tournament.nb_player,
                                     'list_tour' : serialized_tours,
                                     'result': tournament.result}
            serialized_tournaments.append(serialized_tournament)
        tournaments_table.insert_multiple(serialized_tournaments)
        db.close()

        print('Enregistrement terminé')

    def deserialized(self):
        db = TinyDB('db.json')
        players_table = db.table('players')
        tournaments_table = db.table('tournaments')
        serialized_players = players_table.all()
        serialized_tournaments = tournaments_table.all()

        for serialized_player in serialized_players:
            id = serialized_player['id']
            name = serialized_player['name']
            fname = serialized_player['family_name']
            birth = serialized_player['birthday']
            sex = serialized_player['sex']
            rank = serialized_player['rank']
            player = Player(id, fname, name, birth, sex, rank)
            self.list_id.append(id)
            self.list_players.append(player)

        self.list_tour = []
        for serialized_tournament in serialized_tournaments:

            self.list_tour = []
            for serialized_tour in serialized_tournament['list_tour']:

                self.list_matchs = []
                for serialized_match in serialized_tour['list_m']:

                    p1_id = serialized_match['p1']
                    p2_id = serialized_match['p2']
                    s1 = serialized_match['s1']
                    s2 = serialized_match['s2']

                    for player1 in self.list_players:
                        if player1.id_player == p1_id:
                            p1 = player1

                    for player2 in self.list_players:
                        if player2.id_player == p2_id:
                            p2 = player2

                    match = Match(p1, p2, s1, s2)
                    self.list_matchs.append(match)

                name = serialized_tour['name']
                list_m = self.list_matchs
                date_s = serialized_tour['date_s']
                date_e = serialized_tour['date_e']
                tour = Tour(name, list_m, date_s, date_e)
                self.list_tour.append(tour)

            name = serialized_tournament['name']
            place = serialized_tournament['place']
            date_start = serialized_tournament['date_start']
            date_end = serialized_tournament['date_end']
            id_player = serialized_tournament['id_player']
            game_mod = serialized_tournament['game_mod']
            descr = serialized_tournament['descr']
            list_tour = self.list_tour
            nb_tours = serialized_tournament['nb_tours']
            nb_player = serialized_tournament['nb_player']
            result = serialized_tournament['result']
            tournament = Tournament(name, place, date_start,
                                    date_end, id_player, game_mod,
                                    descr, nb_tours,
                                    nb_player, result)
            self.list_tournament.append(tournament)

        print('Importation terminée')