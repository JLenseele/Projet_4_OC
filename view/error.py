class Error:

    def __init__(self):
        self.error_message = None
        self.dict_error = {"ValueError": "/!\ Vous devez saisir un nombre",
                           "MenuError" : "/!\ Ce choix n'est pas disponible"}

    def show_error(self, error):
        print(self.dict_error[error])

