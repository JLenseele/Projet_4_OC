class SetPlayer:

    def __init__(self):
        self.dict_player = {"Family_name" : "Nom : ",
                            "Birthday" : "Date de naissance  : ",
                            "Name" : "Prénom : ",
                            "Sex" : "Genre (M/F) : ",
                            "Rank" : "Classement actuel : "}

    def write(self, attr):
        return input(self.dict_player[attr])

    def list_player(self):
        pass
