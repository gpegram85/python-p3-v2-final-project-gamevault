from game import Game
from models.__init__ import CURSOR, CONN

class Player:

    all = {}

    def __init__(self, name, id=None):
        
        # Ensure name is a string fitting parameters
        if not isinstance(name, str) or not (3 <= len(name) <= 15):
            raise AttributeError("Name must be a string between 3 and 15 characters inclusive.")
        self._name = name
        self._id = id
                
        Player.all[self._id] = self

    def __repr__(self):
        return f"Player(name='{self._name}')"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self):
        if hasattr(self, "_name"):
            raise AttributeError("Name cannot be changed after instantiation.")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Player instances """
        sql = """
            CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT,
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create(cls, name):
        """ Initialize a new Player instance and save the object to the database """
        player = cls(name)
        player.save()
        return player

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Player instances """
        sql = """
            DROP TABLE IF EXISTS players;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name of the current Player object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO players (name)
                VALUES (?)
        """

        CURSOR.execute(sql, (self.name,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        Player.all[self.id] = self

    @classmethod
    def find_by_id(cls, id):
        """Return Player object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM players
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(*row) if row else None

    def games(self):
        """Get all games this player has played"""
        sql = """
            SELECT games.id, games.title, games.genre FROM games
            JOIN players_games ON games.id = players_games.game_id
            WHERE players_games.player_id = ?
        """
        return CURSOR.execute(sql, (self._id,)).fetchall()
    
    def add_gam(self, game, score):
        """Associate a player with a game and record the score"""
        if not isinstance(game, Game):
            raise AttributeError("Game must be an instance of Game.")
        
        sql = """
            INSERT INTO players_games (player_id, game_id, score)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.id, game.id, score))
        CONN.commit()

    def update(self):
        """Update the table row corresponding to the current Player instance."""
        sql = """
            UPDATE players
            SET game = ?, score = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.game, self.score, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Player instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM players
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Player object having the attribute values from the table row."""

        return cls(row[1], id=row[0])

    @classmethod
    def get_all(cls):
        """Return a list containing one Player object per table row"""
        sql = """
            SELECT *
            FROM players
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        """Return Player object corresponding to first table row matching specified title"""
        sql = """
            SELECT *
            FROM players
            WHERE name = ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    