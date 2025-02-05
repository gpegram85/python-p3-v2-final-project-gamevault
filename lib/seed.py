#!/usr/bin/env python3

from models import CONN, CURSOR
from models.game import Game
from models.player import Player

def seed_database():
    Game.drop_table()
    Player.drop_table()
    Game.create_table()
    Player.create_table()

    # Seed data creation
    player_one = Player.create("GBP", "1,000,000")
    player_two = Player.create("RSH", "865,190")

    Game.create("Title One", "Action/RPG", "Placeholder description.")
    Game.create("Title Two", "Action/RPG", "Placeholder description.")
    Game.create("Title Three", "Action/RPG", "Placeholder description.")
    Game.create("Title Four", "Action/RPG", "Placeholder description.")
    Game.create("Title Five", "Action/RPG", "Placeholder description.")
