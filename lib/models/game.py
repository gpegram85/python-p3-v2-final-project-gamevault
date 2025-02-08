from models.__init__ import CURSOR, CONN

class Game:

    all = []

    def __init__(self, title, genre, id=None):
        self.id = id
        if not isinstance(title, str) or not len(title) > 0:
            raise AttributeError("Title must be a string of 1 or more characters.")
        self._title = title
        if not isinstance(genre, str) or not len(genre) > 0:
            raise AttributeError("Genre must be a string of 1 or more characters.")
        self._genre = genre
        # if not isinstance(description, str) or not len(description) > 0:
        #     raise AttributeError("Description must be a string of 1 or more characters.")
        # self._description = description
        Game.all.append(self)

    def __repr__(self):
        return f"<Game {self.id}: {self._title}, {self.genre}>"
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self):
        if hasattr(self, "_title"):
            raise AttributeError("Title cannot be changed after instantiation.")
        
    @property
    def genre(self):
        return self._genre
    
    @genre.setter
    def genre(self, value):
        if not isinstance(value, str) or not len(value) > 0:
            raise AttributeError("New Genre must be a string of 1 or more characters.")
        self._genre = value

    # @property
    # def description(self):
    #     return self._description
    
    # @description.setter
    # def description (self, value):
    #     if not isinstance(value, str) or not len(value) > 0:
    #         raise AttributeError("Description must be a string of 1 or more characters.")
    #     self._description = value

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Game instances """
        sql = """
            CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            title TEXT,
            genre TEXT,
            description TEXT,
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Game instances """
        sql = """
            DROP TABLE IF EXISTS games;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the title, genre, and description of the current Game object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO games (title, genre, description)
                VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.title, self.genre, self.description))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Game instance."""
        sql = """
            UPDATE games
            SET title = ?, genre = ?, description = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.title, self.genre,
                             self.description, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Game instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM games
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, title, genre, description):
        """ Initialize a new Game instance and save the object to the database """
        game = cls(title, genre, description)
        game.save()
        return game

    @classmethod
    def instance_from_db(cls, row):
        """Return a Game object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        game = cls.all.get(row[0])
        if game:
            # ensure attributes match row values in case local instance was modified
            game.title = row[1]
            game.genre = row[2]
            game.description = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            game = cls(row[1], row[2], row[3])
            game.id = row[0]
            cls.all[game.id] = game
        return game

    @classmethod
    def get_all(cls):
        """Return a list containing one Game object per table row"""
        sql = """
            SELECT *
            FROM games
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Game object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM games
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, title):
        """Return Game object corresponding to first table row matching specified title"""
        sql = """
            SELECT *
            FROM games
            WHERE title is ?
        """

        row = CURSOR.execute(sql, (title,)).fetchone()
        return cls.instance_from_db(row) if row else None

    