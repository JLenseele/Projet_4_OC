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
        form = "{0:8}{1:10}{2:10}{3:12}{4:3}{5:4}"
        return print(form.format(self.id_player,
                                 self.name,
                                 self.family_name,
                                 self.birthday,
                                 self.sex,
                                 self.rank))

    def set_list_id(self):
        return self.id_player