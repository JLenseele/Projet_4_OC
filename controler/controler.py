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
from itertools import groupby
from random import randint


GAME_MODE = ("bullet", "blitz", "fast")
GENDER = ('m', 'f', 'M', 'F')


class MainController:
    """Main controller."""

    def __init__(self):
        # models
        self.tournament = None
        self.states = None

        # views
        self.menu = Menu()
        self.set_tournament = SetTournament()
        self.set_player = SetPlayer()
        self.error = Error()
        self.report = Report()

        # listes du controller
        self.list_id = []
        self.list_matchs = []
        self.list_tournament = []
        self.list_associate_player = []
        self.list_players = []

    def run(self):
        """Function start sur le menu principal"""

        valid_choice = False
        while not valid_choice:
            try:
                main_menu = self.menu.main_menu(self.tournament)
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
                    self.report.prompt_report(self.list_tournament,
                                              self.list_players,
                                              report)
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
        """
        Function du second menu
        """
        valid_choice = False
        while not valid_choice:
            try:
                second_menu = self.menu.second_menu()
            except ValueError:
                self.error.show_error("ValueError")
            else:
                if second_menu == 1:
                    # vérifie si un tournoi n'est pas déjà en cour
                    if self.states:
                        if self.states != self.tournament.name:
                            self.set_tournament.show('Open')
                            self.run()
                    else:
                        self.states = self.tournament.name
                    # verifies s'il y a assez de joueurs dans le tournoi
                    if self.tournament.nb_player > len(self.tournament.id_players):
                        self.error.show_error("PlayerMissing")
                        print(f"({len(self.tournament.id_players)} / {self.tournament.nb_player})\n")
                    else:
                        valid_choice = True
                        self.tournament.open = 'started'
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

    def create_tournament(self):
        """
        Récupère et valide les inputs users
        Instancie un nouveau tournoi
        """
        name = self.input_str_validation('tournament', 'Name', 'NameTournament')
        place = self.input_str_validation('tournament', 'Place', 'PlaceTournament')
        date_start = self.input_date_validation('tournament', 'Date_start', 'DateFormat')
        date_end = self.input_date_validation('tournament', 'Date_end', 'DateFormat', date_start)
        game_mod = self.input_str_validation('tournament', 'Game_mod', 'ModTournament')
        nb_player = self.input_int_validation('tournament', 'Nb_player', 'TooMuchPlayer')
        nb_rounds = self.input_int_validation('tournament', 'Nb_rounds', 'TooMuchRounds', nb_player)
        description = self.input_str_validation('tournament', 'Description', 'DescTournament')
        list_tour = []
        id_players = []
        list_player = []
        # Instance du tournoi
        self.tournament = Tournament(name, place, date_start, date_end,
                                     id_players, game_mod, description,
                                     nb_rounds, nb_player, list_player,
                                     list_tour)
        # Affiche le recap du tournoi créé
        self.tournament.__str__()
        # Ajoute le tournoi dans la liste des tournois
        self.list_tournament.append(self.tournament)
        self.check_second_menu()

    def start_tournament(self):
        """  Dirige le déroulement d'un tournoi du début à la fin.

        Créer les rounds du tournoi lancé
        Défini la méthode de pairs
        Affiche le menu des resolutions de rounds
        Clos le tournoi
        Récupère les résultats
        Reset les scores
        Retour au menu principal
        """

        # Création des tours si le tournoi vient d'être créé
        if self.tournament.list_tour == []:
            self.create_tour()

        i = 0
        tour_restant = 0
        # Détermine le nombre de tours restant à jouer
        for tour in self.tournament.list_tour:
            if not tour.date_end:
                tour_restant += 1

        while i < tour_restant:

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
                        self.report.prompt_result(self.tournament)
                    elif main_menu == 3:
                        self.run()
                    else:
                        self.error.show_error("MenuError")
            i += 1
        self.tournament.open = 'End'
        self.tournament.result = (self.report.prompt_result(self.tournament))
        self.states = None

        for player in self.tournament.player:
            player.score_reset()

        self.tournament = None
        self.run()

    def pick_tournament(self):
        """Permet de sélectionner un tournoi depuis la liste des tournois"""
        pick = int(self.set_tournament.show_list_tournament(self.list_tournament)) - 1
        if pick > -1:
            try:
                self.tournament = self.list_tournament[pick]
                if self.tournament.open == 'End':
                    self.set_tournament.write('Tournament_end')
                    self.tournament.__str__()
                    self.run()
                else:
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
        """Instancie un nouveau joueur
        pour l'ajouter à la liste globale des joueurs et
        au tournoi en cours s'il y en a un
        """
        instances = self.menu.second_menu_option()
        for instance in range(instances):
            id_player = randint(10000, 99999)
            while id_player in self.list_id:
                id_player = randint(10000, 99999)

            # Validation des inputs pour chaque attribut
            f_name = self.input_str_validation('player', 'F_name', 'TooLong')
            name = self.input_str_validation('player', 'Name', 'TooLong')
            date_birth = self.input_date_validation('player', 'Birthday', 'DateFormat')
            sex = self.input_str_validation('player', 'Sex', 'Gender')
            rank = self.input_int_validation('player', 'Rank', 'ValueError')

            # Instancie un joueur
            player = Player(id_player, f_name, name, date_birth, sex, rank)

            # Ajoute le joueur dans la liste des joueurs
            self.list_players.append(player)
            # Ajoute l'id du joueur dans la liste des ID
            self.list_id.append(player.id_player)

            # Vérifie si le nombre max de joueur est atteint
            # Si oui, le joueur n'est pas ajouté au tournoi en cour
            if self.tournament:
                if len(self.tournament.player) < self.tournament.nb_player:
                    self.tournament.player.append(player)
                    self.tournament.id_players.append(player.id_player)
                    self.set_tournament.show('AddOk')
                else:
                    self.set_tournament.show('AddNok')
            else:
                self.error.show_error('AddNok2')

    def add_player(self):
        """ Permet d'ajouter des joueurs de la liste globale au tournoi en cour

        - affiche la liste globale des joueurs qui ne sont pas présent dans le tournoi
        - input id joueur pour l'ajouter au tournoi
        - Q pour quitter
        """
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
                    elif int(choice) in self.list_id and\
                            len(self.tournament.player) < self.tournament.nb_player:
                        for player in self.list_players:
                            if player.id_player == int(choice) and\
                                    int(choice) not in self.tournament.id_players:
                                self.tournament.id_players.append(int(choice))
                                self.tournament.player.append(player)
                        self.set_tournament.show('AddOk')
                    else:
                        self.error.show_error("AddNok")
                except ValueError:
                    self.error.show_error("ValueError")
                except TypeError:
                    self.error.show_error("TypeError")
        else:
            self.error.show_error("NoPlayer")
            self.check_second_menu()

    def create_tour(self):
        """ Créer un nouveau round vide pour le tournoi en cour """
        frm = '%Y-%m-%d %H:%M:%S'
        i = 0
        while i < self.tournament.nb_tours:

            i += 1
            name = "Round" + str(i)
            list_matchs = []
            date_start = datetime.strftime(datetime.now(), frm)
            date_end = None
            current_round = Tour(name, list_matchs, date_start, date_end)
            self.tournament.list_tour.append(current_round)

    def create_match(self, method):
        """ Instancie tous les matchs du round à venir """

        # reinitialise la liste des matchs pour en ajouter de nouveaux au round suivant
        self.list_matchs = []
        # reinitialise la liste des joueurs triés
        list_sort_players = []
        # determine le nombre de matchs à créer (1 round = 1 match par joueur)
        nb_match = floor(len(self.tournament.player) / 2)

        # Triage des joueurs par score
        self.tournament.player.sort(key=attrgetter('score'), reverse=True)

        # puis triage des joueurs par rank, pour les joueurs ayant le meme score
        sorted_players = sorted(self.tournament.player, key=attrgetter('score'), reverse=True)
        # regroupement des joueurs avec le meme score dans des sous liste
        grouped = [list(result) for key, result in groupby(sorted_players, key=attrgetter('score'))]

        for i in grouped:
            i.sort(key=attrgetter('rank'))
            for u in i:
                list_sort_players.append(u)

        # methode utilisé pour le premier round
        if method == "split":
            upper_player, lower_player = self.split_player(list_sort_players)
            for i in range(int(nb_match)):
                j1 = upper_player[i]
                j2 = lower_player[i]
                pair = f"{j1.id_player}/{j2.id_player}"
                reverse_pair = f"{j2.id_player}/{j1.id_player}"
                self.list_associate_player.append(pair)
                self.list_associate_player.append(reverse_pair)
                self.list_matchs.append(Match(upper_player[i], lower_player[i], 0, 0))

        # methode pour les rounds suivants
        elif method == "swiss":
            long = int(len(list_sort_players))
            valid_match = False
            rematch = 0

            while not valid_match:
                # reinitialise la liste des joueurs utilisés pour le round suivant
                used_players = []
                for j in range(long - 1):
                    # Selection du 1er joueur
                    j1 = list_sort_players[j]
                    if j1 not in used_players:
                        for k in range(rematch, long):
                            # selection du 2ᵉ joueur
                            j2 = list_sort_players[k]

                            # si les deux joueurs ne sont pas deja affectés à un autre match
                            # et sont différents :
                            if j2 not in used_players and j1 not in used_players and j1 != j2:
                                # on associe les joueurs dans "pair."
                                pair = f"{j1.id_player}/{j2.id_player}"
                                # et dans la "pair" inverse
                                reverse_pair = f"{j2.id_player}/{j1.id_player}"

                                # Si la paire ou reverse paire n'existe pas deja :
                                if pair not in self.list_associate_player and \
                                        reverse_pair not in self.list_associate_player:

                                    # Ajout des pairs dans une liste
                                    self.list_associate_player.append(pair)
                                    self.list_associate_player.append(reverse_pair)
                                    # Ajout des joueurs utilisés dans une autre liste
                                    used_players.append(j1)
                                    used_players.append(j2)
                                    # Creation du match
                                    new_match = Match(j1, j2, 0, 0)
                                    # Ajout du match dans la liste des matchs du controller
                                    self.list_matchs.append(new_match)

                # S'il n'y a pas assez de match trouvé :
                if len(self.list_matchs) < nb_match:
                    print(f"{rematch} : {len(self.list_matchs)} match trouvés")

                    # Suppression des pairs et reverse trouvés
                    for i in range(len(self.list_matchs)):
                        self.list_associate_player.pop()
                        self.list_associate_player.pop()
                    # Reinitialisation de la liste des matchs
                    self.list_matchs = []

                    # rematch s'incrémente pour lancer une nouvelle recherche
                    # de match avec +1 dans la boucle for J2
                    rematch += 1
                    if rematch == 25:
                        valid_match = True

                else:
                    # tournoi nb joueur impair :
                    # si un joueur n'est pas utilisé dans les matchs du round,
                    for player in list_sort_players:
                        if player not in used_players:
                            # alors, il gagne un point
                            player.score += 1
                            used_players.append(player)
                    valid_match = True

        # ajout des matchs dans le round en cour
        self.add_match_to_round()

    def add_match_to_round(self):
        """ Ajout de la liste des matchs créé au round en cour """
        set_dateend = False
        i = 0
        while not set_dateend:
            tour = self.tournament.list_tour[i]
            if not tour.date_end:
                tour.list_matchs = self.list_matchs
                tour.__str__()
                set_dateend = True
            else:
                i += 1

    @staticmethod
    def solve_matchs(matchs):
        """ Résolution des matchs et attribution des points"""
        print("Pour chaque match ci dessous, taper le numéro du vainqueur\n"
              "Taper 3 en cas d'égalité")
        for match in matchs:
            while True:
                win = (input(f"[1]- {match.player_1.name} VS [2]- {match.player_2.name} [3]- Égalité : "))
                if win == '1':
                    match.score_1 += 1
                    match.player_1.score += 1
                    break
                elif win == '2':
                    match.score_2 += 1
                    match.player_2.score += 1
                    break
                elif win == '3':
                    match.score_1 += 0.5
                    match.player_1.score += 0.5
                    match.score_2 += 0.5
                    match.player_2.score += 0.5
                    break
                else:
                    print("Erreur de saisie")

    def close_round(self):
        """ Cloture le round en ajoutant une date de fin """
        frm = '%Y-%m-%d %H:%M:%S'

        end_tour = False
        i = 0
        while not end_tour:
            if i < len(self.tournament.list_tour):
                tour = self.tournament.list_tour[i]
                if not tour.date_end:
                    tour.date_end = datetime.strftime(datetime.now(), frm)
                    end_tour = True
                else:
                    i += 1
            else:
                end_tour = True

    def edit_rank(self):
        """ Permet de modifier le rank (classement ligue)
        d'un joueur présent dans la liste global
        """
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
    def split_player(list_player):
        """ Divise la liste des joueurs en deux """
        half = len(list_player)//2
        return list_player[:half], list_player[half:]

    def serialized(self):
        """
        Function de sauvegarde complete des tournois et joueurs
        dans un fichier db.json
        """
        file_name = input('Nom du fichier de sauvegarde :')
        db = TinyDB(file_name + '.json')

        # creation table players
        players_table = db.table('players')
        players_table.truncate()

        # création table tournament
        tournaments_table = db.table('tournaments')
        tournaments_table.truncate()

        serialized_players = []
        serialized_tournaments = []

        # serialized de la liste complète des joueurs
        for player in self.list_players:
            serialized_player = {'id': player.id_player,
                                 'name': player.name,
                                 'family_name': player.family_name,
                                 'birthday': str(player.birthday),
                                 'sex': player.sex,
                                 'rank': player.rank,
                                 'score': player.score}
            serialized_players.append(serialized_player)
        players_table.insert_multiple(serialized_players)

        # serialized de la liste des tournois
        for tournament in self.list_tournament:
            # serialized de la liste des tours d'un tournoi
            serialized_tours = []
            for tour in tournament.list_tour:
                # serialized de la liste des matchs d'un tour
                serialized_matchs = []
                for match in tour.list_matchs:

                    serialized_match = {'p1': match.player_1.id_player,
                                        'p2': match.player_2.id_player,
                                        's1': match.score_1,
                                        's2': match.score_2}
                    serialized_matchs.append(serialized_match)

                serialized_tour = {'name': tour.name,
                                   'list_m': serialized_matchs,
                                   'date_s': str(tour.date_start),
                                   'date_e': str(tour.date_end)}
                serialized_tours.append(serialized_tour)

            serialized_tournament = {'name': tournament.name,
                                     'place': tournament.place,
                                     'date_start': str(tournament.date_start),
                                     'date_end': str(tournament.date_end),
                                     'id_player': tournament.id_players,
                                     'game_mod': tournament.game_mode,
                                     'descr': tournament.description,
                                     'nb_tours': tournament.nb_tours,
                                     'nb_player': tournament.nb_player,
                                     'list_tour': serialized_tours,
                                     'result': tournament.result,
                                     'open': tournament.open}
            serialized_tournaments.append(serialized_tournament)
        tournaments_table.insert_multiple(serialized_tournaments)
        db.close()

        print('Enregistrement terminé')

    def deserialized(self):
        """ Instancie tous les joueurs / tournoi du fichier de sauvegarde JSON"""
        file_name = input('Nom du fichier de sauvegarde :')
        db = TinyDB(file_name + '.json')
        players_table = db.table('players')
        tournaments_table = db.table('tournaments')
        serialized_players = players_table.all()
        serialized_tournaments = tournaments_table.all()
        frm_date = '%Y-%m-%d %H:%M:%S'
        i = 0
        j = 0

        for serialized_player in serialized_players:
            if serialized_player['id'] not in self.list_id:
                id_player = serialized_player['id']
                name = serialized_player['name']
                fname = serialized_player['family_name']
                birth = datetime.strptime(serialized_player['birthday'], frm_date)
                sex = serialized_player['sex']
                rank = serialized_player['rank']
                score = serialized_player['score']
                player = Player(id_player, fname, name, birth, sex, rank, score)
                self.list_id.append(id_player)
                self.list_players.append(player)
                i += 1

        list_name_t = []
        for tournament in self.list_tournament:
            list_name_t.append(tournament.name)

        for serialized_tournament in serialized_tournaments:
            if serialized_tournament['name'] not in list_name_t:
                list_tour = []
                for serialized_tour in serialized_tournament['list_tour']:

                    list_matchs = []
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
                        list_matchs.append(match)

                    name = serialized_tour['name']
                    list_m = list_matchs
                    date_s = datetime.strptime(serialized_tour['date_s'], frm_date)
                    if serialized_tour['date_e'] == 'None':
                        date_e = None
                    else:
                        date_e = datetime.strptime(serialized_tour['date_e'], frm_date)
                    tour = Tour(name, list_m, date_s, date_e)
                    list_tour.append(tour)

                name = serialized_tournament['name']
                place = serialized_tournament['place']
                date_start = datetime.strptime(serialized_tournament['date_start'], frm_date)
                date_end = datetime.strptime(serialized_tournament['date_end'], frm_date)
                id_players = serialized_tournament['id_player']
                game_mod = serialized_tournament['game_mod']
                descr = serialized_tournament['descr']
                list_tour = list_tour
                nb_tours = serialized_tournament['nb_tours']
                nb_player = serialized_tournament['nb_player']
                result = serialized_tournament['result']
                open_t = serialized_tournament['open']
                list_player = []

                for id_player in id_players:
                    for player in self.list_players:
                        if id_player == player.id_player:
                            list_player.append(player)

                tournament = Tournament(name, place, date_start,
                                        date_end, id_players, game_mod,
                                        descr, nb_tours,
                                        nb_player, list_player, list_tour, result, open_t)
                self.list_tournament.append(tournament)
                j += 1

        print(f"Importation terminée "
              f"( {j} Tournoi(s) / "
              f"{i} Joueur(s) )")

    def input_str_validation(self, objet, attr, error):
        """ Validation des inputs type str
        : param objet : player ou tournament
        : param attr : attribut de l'objet
        : param error : msg d'erreur liée à l'attribut
        """
        valid_input = False
        while not valid_input:
            if objet == 'player':
                attribute = self.set_player.write(attr)
                if any(caract.isdigit() for caract in attribute):
                    self.error.show_error("NoNb")
                elif len(str(attribute)) > 40:
                    self.error.show_error("TooLong")
                elif attr == 'Sex' and attribute not in GENDER:
                    self.error.show_error("Gender")
                else:
                    return attribute
            else:
                attribute = self.set_tournament.write(attr)
                if attr == 'Game_mod' and attribute not in GAME_MODE:
                    self.error.show_error(error)
                elif len(attribute) < 3:
                    self.error.show_error(error)
                else:
                    return attribute

    def input_date_validation(self, objet, attr, error, condition=None):
        """ Validation des inputs de type Date
        : param objet : player ou tournament
        : param attr : attribut de l'objet
        : param error : msg d'erreur liée à l'attribut
        : param condition : comparaison avec un autre attribut
        """
        valid_input = False
        date_format = "%d/%m/%Y"

        while not valid_input:
            try:
                if objet == 'tournament':
                    attribute = self.set_tournament.write(attr)
                else:
                    attribute = self.set_player.write(attr)
                attribute = datetime.strptime(attribute, date_format)
            except ValueError:
                self.error.show_error(error)
            else:
                if attr == 'Date_end':
                    if attribute < condition:
                        self.error.show_error("DateEnd")
                    else:
                        return attribute
                else:
                    return attribute

    def input_int_validation(self, objet, attr, error, condition=None):
        """ Validation des inputs type int
        : param objet : player ou tournament
        : param attr : attribut de l'objet
        : param error : msg d'erreur liée à l'attribut
        : param condition : comparaison avec un autre attribut
        """
        valid_input = False

        while not valid_input:
            try:
                if objet == 'tournament':
                    attribute = int(self.set_tournament.write(attr))
                else:
                    attribute = int(self.set_player.write(attr))
            except ValueError:
                self.error.show_error('ValueError')
            except TypeError:
                self.error.show_error('TypeError')
            else:
                if attr == 'Nb_player' and attribute > 20:
                    self.error.show_error(error)
                elif attr == 'Nb_rounds' and attribute >= condition:
                    self.error.show_error(error)
                else:
                    return attribute
