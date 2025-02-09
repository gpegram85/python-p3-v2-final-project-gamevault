#!/usr/bin/env python3

from models import CONN, CURSOR
from models.game import Game
from models.player import Player

def seed_database():
    Game.drop_table()
    Player.drop_table()
    Game.create_table()
    Player.create_table()

    sql = """
        CREATE TABLE IF NOT EXISTS players_games (
        id INTERGER PRIMARY KEY,
        player_id INTEGER,
        game_id INTEGER,
        score TEXT,
        FOREIGN KEY (player_id) REFERENCES players(id),
        FOREIGN KEY (game_id) REFERENCES games(id)
        );
    """
    CURSOR.execute(sql)
    CONN.commit()

    # Seed data creation
    player_one = Player.create("Grey")
    player_two = Player.create("Rachel")
    player_three = Player.create("Rowan")
    
    game_one = Game.create("Borderlands", "FPS")
    game_two = Game.create("Fortnite", "FPS")
    game_three = Game.create("Mario Kart", "Racing")
