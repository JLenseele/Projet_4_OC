class Match:
    """
    Class for match

    attr:
    -- player_1
    -- player_2
    -- score for player_1
    -- score for player_2
    """

    def __init__(self, first_player, second_player, first_score, second_score):
        self.player_1 = first_player
        self.player_2 = second_player
        self.score_1 = first_score
        self.score_2 = second_score

    def __str__(self):
        return ([self.player_1.id_player, self.score_1], [self.player_2.id_player, self.score_2])
