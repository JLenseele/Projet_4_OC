from models.tournament import Tournament
from models.player import Player
from models.tour import Tour
from models.match import Match
from view.view import Menu
from view.error import Error
from operator import attrgetter
from datetime import datetime

GAME_MODE = ("bullet", "blitz", "fast")
NB_TOURS = 4
NB_PLAYER = 2
NB_MATCH_PER_TOUR = 2


class MainControler:
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
        self.error = Error()

    def run(self):

        valid_choice = False
        while valid_choice == False:
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

        self.add_player()
        self.set_list_id()
        self.create_match()
        self.create_tour()

    def create_tournament(self):

        valid_name = False
        while not valid_name:
            name = self.menu.set_name_tournament()
            if len(name) < 3:
                self.error.name_tournament()
            else:
                valid_name = True

        place = self.menu.set_place_tournament()
        date_start = self.menu.set_date_start()
        date_end = self.menu.set_date_end()
        id_players = []

        mods = ""
        for mod in GAME_MODE:
            mods = f"{mods} / {mod}"

        game_mode = self.menu.set_game_mode(mods)
        description = self.menu.set_description()
        list_tour = []
        self.tournament = Tournament(name, place, date_start, date_end, id_players, game_mode, description, list_tour)

    def add_player(self):
        """
        Call Menu to add some player
        to player list
        """
        while len(self.players) < NB_PLAYER:
            id_player = self.menu.set_id_player()
            family_name = self.menu.set_family_name()
            name = self.menu.set_name_player()
            birthday = self.menu.set_birthday()
            sex = self.menu.set_sex()
            rank = self.menu.set_rank()
            player = Player(id_player, family_name, name, birthday, sex, rank)
            self.players.append(player)

    def set_list_id(self):
        """
        Add all id_player in a list
        for a current tournament
        """
        for player in self.players:
            self.list_id.append(player.id_player)

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

    def split_player(self, list):
        half = len(list)//2
        return list[:half], list[half:]

    def create_tour(self):
        if self.list_tour == []:
            name = "Round 1"
            list_matchs = self.list_matchs
            date_start = datetime.now()
            date_start = date_start.strftime("%d/%m/%Y %H:%M:%S")
            date_end = None
            self.list_tour.append(Tour(name, list_matchs, date_start, date_end))

