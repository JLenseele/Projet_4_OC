class Tour:

    def __init__(self, name, list_matchs, date_start, date_end):
        self.name = name
        self.list_matchs = list_matchs
        self.date_start = date_start
        self.date_end = date_end

    def __str__(self):
        return self.name