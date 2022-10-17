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
from operator import attrgetter
from datetime import datetime
from itertools import groupby

GAME_MODE = ("bullet", "blitz", "fast")
NB_TOURS = 4
NB_PLAYER = 8
NB_MATCH_PER_TOUR = 2


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
                    self.show_report()
                elif main_menu == 4:
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
                    else:
                        self.start_tournament()
                        valid_choice = True
                elif second_menu == 2:
                    self.create_player()
                    valid_choice = True
                elif second_menu == 3:
                    self.add_player()
                    valid_choice = True
                elif second_menu == 4:
                    self.run()
                    valid_choice = True
                elif second_menu == 5:
                    valid_choice = True
                    quit()
                else:
                    self.error.show_error("MenuError")

    def start_tournament(self):

        valid_choice = False
        while not valid_choice:
            try:
                main_menu = self.menu.start_round()
            except ValueError:
                self.error.show_error("ValueError")
            else:
                if main_menu == 1:
                    self.create_tour()
                    valid_choice = True
                elif main_menu == 2:
                    valid_choice = True
                    quit()
                else:
                    self.error.show_error("MenuError")

        i = 0
        while i < NB_TOURS:
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
        self.menu.show_result()

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
        date_format = "%Y/%m/%d"
        while not valid_date:
            try:
                date_start = self.set_tournament.write("Date_start")
                date_start = datetime.strptime(date_start, date_format)
            except ValueError:
                self.error.show_error("DateTournament")
            except TypeError:
                print("error TypeError")
            else:
                valid_date = True

        valid_date = False
        date_format = "%Y/%m/%d"
        while not valid_date:
            try:
                date_end = self.set_tournament.write("Date_end")
                date_end = datetime.strptime(date_end, date_format)
            except ValueError:
                self.error.show_error("DateTournament")
            except TypeError:
                print("error TypeError")
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

        self.tournament = Tournament(name, place, date_start, date_end, id_players, game_mod, description, list_tour, nb_rounds, nb_player)
        self.tournament.__str__()
        self.list_tournament.append(self.tournament)

        self.check_second_menu()

    def pick_tournament(self):

        pick = int(self.set_tournament.show_list_tournament(self.list_tournament)) - 1
        if pick > -1:
            try :
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

        birthday = self.set_player.write("Birthday")
        sex = self.set_player.write("Sex")
        rank = self.set_player.write("Rank")

        player = Player(id_player, family_name, name, birthday, sex, rank)
        self.list_players.append(player)
        self.check_second_menu()

    def add_player(self):
        if len(self.list_players) > 0:
            for player in self.list_players:
                Player.__str__(player)


        else:
            self.error.show_error("NoPlayer")


    def set_list_id(self):
        """
        Add all id_player in a list
        for a current tournament
        """
        for player in self.list_players:
            self.list_id.append(player.id_player)
            self.add_list_id_tournament()
        print("Les joueurs sont ajoutéés au tournoi")
        self.tournament.__str__()

    def create_tour(self):

        i = 0
        while i < NB_TOURS:
            i += 1
            name = "Round" + str(i)
            list_matchs = []
            date_start = datetime.now()
            date_start = date_start.strftime("%d/%m/%Y %H:%M:%S")
            date_end = None
            current_round = Tour(name, list_matchs, date_start, date_end)
            self.list_tour.append(current_round)

    def create_match(self, method):

        # reinitialise la liste des matchs pour en ajouter de nouveaux au round suivant
        self.list_matchs = []
        # reinitialise la liste des joueurs triés
        list_sort_players = []
        # determine le nombre de match a créer (1 round = 1 match par joueur)
        nb_match = len(self.list_players) / NB_MATCH_PER_TOUR

        # Triage des joueurs par score
        self.list_players.sort(key=attrgetter('score'), reverse=True)

        # puis triage des joueurs par rank, pour les joueurs ayant le meme score
        L = [list(v) for k, v in itertools.groupby(self.list_players)]
        for l in L:
            l.sort(key=attrgetter('rank'))
            for u in l:
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
            print(long)
            valid_match = False
            rematch = 0
            while valid_match == False:
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
                    valid_match = True




        self.add_match_to_round()

    def add_list_id_tournament(self):
        self.tournament.id_players = self.list_id

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
            win = int(input(f"[1]-{match.player_1.name} VS [2]-{match.player_2.name} [3]-Draw"))
            if win == 1:
                match.player_1.score += 1
            elif win == 2:
                match.player_2.score += 1
            elif win == 3:
                match.player_1.score += 0.5
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

    @staticmethod
    def split_player(list):
        half = len(list)//2
        return list[:half], list[half:]
