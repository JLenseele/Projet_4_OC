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
from random import random as rd

GAME_MODE = ("bullet", "blitz", "fast")
NB_TOURS = 4
NB_PLAYER = 2
NB_MATCH_PER_TOUR = 2


class MainController:
    """Main controller."""
    def __init__(self):
        # models
        self.players = []
        self.tournament = None
        self.list_id = []
        self.list_tour = []
        self.list_matchs = []

        # view
        self.menu = Menu()
        self.set_tournament = SetTournament()
        self.set_player = SetPlayer()
        self.error = Error()

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
                    valid_choice = True
                    quit()
                else:
                    self.error.show_error("MenuError")

        valid_choice = False
        while not valid_choice:
            try:
                main_menu = self.menu.main_menu()
            except ValueError:
                self.error.show_error("ValueError")
            else:
                if main_menu == 1:
                    self.add_player()
                    self.set_list_id()
                    valid_choice = True
                elif main_menu == 2:
                    valid_choice = True
                    quit()
                else:
                    self.error.show_error("MenuError")

        valid_choice = False
        while not valid_choice:
            try:
                main_menu = self.menu.start_round()
            except ValueError:
                self.error.show_error("ValueError")
            else:
                if main_menu == 1:
                    self.create_match()
                    self.create_tour()
                    valid_choice = True
                elif main_menu == 2:
                    valid_choice = True
                    quit()
                else:
                    self.error.show_error("MenuError")

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

        valid_desc = False
        while not valid_desc:
            description = self.set_tournament.write("Description")
            if len(description) < 10:
                self.error.show_error("DescTournament")
            else:
                valid_desc = True

        list_tour = []
        id_players = []

        self.tournament = Tournament(name, place, date_start, date_end, id_players, game_mod, description, list_tour)
        self.tournament.__str__()

    def add_player(self):
        """
        Call Menu to add some player
        to the tournament
        """
        while len(self.players) < NB_PLAYER:
            id_player = 10000
            while id_player in self.list_id:
                id_player = random.randint(10000, 99999)

        valid_fname = False
        while not valid_fname:
            family_name = self.set_player.write("Family_name")
            if any(chr.isdigit() for chr in family_name):
                self.error.show_error("NoNb")
            elif len(family_name) > 40:
                self.error.show_error("TooLong")
            else:
                valid_fname = True

        valid_name = False
        while not valid_name:
            name = self.set_player.write("Name")
            if any(chr.isdigit() for chr in name):
                self.error.show_error("NoNb")
            elif len(family_name) > 40:
                self.error.show_error("TooLong")
            else:
                valid_name = True

            birthday = self.set_player.write("Birthday")
            sex = self.set_player.write("Sex")
            rank = self.set_player.write("Rank")

            player = Player(id_player, family_name, name, birthday, sex, rank)
            self.players.append(player)

    def set_list_id(self):
        """
        Add all id_player in a list
        for a current tournament
        """
        for player in self.players:
            self.list_id.append(player.id_player)
        print("--------------------\n"
              "Les 8 joueurs sont ajoutéés au tournoi :")
        self.tournament.__str__()

    def add_list_id_tournament(self):
        for list in self.tournament:
            list.list_player = self.list_id

    def create_match(self):
        nb_match = len(self.players) / NB_MATCH_PER_TOUR
        self.sort_player()
        upper_player, lower_player = self.split_player(self.players)
        for i in range(int(nb_match)):
            self.list_matchs.append(Match(upper_player[i], lower_player[i], 0, 0))

    def sort_player(self):
        self.players.sort(key=attrgetter('rank'))

    @staticmethod
    def split_player(self, list):
        half = len(list)//2
        return list[:half], list[half:]

    def create_tour(self):
        if not self.list_tour:
            name = "Round 1"
            list_matchs = self.list_matchs
            date_start = datetime.now()
            date_start = date_start.strftime("%d/%m/%Y %H:%M:%S")
            date_end = None
            self.list_tour.append(Tour(name, list_matchs, date_start, date_end))
