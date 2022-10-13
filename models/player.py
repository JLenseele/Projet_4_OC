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
        return print(f"----------------\n"
                     f"[{self.id_player}] Name : {self.family_name} {self.name}\n"
                     f"Classement : {self.rank}\n"
                     f"----------------")

    def set_list_id(self):
        return self.id_player