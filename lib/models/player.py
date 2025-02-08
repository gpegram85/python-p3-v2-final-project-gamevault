from game import Game

class Player:

    all =[]

    def __init__(self, name, game, highscore):
        
        # Ensure name is a string fitting parameters
        if not isinstance(name, str) or not (3 <= len(name) <= 15):
            raise AttributeError("Name must be a string between 3 and 15 characters inclusive.")
        self._name = name

        # Ensure game is an instance of Game
        if not isinstance(game, Game):
            raise AttributeError("Game must be an instance of game.")
        self._game = game

        # Ensure highscore is a string fitting parameters
        if not isinstance(highscore, str):
            raise AttributeError("Highscore must be a string.")
        self._highscore = highscore
        
        Player.all.append(self)

    def __repr__(self):
        return f"Player(name='{self._name}', game='{self._game}')"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self):
        if hasattr(self, "_name"):
            raise AttributeError("Name cannot be changed after instantiation.")
        
    @property
    def game(self):
        return self._game
    
    @game.setter
    def game(self, new_game):
        if not isinstance(new_game, Game):
            raise AttributeError("Game must be an instance of Game.")
        self._game = new_game

    # need class methods
    # CRUD

    # need properties and setters
    # name, Game, highscore 