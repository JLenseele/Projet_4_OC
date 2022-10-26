import datetime


class Player:
    def __init__(self, id_player, family_name, name, birthday, sex, rank, score=0):
        self.id_player = id_player
        self.family_name = family_name
        self.name = name
        self.birthday = birthday
        self.sex = sex
        self.rank = rank
        self.score = score

    def __str__(self):
        form = "{0:^7}{1:^16}{2:^16}{3:^17}{4:^4}{5:^10}"
        return print(form.format(self.id_player,
                                 self.name,
                                 self.family_name,
                                 self.birthday.strftime("%d %b %Y"),
                                 self.sex,
                                 self.rank))

    def set_list_id(self):
        return self.id_player

    def score_reset(self):
        self.score = 0
        return